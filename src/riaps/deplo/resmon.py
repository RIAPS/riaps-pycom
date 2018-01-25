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
from riaps.run.exc import *
from riaps.utils.sudo import riaps_sudo
from riaps.utils.config import Config
from butter.eventfd import Eventfd
import traceback
from pwd import getpwnam  
from pyroute2 import DQuotSocket

class CPUMonitorThread(threading.Thread):
    '''
    Thread for monitoring an actor and enforcing resource limits.
    '''
    def __init__(self,interval,usage):
        threading.Thread.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.interval = interval    # sec
        self.usage = usage          # % INT
        self.terminated = threading.Event() # Set when the monitor is to be terminated
        self.terminated.clear()
        self.running = threading.Event()    # Cleared when the monitor is not to run
        self.running.set()
        self.stopped = threading.Event()    # Set if the monitor is stoppped
        self.stopped.clear()
        self.alive = False
    
    def setup(self,proc):
        self.proc = proc
        self.mon = psutil.Process(proc.pid)
    
    def is_running(self):
        return self.alive
    
    def restart(self):
        self.stopped.clear()
        self.running.set()

    def run(self):
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
            self.logger.info("SIGXCPU to [%d]? %d > %d in %f" % (self.proc.pid,current,self.usage,self.interval))
            if current > self.usage:
                # print ("SIGXCPU sent")
                self.proc.send_signal(signal.SIGXCPU)
                time.sleep(1.0)
                # self.mon = psutil.Process(self.proc.pid)
                # current = self.mon.cpu_percent(self.interval)           
        
    def stop(self):
        self.running.clear()
        self.stopped.wait()
        
    def terminate(self):
        self.terminated.set()
    
class MemMonitorThread(threading.Thread):
    def __init__(self,efd,usage):
        threading.Thread.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.efd = efd
        self.usage = usage
        self.terminated = threading.Event() # Set when the monitor is to be terminated
        self.terminated.clear()
        self.running = threading.Event()    # Cleared when the monitor is not to run
        self.running.set()
        self.stopped = threading.Event()    # Set if the monitor is stoppped
        self.stopped.clear()
        self.alive = False
    
    def setup(self,proc):
        self.proc = proc

    def is_running(self):
        return self.alive
    
    def restart(self):
        self.stopped.clear()
        self.running.set()

    def run(self):
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
                if not self.running.is_set(): continue
                if self.terminated.is_set(): break
                self.logger.info("MemMonitor[%d] mem limit %d exceeded - %s" % (self.proc.pid,self.usage,str(current)))
                self.logger.info('SIGUSR1 to [%d]' % (self.proc.pid))
                self.proc.send_signal(signal.SIGUSR1)
                time.sleep(1.0)   
        except:
            self.logger.error("MemMonitorThread failure")
            traceback.print_exc()      
        
    def stop(self):
        self.running.clear()
        self.efd.increment()
        self.stopped.wait()
        
    def terminate(self):
        self.terminated.set() 
        self.efd.increment()        

class SpcMonitorThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.terminated = threading.Event() # Set when the monitor is to be terminated
        self.terminated.clear()
        self.running = threading.Event()    # Cleared when the monitor is not to run
        self.running.set()
        self.stopped = threading.Event()    # Set if the monitor is stoppped
        self.stopped.clear()
        self.alive = False
        self.procs = { }
        self.rlock = RLock()
    
    def addProc(self,proc):
        with self.rlock:
            uids = psutil.Process(proc.pid).uids()
            uid  = uids.real    # Real UID
            if uid in self.procs:
                self.procs[uid] = self.procs[uid] + [proc]
            else:
                self.procs[uid] = [proc]
        
    def delProc(self,proc):
        uids = psutil.Process(proc.pid).uids()
        uid  = uids.real    # Real UID
        if uid in self.procs:
            del self.procs[uid]

    def is_running(self):
        return self.alive
    
    def restart(self):
        self.stopped.clear()
        self.running.set()

    def run(self):
        self.alive = True
        self.logger.info("SpcMonitor started")
        time.sleep(0.001)
        try:
            while True:
                if not self.running.is_set():
                    self.stopped.set()
                    self.running.wait()
                if self.terminated.is_set(): break
                with DQuotSocket() as ds:
                    self.logger.info("waiting on DQuotSocket")
                    for msg in ds.get():
                        uid = msg.get_attr('QUOTA_NL_A_EXCESS_ID')
                        with self.rlock:
                            if uid in self.procs:
                                self.logger.info("SPC limit exceeded by uid = %d" % (uid))
                                for proc in self.procs[uid]:
                                    self.logger.info('SIGUSR2 to [%d]' % (proc.pid))
                                    proc.send_signal(signal.SIGUSR2)
                                    time.sleep(0.1)   
                if not self.running.is_set(): continue
                if self.terminated.is_set(): break
        except:
            self.logger.error("SpcMonitorThread failure")
            traceback.print_exc()      
        
    def stop(self):
        self.running.clear()
        self.efd.increment()
        self.stopped.wait()
        
    def terminate(self):
        self.terminated.set() 
        self.efd.increment()   
