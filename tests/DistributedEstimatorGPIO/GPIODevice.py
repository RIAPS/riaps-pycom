# import riaps
from riaps.run.comp import Component
import logging
import random
import os
import threading
import zmq
import time

class GPIODeviceThread(threading.Thread):
    '''
    Inner GPIODevice thread
    '''
    def __init__(self,trigger,logger):
        threading.Thread.__init__(self)
        self.logger = logger
        self.active = threading.Event()
        self.active.clear()
        self.waiting = threading.Event()
        self.terminated = threading.Event()
        self.terminated.clear()
        self.trigger = trigger
        self.plug = None              # inside RIAPS port
        self.plug_identity = None
        self.logger.info('GPIODeviceThread _init()_ed')

    def get_identity(self,ins_port):
        if self.plug_identity is None:
            while True:
                if self.plug != None:
                    self.plug_identity = ins_port.get_plug_identity(self.plug)
                    break
                time.sleep(0.1)
        return self.plug_identity
    
    def run(self):
        self.logger.info('GPIODeviceThread starting')
        self.plug = self.trigger.setupPlug(self)    # Ask RIAPS port to make a plug (zmq socket) for this end
        self.poller = zmq.Poller()                  # Set up poller to wait for messages from either side
        self.poller.register(self.plug, zmq.POLLIN) # plug socket (connects to trigger port of parent device comp)
        while 1:
            self.active.wait(None)                  # Events to handle activation/termination
            if self.terminated.is_set(): break
            if self.active.is_set():                # If we are active
                socks = dict(self.poller.poll(1000.0))  # Run the poller: wait input from either side, timeout if none
                if len(socks) == 0:
                    # self.logger.info('IODeviceThread timeout')
                    pass
                if self.terminated.is_set(): break
                if self.plug in socks and socks[self.plug] == zmq.POLLIN:   # Input from the plug
                    msg = self.plug.recv_pyobj()
                    self.logger.info('IODeviceThread : msg = %s' % str(msg))
        self.logger.info('GPIODeviceThread ended')
               

    def activate(self):
        self.active.set()
        self.logger.info('GPIODeviceThread activated')
                    
    def deactivate(self):
        self.active.clear()
        self.logger.info('GPIODeviceThread deactivated')
    
    def terminate(self):
        self.active.set()
        self.terminated.set()
        self.logger.info('GPIODeviceThread terminating')

class GPIODevice(Component):
    def __init__(self):
        super(GPIODevice, self).__init__()
        self.logger.info("GPIOIODevice - starting")
        self.ioThread = None  # Cannot manipulate ports in constructor or start threads, use clock pulse 

    def on_clock(self):
        if self.ioThread == None: # First clock pulse
            self.ioThread = GPIODeviceThread(self.trigger,self.logger) # Inside port
            self.ioThread.start() # Start thread
            self.trigger.set_identity(self.ioThread.get_identity(self.trigger))
            self.trigger.activate()
        now = self.clock.recv_pyobj()   # Receive time (as float)
        self.clock.halt()               # Halt this timer (don't need it anymore)

    def __destroy__(self):
        self.logger.info("__destroy__")
        self.ioThread.deactivate()
        self.ioThread.terminate()
        self.ioThread.join()
        self.logger.info("__destroy__ed")
        
    def on_trigger(self):                       # Internally triggered operation 
        msg = self.trigger.recv_pyobj()         # Receive message from internal thread
        self.logger.info('on_trigger():%s' % msg)
        
    def on_blink(self):
        msg = self.blink.recv_pyobj()            # Receive response from echo server
        self.logger.info('on_blink():%s' % msg)
        if self.ioThread:
            self.trigger.send_pyobj(msg)            # Send it to the internal thread
