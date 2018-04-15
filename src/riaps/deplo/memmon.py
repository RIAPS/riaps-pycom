'''
Resource monitors

Created on Nov 23, 2017

@author: riaps
'''
from cgroupspy import trees
import os
import stat
import time
import signal
import subprocess
import psutil
import threading
from threading import RLock
import logging
import traceback
from pwd import getpwnam 

from butter.eventfd import Eventfd
from pyroute2 import DQuotSocket
import zmq
from zmq import devices
from zmq.error import ZMQError

from riaps.consts.defs import *
from riaps.run.exc import *
from riaps.proto import deplo_capnp
from riaps.utils.sudo import riaps_sudo
from riaps.utils.config import Config
    
class MemMonitorThread(threading.Thread):
    def __init__(self,parent,efd,usage):
        threading.Thread.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.parent = parent
        self.context = self.parent.context
        self.efd = efd
        self.usage = usage
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

    def addClientDevice(self,appName,actorName,device):
        while self.notifierPort == None:
            time.sleep(0.1)
        with self.lock:
            device.connect_in('tcp://127.0.0.1:%i' % self.notifierPort)
            key = str(appName) + "." + str(actorName)
            self.devices[key] = device
    
    def is_running(self):
        return self.alive
    
    def restart(self):
        self.stopped.clear()
        self.running.set()

    def run(self):
        self.notifier = self.context.socket(zmq.ROUTER)
        # self.notifier.setsockopt(zmq.SNDTIMEO,const.deplEndpointSendTimeout)
        self.notifierPort = self.notifier.bind_to_random_port('tcp://127.0.0.1')
        self.alive = True
        self.logger.info("MemMonitor:%d at %d" % (self.proc.pid,self.efd.fileno()))
        time.sleep(0.001)
        try:
            while True:
                if not self.running.is_set():
                    self.stopped.set()
                    self.running.wait()
                if self.terminated.is_set(): break
                # current = os.read(self.efd.fileno(),8) # .read_event()
                current = self.efd._read_events()
                if self.terminated.is_set(): break
                if not self.running.is_set(): continue
                self.logger.info("MemMonitor[%d] mem limit %d exceeded - %s" % (self.proc.pid,self.usage,str(current)))
                with self.lock:
                    for key,_dev in self.devices.items():
                        msg = deplo_capnp.DeplCmd.new_message()
                        msgCmd = msg.init('resourceMsg')
                        msgMessage = msgCmd.init('resMemX')
                        msgMessage.msg = "X"
                        msgBytes = msg.to_bytes()
                        payload = zmq.Frame(msgBytes)
                        identity = str(key).encode(encoding='utf-8')
                        self.notifier.send_multipart([identity,payload])
                        self.logger.info("XMem sent to [%d]" % (self.proc.pid))
                # self.proc.send_signal(signal.SIGUSR1)              
                time.sleep(1.0)
                if self.terminated.is_set(): break   
        except:
            self.logger.error("MemMonitorThread failure")
            traceback.print_exc() 
        self.logger.info("MemMonitor terminated")     
        
    def stop(self):
        self.running.clear()
        self.efd.increment()
        self.stopped.wait()
        
    def terminate(self):
        self.terminated.set() 
        self.efd.increment()
        if self.stopped.is_set():
            self.stopped.clear()
            self.running.set()     
