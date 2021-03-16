# import riaps
from riaps.run.comp import Component
import logging
import random
import os
import threading
import zmq
import time

class IODeviceThread(threading.Thread):
    '''
    Inner IODevice thread
    '''
    def __init__(self,trigger,port,logger):
        threading.Thread.__init__(self)
        self.logger = logger
        self.active = threading.Event()
        self.active.clear()
        self.waiting = threading.Event()
        self.terminated = threading.Event()
        self.terminated.clear()
        self.trigger = trigger              # inside RIAPS port
        self.port = port                    # port number for socket to connect to connect to console client
        self.plug = None 
        self.plug_identity = None
        self.context = zmq.Context()
        self.cons = self.context.socket(zmq.REP)    # Create zmq REP socket 
        self.cons.bind("tcp://*:%s" % self.port)
        self.logger.info('IODeviceThread _init()_ed')
    
    def get_identity(self,ins_port):
        if self.plug_identity is None:
            while True:
                if self.plug != None:
                    self.plug_identity = ins_port.get_plug_identity(self.plug)
                    break
                time.sleep(0.1)
        return self.plug_identity
    
    def run(self):
        self.logger.info('IODeviceThread starting')
        self.plug = self.trigger.setupPlug(self)    # Ask RIAPS port to make a plug (zmq socket) for this end
        self.poller = zmq.Poller()                  # Set up poller to wait for messages from either side
        self.poller.register(self.cons, zmq.POLLIN) # console socket (connects to console client)
        self.poller.register(self.plug, zmq.POLLIN) # plug socket (connects to trigger port of parent device comp)
        while 1:
            self.active.wait(None)                  # Events to handle activation/termination
            if self.terminated.is_set(): break
            if self.active.is_set():                # If we are active
                socks = dict(self.poller.poll(5000.0))  # Run the poller: wait input from either side, timeout if none
                if len(socks) == 0:
                    self.logger.info('IODeviceThread timeout')
                if self.terminated.is_set(): break
                if self.cons in socks and socks[self.cons] == zmq.POLLIN:   # Input from the console
                    message = self.cons.recv_pyobj()
                    self.plug.send_pyobj(message)                           # Send it to the plug
                if self.plug in socks and socks[self.plug] == zmq.POLLIN:   # Input from the plug
                    message = self.plug.recv_pyobj()
                    self.cons.send_pyobj(message)                           # Send it to the console
        self.logger.info('IODeviceThread ended')
               

    def activate(self):
        self.active.set()
        self.logger.info('IODeviceThread activated')
                    
    def deactivate(self):
        self.active.clear()
        self.logger.info('IODeviceThread deactivated')
    
    def terminate(self):
        self.active.set()
        self.terminated.set()
        self.logger.info('IODeviceThread terminating')

class IODevice(Component):
    def __init__(self,port):
        super(IODevice, self).__init__()
        self.logger.info("IODevice - starting")
        self.port = port
        self.IODeviceThread = None  # Cannot manipulate ports in constructor or start threads, use clock pulse 

    def on_clock(self):
        if self.IODeviceThread == None: # First clock pulse
            self.IODeviceThread = IODeviceThread(self.trigger,self.port,self.logger) # Inside port, external zmq port
            self.IODeviceThread.start() # St
            self.trigger.set_identity(self.IODeviceThread.get_identity(self.trigger))
            self.trigger.activate()
        now = self.clock.recv_pyobj()   # Receive time (as float)
        self.clock.halt()               # Halt this timer (don't need it anymore)

    def __destroy__(self):
        self.logger.info("__destroy__")
        self.IODeviceThread.deactivate()
        self.IODeviceThread.terminate()
        self.IODeviceThread.join()
        self.logger.info("__destroy__ed")
        
    def on_trigger(self):                       # Internally triggered operation (
        msg = self.trigger.recv_pyobj()         # Receive message from internal thread
        self.logger.info('on_trigger():%s' % msg)
        self.echo.send_pyobj(msg)               # Send it to the echo server
        
    def on_echo(self):
        msg = self.echo.recv_pyobj()            # Receive response from echo server
        self.logger.info('on_echo():%s' % msg)
        self.trigger.send_pyobj(msg)            # Send it to the internal thread
