'''
Created on Jan 9, 2017

@author: riaps
'''
from .port import Port,PortInfo
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

    
# Example insider thread (1 sec ticker)
class InsThread(threading.Thread):

    def __init__(self, parent):
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
        self.waiting.set()
        self.terminated.set()

        
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

    def setup(self):
        if self.spec == 'default':
            thread = InsThread(self)
            thread.start()
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
    
