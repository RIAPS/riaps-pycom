'''
Resource monitors

Created on Nov 23, 2017

@author: riaps
'''

import os
import stat
import time
#import signal
import psutil
import threading
from threading import RLock
import logging
import traceback

import zmq
from zmq import devices
from zmq.error import ZMQError

from riaps.consts.defs import *
from riaps.run.exc import *
from riaps.proto import deplo_capnp
from riaps.utils.config import Config
from riaps.utils.names import *

class CPUMonitorThread(threading.Thread):
    '''
    Thread for monitoring an actor and enforcing resource limits.
    '''
    def __init__(self,parent,interval,usage):
        threading.Thread.__init__(self,name = 'CPUMonitorThread',daemon=True)
        self.logger = logging.getLogger(__name__)
        self.parent = parent
        self.context = self.parent.context
        self.interval = interval    # sec
        self.usage = usage          # % INT
        self.terminated = threading.Event() # Set when the monitor is to be terminated
        self.terminated.clear()
        self.running = threading.Event()    # Cleared when the monitor is not to run
        self.running.set()
        self.stopped = threading.Event()    # Set if the monitor is stoppped
        self.stopped.clear()
        self.lock = RLock()
        self.notifier = None
        self.notifierPort = None
        self.devices = { }
        self.alive = False
    
    def setup(self,proc):
        self.proc = proc
        self.mon = psutil.Process(proc.pid)
    
    def addClientDevice(self,appName,actorName,device):
        while self.notifierPort == None:
            time.sleep(0.1)
        with self.lock:
            device.connect_in('tcp://127.0.0.1:%i' % self.notifierPort)
            key = str(appName) + "." + str(actorName)
            identity = actorIdentity(appName,actorName,self.proc.pid)
            self.logger.info("zmqdev id = %s" % identity)
            self.devices[key] = (device,identity)
        
    def is_running(self):
        return self.alive
    
    def restart(self):
        self.stopped.clear()
        self.running.set()

    def run(self):
        self.name = 'CPUMonitorThread-%r' % self.ident 
        self.notifier = self.context.socket(zmq.ROUTER)
        # self.notifier.setsockopt(zmq.SNDTIMEO,const.deplEndpointSendTimeout)
        self.notifierPort = self.notifier.bind_to_random_port('tcp://127.0.0.1')
        self.alive = True
        current = self.mon.cpu_percent(self.interval)
        time.sleep(0.001)
        while True:
            if not self.running.is_set():
                self.stopped.set()
                self.running.wait()                    
            if self.terminated.is_set(): break
            current = self.mon.cpu_percent(self.interval)
            if self.terminated.is_set(): break
            if current == 0: continue
            self.logger.info("XCPU to [%d]? %d > %d in %f" % (self.proc.pid,current,self.usage,self.interval))
            if current > self.usage:
                # print ("SIGXCPU sent")
                # self.proc.send_signal(signal.SIGXCPU)
                with self.lock:
                    for key,pair in self.devices.items():
                        (_dev,identity) = pair
                        msg = deplo_capnp.DeplCmd.new_message()
                        msgCmd = msg.init('resourceMsg')
                        msgMessage = msgCmd.init('resCPUX')
                        msgMessage.msg = "X"
                        msgBytes = msg.to_bytes()
                        payload = zmq.Frame(msgBytes)
                        header = identity.encode(encoding='utf-8')
                        self.notifier.send_multipart([header,payload])
                        self.logger.info("XCPU sent to [%d]" % (self.proc.pid))
                time.sleep(1.0)
                # self.mon = psutil.Process(self.proc.pid)
                # current = self.mon.cpu_percent(self.interval)
            if self.terminated.is_set(): break           
        self.logger.info("CPUMonitor terminated") 
                
    def stop(self):
        self.running.clear()
        self.stopped.wait()
        
    def terminate(self):
        self.terminated.set()
        if self.stopped.is_set():
            self.stopped.clear()
            self.running.set()
            
        
    
