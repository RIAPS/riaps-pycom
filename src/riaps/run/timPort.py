'''
Created on Oct 10, 2016

@author: riaps
'''
from .port import Port,PortScope,PortInfo
import threading
import zmq
import time
import logging
import struct
from enum import Enum,auto
from .exc import OperationError


class TimerThread(threading.Thread):

    class Command(Enum):        # Timer command codes
        TERMINATE   = auto()            
        ACTIVATE    = auto()          
        DEACTIVATE  = auto()            
        START       = auto()           
        CANCEL      = auto()
        HALT        = auto()
        
    def __init__(self, parent):
        threading.Thread.__init__(self,daemon=False)
        self.logger = logging.getLogger(__name__)
        self.name = parent.instName
        self.context = parent.context
        if parent.period == 0:
            self.period = None
            self.periodic = False
        else:
            self.period = parent.period * 0.001  # millisec
            self.periodic = True
        self.delay = None
        self.socket = None
        self._ready = threading.Event()         # Timer thread ready to accept commands
        self._ready.clear()
        self._running = False                   # Timer ('counter') is running

    
        # self.active = threading.Event()
        # self.active.clear()
        # self.waiting = threading.Event()
        # self.waiting.clear()
        # self.terminated = threading.Event()
        # self.terminated.clear()
        # self.started = threading.Event()
        # self.started.clear()
        
    def ready(self):
        return self._ready
    
    def cmdError(self,where,cmd):
        self.logger.error("Timer %s:%s: cmd = %r" % (self.name,where,cmd))
    
    def waitFor(self,timeout=None):
        res = self.poller.poll(timeout)
        if len(res) == 0:
            return None
        else:          
            (s,_m) = res[0]
            return s.recv_pyobj()
        
    def run(self):
        self.socket = self.context.socket(zmq.PAIR)  # PUB
        self.socket.bind('inproc://timer_' + self.name)
        self.poller = zmq.Poller()
        self.poller.register(self.socket,zmq.POLLIN)
        self._ready.set()                       # Ready to accept commands
        self.timeout = None
        self.active = False
        self._running = False
        self.skip = False
        self.last = None
        while 1:
            msg = self.waitFor(self.timeout)
            if msg == TimerThread.Command.TERMINATE: break  # Terminated
            elif msg == None:                               # Timeout
                if not self.active:                         # Wait if not active
                    self.timeout = None
                    continue
                self.last = time.time()
                if self._running:
                    if self.periodic and self.skip:
                        self.skip = False
                    else:
                        self.socket.send_pyobj(self.last)          
                if self.periodic:           # Periodic: again
                    self.timeout = int(self.period * 1000)
                    pass                              
                else:                       # Sporadic: wait for next command
                    self._running = False
                    self.timeout = None
                continue
            elif msg == TimerThread.Command.ACTIVATE:
                self.active = True
                self.last = None
            elif msg == TimerThread.Command.DEACTIVATE:
                self.active = False
                self.timeout = None
                self.last = None
            elif msg == TimerThread.Command.START:
                if self.active: 
                    if self.periodic:
                        self.timeout = int(self.period * 1000)
                    else:
                        self.timeout = int(self.delay * 1000)
                    self._running = True
                else:                           # Not active 
                    self.cmdError('not active',msg)
                    continue
            elif msg == TimerThread.Command.CANCEL:
                if self.periodic:
                    if self.last != None:       # Skip next firing
                        delay = self.last + self.period - time.time()
                        self.timeout = int(delay * 1000) 
                        self.skip = True
                else:
                    self._running = False
                    self.timeout = None
            elif msg == TimerThread.Command.HALT:
                self.timeout = None
                self._running = False
            else:
                self.cmdError('loop',msg)
        
            
            # self.active.wait(None)              # Wait for activation
            # if self.terminated.is_set(): break  # If terminated, we exit
            # if self.periodic:                   # Periodic timer
            #     while 1:
            #         self.started.wait(None)  
            #         if self.terminated.is_set(): break        
            #         cancelled = self.waiting.wait(self.period)  # Wait for period
            #         if self.terminated.is_set(): break  
            #         if cancelled:               # Period was cancelled
            #             self.waiting.clear()    # Start next period, but do not send tick
            #             continue
            #         if self.active.is_set() and self.started.is_set():  # Send tick (if active)
            #             value = time.time()
            #             self.socket.send_pyobj(value)
            # else:  # One shot timer
            #     while 1:
            #         self.started.wait(None)     # Wait for start
            #         if self.terminated.is_set() or not self.active.is_set(): break
            #         assert self.delay != None and self.delay > 0.0
            #         cancelled = self.waiting.wait(self.delay)  # Wait for the delay
            #         if self.terminated.is_set(): break  
            #         self.started.clear()        # We are not started anymore
            #         if cancelled:               # Delay was cancelled
            #             self.waiting.clear()    # Enable next waiting, but  do not send tick
            #             continue
            #         if self.active.is_set():    # Send tick (if active)
            #             value = time.time()
            #             self.socket.send_pyobj(value)
            # if self.terminated.is_set(): break  # Terminated
        pass
            
    # def activate(self):
    #     '''
    #     Activate the timer port
    #     '''
    #     self.socket.send_pyobj(TimerThread.Command.ACTIVATE)
    #     if self.periodic:
    #         self.socket.send_pyobj(TimerThread.Command.START)
    
    # def deactivate(self):
    #     '''
    #     Deactivate the timer port
    #     '''
    #     self.socket.send_pyobj(TimerThread.Command.DEACTIVATE)
    
    # def terminate(self):
    #     '''
    #     Terminate the timer 
    #     '''
    #     self.socket.send_pyobj(TimerThread.Command.TERMINATE)
    
    def getPeriod(self):
        ''' 
        Read out the period
        '''
        return self.period
    
    def setPeriod(self, _period):
        ''' 
        Set the period (for periodic timer).
        Takes effect after the next firing.
        '''
        assert type(_period) == float and _period > 0.0  
        self.period = _period
    
    def getDelay(self):
        '''
        Get the current delay (for sporadic timer)
        '''
        return self.delay
    
    def setDelay(self, _delay):
        '''
        Set the current delay (for sporadic timer)
        '''
        assert type(_delay) == float and _delay > 0.0  
        self.delay = _delay
        
    # def launch(self):
    #     '''
    #     Launch the timer
    #     '''
    #     self.socket.send_pyobj(TimerThread.Command.START)
    
    def running(self):
        '''
        Returns True if the timer is running
        '''
        return self._running
       
    # def cancel(self):
    #     '''
    #     Cancel the sporadic timer
    #     '''
    #     self.socket.send_pyobj(TimerThread.Command.CANCEL)
    #     # if self.started.is_set():
    #     #     self.waiting.set()  # Go to wait mode if started
    #     # else:
    #     #     pass  # Ignore if not started
        
    # def halt(self):
    #     '''
    #     Halt the timer
    #     '''
    #     self.socket.send_pyobj(TimerThread.Command.HALT)
    #     # self.started.clear()

        
