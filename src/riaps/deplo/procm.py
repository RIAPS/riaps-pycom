'''
Created on Apr 7, 2018

@author: riaps
'''
import os,signal
import sys
import time
import json
import hashlib
from os.path import join
from collections import namedtuple
import subprocess
import threading
import logging
import traceback
import psutil
import pwd

import zmq

from riaps.consts.defs import *
from riaps.utils.sudo import is_su
from riaps.utils.config import Config
from riaps.run.exc import BuildError

ProcessMonitorRecord = namedtuple('ProcessMonitorRecord', 'name proc thread')

class ProcessMonitor(threading.Thread):
    '''
    Thread for monitoring a process
    '''
    def __init__(self,parent,qualName):
        threading.Thread.__init__(self,name='ProcessMonitor:%r' % qualName,daemon=False)
        self.logger = logging.getLogger(__name__)
        self.parent = parent
        self.context = parent.context
        self.endpoint = parent.endpoint
        self.proc = None
        self.command = None
        self.proc_name = None
        self.terminated = threading.Event() # Thread must terminate
        self.terminated.clear()
        self.released = threading.Event()   # Process to be released 
        self.released.clear()
    
    def setup(self,record):
        self.proc_name = record.name
        self.proc = record.proc
          
    def run(self):
        self.dealer = self.context.socket(zmq.DEALER)
        self.dealer.setsockopt(zmq.IDENTITY, str(self.proc_name).encode(encoding='utf_8'))
        self.dealer.connect(self.endpoint)
        self.unexpected = False
        while True: 
            self.proc.wait()
            if self.terminated.is_set(): break
            code = self.proc.returncode
            if self.released.is_set(): 
                self.logger.info("expected termination: %s[%r]" % (self.proc_name,code))
                break
            else:
                # Process termination was unexpected
                self.unexpected = True
                self.logger.error("unexpected termination: %s[%r]" % (self.proc_name,code))
                self.dealer.send_pyobj((self.proc_name,))
                # Ask parent to restart, wait until completed
                _resp = self.dealer.recv_pyobj()
                self.unexpected = False
        self.dealer.close()

    def release(self):
        self.released.set()
        self.logger.info("released proc %s" % self.proc_name)
    
    def error(self):
        return self.unexpected 
    
    def terminate(self):
        self.logger.info("terminating")
        self.terminated.set()

class ProcessManager(object):
    '''
    Manages processes: service(s) and actors started by deplo
    '''
    def __init__(self,parent):
        '''
        Constructor
        '''
        self.logger = logging.getLogger(__name__)
        self.depm = parent
        self.context = parent.context
        self.endpoint = None
        self.monitors = { }                 
        self.lock = threading.RLock()
        
    def monitor(self,qualName,proc):
        self.logger.info(" monitoring %s" % (qualName))
        with self.lock:
            if self.endpoint == None:
                self.endpoint = self.depm.procMonEndpoint
            if qualName in self.monitors:
                old = self.monitors[qualName]
                new = ProcessMonitorRecord(name=old.name,proc=proc,thread=old.thread)
                old.thread.setup(new)
                self.monitors[qualName] = new
            else:
                thread = ProcessMonitor(self,qualName)
                record = ProcessMonitorRecord(name=qualName,proc=proc,thread=thread)
                self.monitors[qualName] = record
                thread.setup(record)
                thread.start()
                time.sleep(0.01)
    
    def release(self,qualName):
        self.logger.info("releasing %s" % qualName)
        with self.lock:
            if qualName in self.monitors:
                record = self.monitors[qualName]
                thread = record.thread
                if not thread.error():
                    thread.release()
                    del self.monitors[qualName]
            else:
                self.logger.error(" unknown process %s" % qualName)
    
    def __destroy__(self):
        for mon in self.monitors.keys():
            thread = self.monitors[mon]
            thread.terminate()
        self.monitors.clear()
        
        
            
    