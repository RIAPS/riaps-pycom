from riaps.run.comp import Component
import logging #if we have a logger, is this necessary?
import threading
import time

import os # not sure why we need this. Its used to get the pid

import socket

class DensitySensorThread(threading.Thread):
    def __init__(self, port, gameServerIP):
        threading.Thread.__init__(self)
        self.port = port
        self.period = 2500
        self.active = threading.Event()
        self.waiting = threading.Event()
        self.terminated = threading.Event()
        self.terminated.clear()
        
        self.gameSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.gameServerIP = gameServerIP
    
    def run(self):
        self.plug = self.port.setupPlug(self) #I think this is basically to let the component poll its device ports...?
        # I think this is essentially a heartbeat and handles ctrl-c
        while 1:
            self.active.wait(None)#no clue
            if self.terminated.is_set():break #no clue
            self.waiting.wait(self.period)
            if self.terminated.is_set():break
            if self.active.is_set():
                value = time.time()
                self.plug.send_pyobj(value)
                
    def activate(self):
        self.active.set()
    
    def deactivate(self):
        self.active.clear()
    
    def terminate(self):
        self.terminated.set()
        
class DensitySensor(Component):
    def __init__(self,rate, gameServerIP):
        super(DensitySensor, self).__init__()
        self.pid = os.getpid()
        self.logger.info("Sensor(rate=%d) [%d]", rate, self.pid)
        self.DensitySensorThread = None #handle for thread once we make it
        self.gameServerIP = gameServerIP
        
    def on_clock(self):
        if self.DensitySensorThread == None:
            self.DensitySensorThread = DensitySensorThread(self.trigger, self.gameServerIP)          # Port object to talk to 
            self.DensitySensorThread.start()
            self.trigger.activate()        
        now = self.clock.recv_pyobj()   # Receive time (as float)
        self.logger.info('on_clock():%s',now)
        msg = (now,self.pid)        # Send (timestamp,value) 
        
        
        self.densityPort.send_pyobj(msg)

    def __destroy__(self):
        self.logger.info("__destroy__")
        
    def on_trigger(self):                   # Internally triggered op
        now = self.trigger.recv_pyobj()     # Receive time (as float)
        self.logger.info('on_trigger():%s',now)

    