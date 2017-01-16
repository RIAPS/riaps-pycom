'''
Created on Oct 10, 2016

@author: riaps
'''
from .port import Port
import threading
import zmq
import time
from .exc import OperationError

class TimerThread(threading.Thread):
    def __init__(self,parent):
        threading.Thread.__init__(self)
        self.name = parent.instName
        self.context = parent.context
        if parent.period == 0:
            self.period = None
        else:
            self.period = parent.period * 0.001 # millisec
        self.active = threading.Event()
        self.active.clear()
        self.waiting = threading.Event()
        self.terminated = threading.Event()
        self.terminated.clear()
        
    def run(self):
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind('inproc://timer_' + self.name)
        while 1:
            self.active.wait(None)
            if self.terminated.is_set(): break
            if self.period:
                self.waiting.wait(self.period)
                if self.terminated.is_set(): break
                if self.active.is_set():
                    value = time.time()
                    self.socket.send_pyobj(value)
            else:
                pass
            
    def activate(self):
        self.active.set()
    
    def deactivate(self):
        self.active.clear()
    
    def terminate(self):
        self.terminated.set()
        
class TimPort(Port):
    '''
    classdocs
    '''

    def __init__(self, parentPart, portName, portSpec):
        '''
        Constructor
        '''
        super(TimPort,self).__init__(parentPart,portName)
        self.instName = self.parent.name + '.' + self.name
        self.period = portSpec["period"]
        self.thread = None

    def setup(self):
        self.thread = TimerThread(self)
        self.thread.start() 
    
    def setupSocket(self):
        assert self.instName == self.thread.name       
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect('inproc://timer_' + self.instName)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, u'')
        return ('tim',self.name)

    def activate(self):
        if self.thread != None:
            self.thread.activate()
        
    def deactivate(self):
        if self.thread != None:
            self.thread.deactivate()
        
    def terminate(self):
        if self.thread != None:
            self.thread.terminate()

    def getSocket(self):
        return self.socket
    
    def inSocket(self):
        return True
    
    def recv_pyobj(self):
        res = self.socket.recv_pyobj()
        return res
    
    def send_pyobj(self,msg):
        raise OperationError("attempt to send through a timer port")
    
    def getInfo(self):
        return ("tim",self.name,"*tick*")
