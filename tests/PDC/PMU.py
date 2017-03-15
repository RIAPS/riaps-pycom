# import riaps
from riaps.run.comp import Component
import logging
import random
import os
import threading
import zmq
import time
from pypmu import pdc

    
class PMUThread(threading.Thread):
    def __init__(self, component):
        threading.Thread.__init__(self)
        self.port = component.queue
        self.active = threading.Event()
        self.active.clear()
        self.waiting = threading.Event()
        self.terminated = threading.Event()
        self.terminated.clear()
        self.component = component
        self.pdc = None
    
    def run(self):
        self.plug = self.port.setupPlug(self)             # Ask parent port to make a plug for this end
        
        if self.terminated.is_set(): return
        
        self.active.wait()
        self.pdc = pdc.Pdc(pmu_ip=self.component.pmu_ip, 
                             pmu_port=self.component.pmu_port)
        self.pdc.run()
        self.pdc.start()
        
        while 1:
            if self.terminated.is_set():
                self.pdc.quit() 
                break
    
            if not self.active.is_set():
                self.pdc.stop()
                self.active.wait()
                self.pdc.start()
            
            data = self.pdc.get() 
            self.plug.send_pyobj(data)
    
    def activate(self):
        self.active.set()
    
    def deactivate(self):
        self.active.clear()
    
    def terminate(self):
        self.terminated.set()

class PMU(Component):
    def __init__(self, pmu_ip, pmu_port):
        super().__init__()
        self.logger.setLevel(logging.DEBUG)
        self.pid = os.getpid()
        self.pmu_ip = pmu_ip
        self.pmu_port = pmu_port
        self.logger.info("PMU @%s:%d [%d]", pmu_ip, pmu_port, self.pid)
        self.pmuThread = None                    # Cannot manipulate ports in constructor or start threads 

    def on_clock(self):
        now = self.clock.recv_pyobj()   # Receive time (as float)
        self.logger.info('on_clock():%s',now)
        if self.pmuThread == None:
            self.pmuThread = PMUThread(self)           
            self.pmuThread.start()
            self.queue.activate()
        
    def __destroy__(self):
        self.logger.info("__destroy__")
        
    def on_queue(self):                   # Internally triggered op
        dataFrame = self.queue.recv_pyobj()     # Receive time (as float)
        self.logger.info('on_queue()') 
        self.pmuData.send_pyobj(dataFrame)
