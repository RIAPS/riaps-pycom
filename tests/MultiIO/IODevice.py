# import riaps
from riaps.run.comp import Component
from collections import deque
import logging
import random
import string
import os
import threading
import zmq
import time

def get_random_string(length):
    '''
    Generate a random string of specific length
    '''
    letters = string.ascii_lowercase
    res = ''.join(random.choice(letters) for i in range(length))
    return res
    
class IODeviceThread(threading.Thread):
    '''
    Inner IODevice thread
    '''
    def __init__(self,trigger,logger):
        threading.Thread.__init__(self)
        self.logger = logger
        self.active = threading.Event()
        self.active.clear()
        self.waiting = threading.Event()
        self.terminated = threading.Event()
        self.terminated.clear()
        self.trigger = trigger              # inside RIAPS port
        self.context = zmq.Context()
        self.plug = None
        self.past = deque()
        self.logger.info('IODeviceThread _init()_ed')

    def get_plug(self):
        return self.plug
    
    def run(self):
        self.logger.info('IODeviceThread[%d] starting' % self.ident)
        self.plug = self.trigger.setupPlug(self)    # Ask RIAPS port to make a plug (zmq socket) for this end
        self.poller = zmq.Poller()                  # Set up poller to wait for messages from either side
        self.poller.register(self.plug, zmq.POLLIN) # plug socket (connects to trigger port of parent device component)
        while 1:
            self.active.wait(None)                  # Events to handle activation/termination
            if self.terminated.is_set(): break
            if self.active.is_set():                # If we are active
                timeout = random.uniform(3000.0,5000.0)  # Random wait time
                socks = dict(self.poller.poll(timeout))  # Run the poller: wait for input from outer component thread or timeout
                if len(socks) == 0:
                    self.logger.info('IODeviceThread[%d] timeout' % self.ident)
                    if self.terminated.is_set(): break
                    message = get_random_string(8)      # Build random string
                    self.logger.info("IODeviceThread[%d] send = %s" % (self.ident,message))
                    self.plug.send_pyobj(message)       # Send random string to component thread
                    self.past.append(message)
                elif self.plug in socks and socks[self.plug] == zmq.POLLIN:   # Input from the plug
                    message = self.plug.recv_pyobj()    # Receive messages 
                    self.logger.info("IODeviceThread[%d] recv = %s" % (self.ident,message))
                    sent = self.past.popleft()
                    assert str(sent)[::-1] == message  
        self.logger.info('IODeviceThread ended')
               

    def activate(self):
        self.active.set()
        self.logger.info('IODeviceThread[%d] activated' % self.ident)
                    
    def deactivate(self):
        self.active.clear()
        self.logger.info('IODeviceThread[%d] deactivated' % self.ident)
    
    def terminate(self):
        self.active.set()
        self.terminated.set()
        self.logger.info('IODeviceThread[%d] terminating' % self.ident)

class IODevice(Component):
    def __init__(self,nthreads):
        super(IODevice, self).__init__()
        self.logger.info("IODevice - starting")
        self.nthreads = nthreads
        self.ioThreads = { }    # Map: plug_identity --> thread
        self.ioPlugs = { }

    def on_clock(self):
        if len(self.ioThreads) == 0: # First clock pulse
            for i in range(self.nthreads):
                thread = IODeviceThread(self.trigger,self.logger) # Inside port
                thread.start()
                self.ioThreads[thread.ident] = thread
                while True:
                    time.sleep(0.1)
                    plug = thread.get_plug()
                    if plug != None:            # Retrieve the 'plug' of the inner thread
                        identity = self.trigger.get_plug_identity(plug) # Retrieve the identity of the thread's plug 
                        self.ioPlugs[identity] = thread # Map the plug's identity to the inner thread 
                        break
            self.trigger.activate()
        now = self.clock.recv_pyobj()   # Receive time (as float)
        self.clock.halt()               # Halt this timer (don't need it anymore)

    def __destroy__(self):
        self.logger.info("__destroy__")
        for _ident,thread in self.ioThreads.items():
            thread.deactivate()
            thread.terminate()
            thread.join()
        self.logger.info("__destroy__ed")
        
    def on_trigger(self):                       # Internally triggered operation 
        msg = self.trigger.recv_pyobj()         # Receive message from an inner thread
       # Each plug (of an inner thread) has an identity that can be retrieved after receiving the message 
        src_plug_id = self.trigger.get_identity()   
        src_thread_id = self.ioPlugs[src_plug_id].ident 
        self.logger.info('on_trigger(): from %d recv = %s' % (src_thread_id,msg))
        msg_out = (src_plug_id, msg)                # We pass along the identity (and we will get it back from the the echo server)
        self.echo.send_pyobj(msg_out)               # Send it to the echo server
        
    def on_echo(self):
        (dst_plug_id,msg) = self.echo.recv_pyobj()    # Receive response from echo server (including the sender's identity)
        dst_thread_id = self.ioPlugs[dst_plug_id].ident
        self.logger.info('on_echo(): to %d %s' % (dst_thread_id,msg))
        # Before sending the message we have to set the identity - this will ensure that it gets sent to the correct thread
        self.trigger.set_identity(dst_plug_id)  
        self.trigger.send_pyobj(msg)            # Send it to the internal thread
