'''
Created on Jan 9, 2017

@author: riaps
'''
from .port import Port,PortInfo,PortScope
import threading
import zmq
import time
from .exc import OperationError, PortError
from enum import Enum

try:
    import cPickle
    pickle = cPickle
except:
    cPickle = None
    import pickle

class _DeviceThread(threading.Thread):
    '''
    Prototypical 'inside' thread that implements a 1 sec 
    'ticker' and an echo service.
    '''
    def __init__(self, trigger):
        threading.Thread.__init__(self,daemon=True)
        self.trigger = trigger
        self.active = threading.Event()
        self.active.clear()
        self.terminated = threading.Event()
        self.terminated.clear()
        self.period = 1000.0        # 1 sec 
        self.plug = None
        self.plug_identity = None

    def get_identity(self,ins_port):
        '''
        to be called from the 'outer' component thread, retrieves the identity of the 
        'inner' side (i.e. thread), so that that component thread can send 
        messages to the selected inner (thread).   
        '''
        if self.plug_identity is None:
            while True:
                if self.plug != None:
                    self.plug_identity = ins_port.get_plug_identity(self.plug)
                    break
                time.sleep(0.1)
        return self.plug_identity

    def run(self):
        self.plug = self.parent.setupPlug(self)
        self.poller = zmq.Poller() 
        self.poller.register(self.plug, zmq.POLLIN)
        while 1:
            self.active.wait(None)
            if self.terminated.is_set(): break
            if self.active.is_set():
                socks = dict(self.poller.poll(self.period))
                if self.terminated.is_set(): break
                if self.plug in socks and socks[self.plug] == zmq.POLLIN:
                    msg = self.plug.recv_pyobj()    # Message from component
                    self.plug.send_pyobj(msg)       # ... echo it
                    continue
                if len(socks) == 0:                 # Timeout
                    value = time.time()
                    self.plug.send_pyobj(value)

    def activate(self):
        self.active.set()

    def deactivate(self):
        self.active.clear()

    def terminate(self):
        self.active.set()
        self.terminated.set()

# class Component:
#     pass
#
# class _Device(Component):
#     '''
#     message Query;
#     message Answer;
#     device _Device() {
#         inside trigger;
#         ans echo (Query,Answer);
#     }
#     '''
#     def __init__(self):
#         super().__init__()
#         self.thread = None
#
#     def handleActivate(self):                   # activation: sets up inner thread
#         if self.thread == None: 
#             self.thread = _DeviceThread(self.trigger)
#             self.thread.start() 
#             self.trigger.set_identity(self._DeviceThread.get_identity(self.trigger))
#             self.trigger.activate()
#
#     def __destroy__(self):
#         self._DeviceThread.deactivate()
#         self._DeviceThread.terminate()
#         self._DeviceThread.join()
#
#     def on_trigger(self):                       # operation triggered by inner thread
#         msg = self.trigger.recv_pyobj()
#         if type(msg) == float:                  # time value
#             pass
#         else:                                   # echo answer
#             self.echo.send_pyobj(msg)
#
#     def on_echo(self):
#         qry = self.echo.recv_pyobj()            # recv query to echo
#         self.trigger.send_pyobj(qry)            # send it to inner thread


class InsPort(Port):
    '''
    classdocs
    '''
        
    def __init__(self, parentPart, portName, portSpec):
        '''
        Constructor
        '''
        super(InsPort, self).__init__(parentPart, portName, portSpec)
        self.instName = self.parent.name + '.' + self.name
        self.spec = portSpec["spec"]
        self.inner_threads = []
        self.parent_thread = None
        self.info = None
        self.plugMap = { }
        self.identity = bytes(8)    # Default identity, it is an error to use it. 

    def setup(self):
        if self.spec == 'default':
            thread = _DeviceThread(self)
            thread.start()
            self.activate()
        else:
            pass 
    
    def setupSocket(self, owner):
        self.setOwner(owner)
        self.parent_thread = threading.current_thread()
        self.socket = self.context.socket(zmq.ROUTER)
        self.socket.bind('inproc://inside_' + self.instName)
        self.info = PortInfo(portKind='ins', portScope=PortScope.INTERNAL, portName=self.name, 
                             msgType='inside', portHost='', portNum=-1)
        return self.info
    
    def reset(self):
        pass
    
    def setupPlug(self, thread):
        assert thread != self.parent_thread  # Must be called from an inner thread
        if thread in self.inner_threads:
            raise OperationError('inside thread %s already running on %s' % (thread.ident, self.instName))
        else:
            self.inner_threads += [thread]
        plug = self.context.socket(zmq.DEALER)
        identity = str(id(thread))
        plug.setsockopt_string(zmq.IDENTITY, identity, 'utf-8')
        plug.connect('inproc://inside_' + self.instName)
        self.plugMap[plug] = bytes(identity, 'utf-8')
        return plug

    def activate(self):
        for thread in self.inner_threads:
            if thread and hasattr(thread, 'activate'):
                thread.activate()
        
    def deactivate(self):
        for thread in self.inner_threads:
            if thread and hasattr(thread, 'deactivate'):
                thread.deactivate()
        
    def terminate(self):
        for thread in self.inner_threads:
            if hasattr(thread, 'terminate') and thread.is_alive():
                thread.terminate()

    def getSocket(self):
        return self.socket
    
    def inSocket(self):
        return True
    
    def getContext(self):
        return self.context
    
    def get_plug_identity(self, plug):
        return self.plugMap.get(plug, None)
    
    def get_identity(self):
        return self.identity
    
    def set_identity(self, identity):
        self.identity = identity
        
    def ins_port_recv(self, is_pyobj): 
        try:
            msgFrames = self.socket.recv_multipart()  # Receive multipart (IDENTITY + payload) message
        except zmq.error.ZMQError as e:
            raise PortError("recv error (%d)" % e.errno, e.errno) from e
        self.identity = msgFrames[0]  # Separate identity, it is a Frame
        if is_pyobj:
            result = pickle.loads(msgFrames[1])  # Separate payload (pyobj)
        else:
            result = msgFrames[1]  # Separate payload (bytes)
        return result
        
    def ins_port_send(self, msg, is_pyobj):
        try:
            sendMsg = [self.identity]  # Identity is already a frame
            if is_pyobj:
                payload = zmq.Frame(pickle.dumps(msg))  # Pickle python payload
            else:
                payload = zmq.Frame(msg)  # Take bytes                        
            sendMsg += [payload]
            self.socket.send_multipart(sendMsg)
        except zmq.error.ZMQError as e:
            raise PortError("send error (%d)" % e.errno, e.errno) from e
        return True
    
    def recv_pyobj(self):
        return self.ins_port_recv(True)

    def send_pyobj(self, msg): 
        return self.ins_port_send(msg, True)     
    
    def recv(self):
        return self.ins_port_recv(False)

    def send(self, msg):
        return self.ins_port_send(msg, False)
    
    def getInfo(self):
        return self.info
    
