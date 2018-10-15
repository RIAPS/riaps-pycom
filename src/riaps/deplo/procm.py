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
from concurrent.futures.thread import ThreadPoolExecutor
from _thread import RLock

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
    def __init__(self,parent):
        threading.Thread.__init__(self,daemon=True)
        self.logger = logging.getLogger(__name__)
        self.parent = parent
        self.context = parent.context
        self.endpoint = parent.endpoint
        self.proc = None
        self.command = None
        self.name = None
        self.terminated = threading.Event() # Thread must terminate
        self.terminated.clear()
        self.released = threading.Event()   # Process to be released 
        self.released.clear()
    
    def setup(self,record):
        self.name = record.name
        self.proc = record.proc
          
    def run(self):
        self.dealer = self.context.socket(zmq.DEALER)
        self.dealer.setsockopt(zmq.IDENTITY, str(self.name).encode(encoding='utf_8'))
        self.dealer.connect(self.endpoint)
        while True: 
            self.proc.wait()
            if self.terminated.is_set(): break
            if self.released.is_set(): 
                self.logger.info("expected termination: %s" % self.name)
                break
            else:
                # Process termination was unexpected
                self.logger.info("restarting process: %s" % self.name)
                self.dealer.send_pyobj((self.name,))
                # Ask parent to restart, wait until completed
                _resp = self.dealer.recv_pyobj()
        self.dealer.close()

    def release(self):
        self.released.set()
        self.logger.info("released proc %s" % self.name)
        
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
        self.lock = RLock()
        
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
                thread = ProcessMonitor(self)
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
                thread.release()
                del self.monitors[qualName]
            else:
                self.logger.error(" unknown process %s" % qualName)
    
    def __destroy__(self):
        for mon in self.monitors.keys():
            thread = self.monitors[mon]
            thread.terminate()
        self.monitors.clear()
        
        
            
    