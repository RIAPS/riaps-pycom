# import riaps
from riaps.run.comp import Component
import logging
import random
import os
import threading
import zmq
import time

class SensorThread(threading.Thread):
    def __init__(self,port):
        threading.Thread.__init__(self)
        self.port = port
        self.period = 2500.0                            # 2.5 sec period
        self.active = threading.Event()
        self.active.clear()
        self.waiting = threading.Event()
        self.terminated = threading.Event()
        self.terminated.clear()
    
    def run(self):
        self.plug = self.port.setupPlug(self)             # Ask parent port to make a plug for this end 
        while 1:
            self.active.wait(None)
            if self.terminated.is_set(): break
            self.waiting.wait(self.period)
            if self.terminated.is_set(): break
            if self.active.is_set():
                value = time.time()
                self.plug.send_pyobj(value)
    
    def activate(self):
        self.active.set()
    
    def deactivate(self):
        self.active.clear()
    
    def terminate(self):
        self.terminated.set()

class Sensor(Component):
    def __init__(self,rate):
        super(Sensor, self).__init__()
        self.pid = os.getpid()
        self.myValue = (10.0 * random.random()) - 5.0
        self.logger.info("Sensor(rate=%d)[%d]",rate,self.pid)
        self.sensorThread = None                    # Cannot manipulat ports in constructr or start threads 

    def on_clock(self):
        if self.sensorThread == None:
            self.sensorThread = SensorThread(self.trigger)          # Port object to talk to 
            self.sensorThread.start()
            self.trigger.activate()
        now = self.clock.recv_pyobj()   # Receive time (as float)
        self.logger.info('on_clock():%s',now)
        msg = (now,self.myValue)        # Send (timestamp,value) 
        self.sensorReady.send_pyobj(msg)

    def __destroy__(self):
        self.logger.info("__destroy__")
        
    def on_trigger(self):                   # Internally triggered op
        now = self.trigger.recv_pyobj()     # Receive time (as float)
        self.logger.info('on_trigger():%s',now)
