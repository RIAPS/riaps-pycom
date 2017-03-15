'''
Created on Jan 9, 2017

@author: riaps
'''
from .port import Port
import threading
import zmq
import time
from .exc import OperationError
from enum import Enum

# Example insider thread (1 sec ticker)
class InsThread(threading.Thread):
    def __init__(self,parent):
        threading.Thread.__init__(self)
        self.name = parent.instName
        self.parent = parent
        self.context = parent.context
        self.period = 1.0 
        self.active = threading.Event()
        self.active.clear()
        self.waiting = threading.Event()
        self.terminated = threading.Event()
        self.terminated.clear()
        
    def run(self):
        self.plug = self.parent.setupPlug(self)
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
        
class InsPort(Port):
    '''
    classdocs
    '''
        
    def __init__(self, parentPart, portName, portSpec):
        '''
        Constructor
        '''
        super(InsPort,self).__init__(parentPart,portName)
        self.instName = self.parent.name + '.' + self.name
        self.spec = portSpec["spec"]
        self.thread = None

    def setup(self):
        if self.spec == 'default':
            self.thread = InsThread(self)
            self.thread.start()
        else:
            pass 
    
    def setupSocket(self):
        self.socket = self.context.socket(zmq.PAIR)
        self.socket.connect('inproc://inside_' + self.instName)
        return ('ins',self.name)
    
    def setupPlug(self,thread):
        # Must not be called from the main thread
        assert thread != threading.main_thread()
        if self.thread != None:
            if self.thread != thread:
                raise OperationError('default inside thread already running on %s' % self.instName)
        else:
            self.thread = thread
        self.plug = self.context.socket(zmq.PAIR)
        self.plug.bind('inproc://inside_' + self.instName)
        return self.plug

    def activate(self):
        if self.thread and hasattr(self.thread,'activate'):
            self.thread.activate()
        
    def deactivate(self):
        if self.thread and hasattr(self.thread,'deactivate'):
            self.thread.deactivate()
        
    def terminate(self):
        if self.thread and hasattr(self.thread,'terminate'):
            self.thread.terminate()

    def getSocket(self):
        return self.socket
    
    def inSocket(self):
        return True
    
    def getContext(self):
        return self.context

    def recv_pyobj(self):
        res = self.socket.recv_pyobj()
        return res
    
    def send_pyobj(self,msg):
        try:
            self.socket.send_pyobj(msg)
        except ZMQError as e:
            if e.errno == zmq.EAGAIN:
                return False
            else:
                raise
        return True
    
    def getInfo(self):
        return ("ins",self.name,self.kind)
