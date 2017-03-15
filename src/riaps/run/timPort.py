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
            self.periodic = False
        else:
            self.period = parent.period * 0.001 # millisec
            self.periodic = True
        self.delay = None
        self.active = threading.Event()
        self.active.clear()
        self.waiting = threading.Event()
        self.waiting.clear()
        self.terminated = threading.Event()
        self.terminated.clear()
        self.started = threading.Event()
        self.started.clear()
        
    def run(self):
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind('inproc://timer_' + self.name)     
        while 1:
            self.active.wait(None)                  # Wait for activation
            if self.terminated.is_set(): break      # If terminated, we exit
            if self.periodic:                       # Periodic timer
                self.started.wait(None)              
                self.waiting.wait(self.period)      # Wait for period
                if self.terminated.is_set(): break  
                if self.waiting.is_set():           # Period was cancelled
                    self.waiting.clear()            # Start next period, but do not send tick
                    continue
                if self.active.is_set():            # Send tick (if active)
                    value = time.time()
                    self.socket.send_pyobj(value)
            else:                                   # One shot timer
                while 1:
                    self.started.wait(None)         # Wait for start
                    assert self.delay != None and self.delay > 0.0
                    self.waiting.wait(self.delay)   # Wait for the delay
                    if self.terminated.is_set() : break  
                    self.started.clear()            # We are not started anymore
                    if self.waiting.is_set():       # Delay was cancelled
                        self.waiting.clear()        # Enable next waiting, but  do not send tick
                        continue
                    if self.active.is_set():        # Send tick (if active)
                        value = time.time()
                        self.socket.send_pyobj(value)
            
    def activate(self):
        '''
        Activate the timer port
        '''
        self.active.set()
        if self.periodic:
            self.started.set()
    
    def deactivate(self):
        '''
        Deactivate the timer port
        '''
        self.active.clear()
    
    def terminate(self):
        '''
        Terminate the timer 
        '''
        self.terminated.set()
    
    def getPeriod(self):
        ''' 
        Read out the period
        '''
        return self.period
    
    def setPeriod(self,_period):
        ''' 
        Set the period - will be changed after the next firing.
        Period must be positive
        '''
        assert type(_period) == float and _period > 0.0  
        self.period = _period
    
    def getDelay(self):
        '''
        Get the current delay (for sporadic timer)
        '''
        return self.delay
    
    def setDelay(self,_delay):
        '''
        Set the current delay (for sporadic timer)
        '''
        assert type(_delay) == float and _delay > 0.0  
        self.delay = _delay
        
    def launch(self):
        '''
        Launch (start) the sporadic timer
        '''
        self.started.set()
    
    def running(self):
        '''
        Returns True if the timer is running
        '''
        return self.started.is_set()
    
    def cancel(self):
        '''
        Cancel the sporadic timer
        '''
        self.waiting.set()
    
    def halt(self):
        '''
        Halt the timer
        '''
        self.started.clear()
        
class TimPort(Port):
    '''
    Timer port
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
        '''
        Activate the timer port
        '''
        if self.thread != None:
            self.thread.activate()
        
    def deactivate(self):
        '''
        Deactivate the timer port
        '''
        if self.thread != None:
            self.thread.deactivate()
        
    def terminate(self):
        '''
        Terminate the timer 
        '''
        if self.thread != None:
            self.thread.terminate()

    def getPeriod(self):
        ''' 
        Read the period of the periodic timer
        '''
        if self.thread != None:
            return self.thread.getPeriod()
        else:
            return None
    
    def setPeriod(self,_period):
        ''' 
        Set the period - will be changed after the next firing.
        Period must be positive
        '''
        if not (type(_period) == float and _period > 0.0):
            raise OperationError("invalid argument %s" % str(_period))
        if self.thread != None: 
            self.thread.setPeriod(_period)
    
    def getDelay(self):
        '''
        Get the current delay (for sporadic timer)
        '''
        if self.thread != None: 
            return self.thread.getDelay()
        else:
            return None
    
    def setDelay(self,_delay):
        '''
        Set the current delay (for sporadic timer)
        '''
        if not (type(_delay) == float and _delay > 0.0):
            raise OperationError("invalid argument %s" % str(_delay))
        if self.thread != None: 
            self.thread.setDelay(_delay)
        
    def launch(self):
        '''
        Launch (start) the sporadic timer
        '''
        if self.thread != None: 
            self.thread.launch()

    def running(self):
        '''
        Returns True if the timer is running
        '''
        if self.thread != None:
            return self.thread.running()
        else:
            return None

    def cancel(self):
        '''
        Cancel the sporadic timer
        '''
        if self.thread != None: 
            self.thread.cancel()
    
    def halt(self):
        '''
        Halt the timer
        '''
        if self.thread != None: 
            self.thread.halt()

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
