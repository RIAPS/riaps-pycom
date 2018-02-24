'''
Resource monitors

Created on Nov 23, 2017

@author: riaps
'''

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
import socket
import zmq
from zmq import devices
from zmq.error import ZMQError

from riaps.consts.defs import *
from riaps.run.exc import *
from riaps.proto import deplo_capnp
from riaps.utils.sudo import riaps_sudo
from riaps.utils.config import Config

class SpcMonitorThread(threading.Thread):
    def __init__(self, parent):
        threading.Thread.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.parent = parent
        self.context = self.parent.context
        self.terminated = threading.Event()  # Set when the monitor is to be terminated
        self.terminated.clear()
        self.running = threading.Event()  # Cleared when the monitor is not to run
        self.running.set()
        self.stopped = threading.Event()  # Set if the monitor is stoppped
        self.stopped.clear()
        self.alive = False
        self.procs = { }
        self.rlock = RLock()
        self.notifier = None
        self.notifierPort = None
        self.devices = { }
        self.pid2Key = { }
        self.ds = None
    
    def addProc(self,proc):
        with self.rlock:
            uids = psutil.Process(proc.pid).uids()
            uid  = uids.real    # Real UID
            if uid in self.procs:
                self.procs[uid] = self.procs[uid] + [proc]
            else:
                self.procs[uid] = [proc]
            self.pid2Key[proc.pid] = '???'
        
    def delProc(self,proc):
        uids = psutil.Process(proc.pid).uids()
        uid  = uids.real    # Real UID
        with self.rlock:
            if uid in self.procs:
                del self.procs[uid]
    
    def addClientDevice(self,appName,actorName,device,proc):
        while self.notifierPort == None:
            time.sleep(0.1)
        with self.rlock:
            device.connect_in('tcp://127.0.0.1:%i' % self.notifierPort)
            key = str(appName) + "." + str(actorName)
            self.devices[key] = device
            self.pid2Key[proc.pid] = key
            
    def is_running(self):
        return self.alive
    
    def restart(self):
        self.stopped.clear()
        self.running.set()

    def run(self):
        self.logger.info("SpcMonitor started")
        self.alive = True
        self.notifier = self.context.socket(zmq.ROUTER)
        # self.notifier.setsockopt(zmq.SNDTIMEO,const.deplEndpointSendTimeout)
        self.notifierPort = self.notifier.bind_to_random_port('tcp://127.0.0.1') 
        self.alive = True
        while True:
            try:
                self.ds = DQuotSocket()
                self.ds.settimeout(const.spcMonitorTimeout)     # Timeout on quota system netlink socket @ 10 sec
                if not self.running.is_set():
                    self.stopped.set()
                    self.running.wait()
                if self.terminated.is_set(): break
                self.logger.info("waiting on DQuotSocket")
                try:
                    for msg in self.ds.get():
                        uid = msg.get_attr('QUOTA_NL_A_EXCESS_ID')
                        with self.rlock:
                            if uid in self.procs:
                                self.logger.info("SPC limit exceeded by uid = %d" % (uid))
                                for proc in self.procs[uid]:
                                    # self.logger.info('SIGUSR2 to [%d]' % (proc.pid))
                                    # proc.send_signal(signal.SIGUSR2)
                                    if proc.pid not in self.pid2Key:
                                        self.logger.error("Invalid pid %i w/o key" % (proc.pid))
                                        continue
                                    key = self.pid2Key[proc.pid]
                                    msg = deplo_capnp.ResMsg.new_message()
                                    msgMessage = msg.init('resSpcX')
                                    msgMessage.msg = "X"
                                    msgBytes = msg.to_bytes()
                                    payload = zmq.Frame(msgBytes)
                                    identity = str(key).encode(encoding='utf-8')
                                    self.notifier.send_multipart([identity,payload])
                                    self.logger.info("XSpc sent to [%d]" % (proc.pid))
                                    time.sleep(0.1)
                except socket.timeout:
                    self.ds.close()
                    self.ds = None
                    if self.terminated.is_set(): break
                    continue
                except:
                    self.logger.error("SpcMonitorThread exception")
                    raise
                if not self.running.is_set(): continue
                if self.terminated.is_set(): break
            except:
                self.logger.error("SpcMonitorThread failure")
                # traceback.print_exc()
                break
        if self.ds != None: 
            self.ds.close()
        self.ds = None
        self.logger.info("SpcMonitor terminated")     
        
    def stop(self):
        self.running.clear()
        self.stopped.wait()
        
    def terminate(self):
        self.logger.info("terminating")     
        if self.ds != None:
            self.ds.settimeout(0.1)
        self.terminated.set() 
        if self.stopped.is_set():
            self.stopped.clear()
            self.running.set()
        self.logger.info("terminated") 

           
