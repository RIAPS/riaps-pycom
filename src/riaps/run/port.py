'''
Port
Base class for all Port objects
Created on Oct 9, 2016

@author: riaps
'''
import zmq
import time
import struct
from .exc import SetupError,OperationError,PortError
from riaps.utils.config import Config
import logging

try:
    import cPickle
    pickle = cPickle
except:
    cPickle = None
    import pickle
    
class Port(object):
    '''
    classdocs
    '''

    def __init__(self, parentPart, portName):
        '''
        Constructor
        '''
        self.logger = logging.getLogger(__name__)
        self.parent = parentPart
        self.name = portName
        self.context = parentPart.context
        self.localIface = None
        self.globalIface = None
        self.sendTimeout = Config.SEND_TIMEOUT
        self.recvTimeout = Config.RECV_TIMEOUT
        self.sendTime = 0.0
        self.recvTime = 0.0
        self.socket = None
        self.isTimed = False
        self.deadline = 0.0
        self.info = None
        self.owner = None
    
    def setupSocket(self,owner):
        '''
        Setup the socket. Subclasses override this method to perform the specific setup. 
        '''
        pass
    
    def setOwner(self,owner):
        '''
        Save owner thread.
        '''
        self.owner = owner
    
    def reset(self):
        '''
        Reset socket. Subclasses are to override this method.
        '''
        pass
    
    def getDeadline(self):
        return self.deadline

    def getLocalIface(self):
        if self.localIface != None:
            pass
        else:
            self.localIface = self.parent.parent.getLocalIface()
        return self.localIface
    
    def getGlobalIface(self):
        if self.globalIface != None:
            pass
        else:
            self.globalIface = self.parent.parent.getGlobalIface()
        return self.globalIface
    
    def setup(self):
        '''
        Initialize the port object (after construction but before socket creation) 
        '''
        raise SetupError
            
    def getSocket(self):
        '''
        Retrieve the socket(s) used by the port
        '''
        raise SetupError
    
    def inSocket(self):
        '''
        return True if the socket can be used for input
        '''
        raise SetupError
    
    def getInfo(self):
        '''
        Retrieve configuration information about the port
        Return value is a tuple (with a common prefix) formatted to the specific port type
        Prefix: ( Kind, portName, msgType )
        '''
        return ("port",None,None)
    
    def update(self,host,port):
        ''' 
        Update the socket(s) - typically connect them to another socket
        '''
        raise OperationError("abstract op")
    
    def activate(self):
        pass
    
    def deactivate(self):
        pass
    
    def terminate(self):
        pass
    
    def send_pyobj(self,msg):
        '''
        Send an object (if possible) out through the port
        '''
        pass
    
    def recv_pyobj(self):
        '''
        Receive an object (if possible) through the port
        '''
        return None

    def send_capnp(self,msg):
        '''
        DEPRECATED
        Send a byte array (if possible) out through the port
        '''
        self.logger.warning("send_capnp: deprecated, use send() instead")
        pass
    
    def recv_capnp(self):
        '''
        DEPRECATED
        Receive an object (if possible) through the port
        '''
        self.logger.warning("recv_capnp: deprecated, use recv() instead")
        return None
    
    def send(self,msg):
        '''
        Send a byte array (if possible) out through the port
        '''
        pass
    
    def recv(self):
        '''
        Receive a byte array (if possible) through the port
        '''
        return None
    
    def port_send(self,msg,is_pyobj):
        try:
            if is_pyobj:
                sendMsg = [zmq.Frame(pickle.dumps(msg))]
            else:
                sendMsg = [zmq.Frame(msg)]
            if self.isTimed:
                now = time.time()
                now = struct.pack("d", now)
                nowFrame = zmq.Frame(now)
                sendMsg += [nowFrame]
            self.socket.send_multipart(sendMsg)
        except zmq.error.ZMQError as e:
            raise PortError("send error (%d)" % e.errno, e.errno) from e
        return True
    
    def port_recv(self,is_pyobj):
        try:
            msgFrames = self.socket.recv_multipart()
        except zmq.error.ZMQError as e:
            raise PortError("recv error (%d)" % e.errno, e.errno) from e
        if self.isTimed:
            self.recvTime = time.time()
        if is_pyobj:
            result = pickle.loads(msgFrames[0])
        else:
            result = msgFrames[0]
        if len(msgFrames) == 2:
            rawMsg = msgFrames[1]
            rawTuple = struct.unpack("d", rawMsg)
            self.sendTime = rawTuple[0]
        return result
        
    def get_recvTime(self):
        return self.recvTime
    
    def get_sendTime(self):
        return self.sendTime
    
    def get_recv_timeout(self):
        rto = None if self.recvTimeout == -1 else self.recvTimeout * 0.001
        return rto
        
    def get_send_timeout(self):
        sto = None if self.sendTimeout == -1 else self.sendTimeout * 0.001
        return sto
    
    def set_recv_timeout(self,rto):
        assert rto == None or (type(rto) == float and rto >= 0.0)
        self.recvTimeout = -1 if rto == None else int(rto * 1000)
        self.socket.setsockopt(zmq.RCVTIMEO,self.recvTimeout)

    def set_send_timeout(self,sto):
        assert sto == None or (type(sto) == float and sto >= 0.0)
        self.sendTimeout = -1 if sto == None else int(sto * 1000)
        self.socket.setsockopt(zmq.SNDTIMEO,self.sendTimeout)
    