class TimPort(Port):
    '''
    Timer port
    '''

    def __init__(self, parentPart, portName, portSpec):
        '''
        Constructor
        '''
        super(TimPort, self).__init__(parentPart, portName, portSpec)
        self.logger = logging.getLogger(__name__)
        self.instName = self.parent.name + '.' + self.name
        self.period = portSpec["period"]
        self.deadline = portSpec.get("deadline",0) * 0.001  # msec
        self.thread = None
        self.info = None

    def setup(self):
        self.thread = TimerThread(self)
        self.thread.start() 
        self.thread.ready().wait()          # Wait until thread is ready to receive commands
    
    def setupSocket(self, owner):
        self.setOwner(owner)
        assert self.instName == self.thread.name       
        self.socket = self.context.socket(zmq.PAIR)  # SUB
        self.socket.connect('inproc://timer_' + self.instName)
        # self.socket.setsockopt_string(zmq.SUBSCRIBE, u'')
        self.info = PortInfo(portKind='tim', portScope=PortScope.INTERNAL, portName=self.name, 
                             msgType='tick', portHost='', portNum=-1)
        return self.info

    def reset(self):
        pass
    
    def activate(self):
        '''
        Activate the timer port
        '''
        if self.thread != None:
            self.socket.send_pyobj(TimerThread.Command.ACTIVATE)
            if self.thread.getPeriod():             # Periodic timer
                self.socket.send_pyobj(TimerThread.Command.START)
        
    def deactivate(self):
        '''
        Deactivate the timer port
        '''
        if self.thread != None:
            self.socket.send_pyobj(TimerThread.Command.DEACTIVATE)
        
    def terminate(self):
        '''
        Terminate the timer 
        '''
        if self.thread != None:
            self.logger.info("terminating")
            self.socket.send_pyobj(TimerThread.Command.TERMINATE)
            # self.thread.terminate()
            self.thread.join()
            self.logger.info("terminated")

    def getPeriod(self):
        ''' 
        Read the period of the periodic timer
        '''
        if self.thread != None:
            return self.thread.getPeriod()
        else:
            return None
    
    def setPeriod(self, _period):
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
    
    def setDelay(self, _delay):
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
            # self.thread.launch()
            self.socket.send_pyobj(TimerThread.Command.START)

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
            # self.thread.cancel()
            self.socket.send_pyobj(TimerThread.Command.CANCEL)
    
    def halt(self):
        '''
        Halt the timer
        '''
        if self.thread != None: 
            # self.thread.halt()
            self.socket.send_pyobj(TimerThread.Command.HALT)

    def getSocket(self):
        return self.socket
    
    def inSocket(self):
        return True
    
    def recv_pyobj(self):
        res = self.socket.recv_pyobj()
        return res
    
    def send_pyobj(self, msg):
        raise OperationError("attempt to send through a timer port")
    
    def recv(self):
        '''
        Receive time stamp (a float) as a byte array
        '''
        value = self.socket.recv_pyobj()
        res = bytearray(struct.pack("f", value))
        return res
    
    def send(self):
        raise OperationError("attempt to send through a timer port")
    
    def getInfo(self):
        return self.info
    
