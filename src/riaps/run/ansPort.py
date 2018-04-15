'''
Created on Oct 10, 2016

@author: riaps
'''
import time
import zmq
import struct
from .port import Port
from riaps.run.exc import OperationError
from riaps.utils.config import Config
from zmq.error import ZMQError
try:
    import cPickle
    pickle = cPickle
except:
    cPickle = None
    import pickle
    
class AnsPort(Port):
    '''
    classdocs
    '''

    def __init__(self, parentComponent, portName, portSpec):
        '''
        Constructor
        '''
        super(AnsPort,self).__init__(parentComponent,portName)
        self.req_type = portSpec["req_type"]
        self.rep_type = portSpec["rep_type"]
        self.isTimed = portSpec["timed"]
        self.deadline = portSpec["deadline"] * 0.001 # msec
        parentActor = parentComponent.parent
        self.isLocalPort = parentActor.isLocalMessage(self.req_type) and parentActor.isLocalMessage(self.rep_type)
        self.identity = None
        self.info = None

    def setup(self):
        pass
  
    def setupSocket(self):
        self.socket = self.context.socket(zmq.ROUTER)
        self.socket.setsockopt(zmq.SNDTIMEO,self.sendTimeout)
        self.host = ''
        if not self.isLocalPort:
            globalHost = self.getGlobalIface()
            self.portNum = self.socket.bind_to_random_port("tcp://" + globalHost)
            self.host = globalHost
        else:
            localHost = self.getLocalIface()
            self.portNum = self.socket.bind_to_random_port("tcp://" + localHost)
            self.host = localHost
        self.info = ('ans',self.isLocalPort,self.name,str(self.req_type) + '#' + str(self.rep_type), self.host,self.portNum)
        return self.info

    def update(self, host, port):
        raise OperationError("Unsupported update() on AnsPort")
    
    def getSocket(self):
        return self.socket
    
    def inSocket(self):
        return True
    
    def get_identity(self):
        return self.identity
    
    def set_identity(self,identity):
        self.identity = identity
        
    def ans_port_recv(self,is_pyobj):
        msgFrames = self.socket.recv_multipart()    # Receive multipart (IDENTITY + payload) message
        if self.isTimed:
            self.recvTime = time.time()
        self.identity = msgFrames[0]                # Separate identity, it is a Frame
        if is_pyobj:
            result = pickle.loads(msgFrames[1])     # Separate payload (pyobj)
        else:
            result = msgFrames[1]                   # Separate payload (bytes)
        if len(msgFrames) == 3:                     # If we have a send time stamp
            rawMsg = msgFrames[2]
            rawTuple = struct.unpack("d", rawMsg)
            self.sendTime = rawTuple[0]
        return result
        
    def ans_port_send(self,msg,is_pyobj):
        try:
            sendMsg = [self.identity]                   # Identity is already a frame
            if is_pyobj:
                payload = zmq.Frame(pickle.dumps(msg))  # Pickle python payload
            else:
                payload = zmq.Frame(msg)                # Take bytearray                        
            sendMsg += [payload]
            if self.isTimed:
                now = time.time()
                now = struct.pack("d", now)
                nowFrame = zmq.Frame(now)
                sendMsg += [nowFrame]
            self.socket.send_multipart(sendMsg)
        except ZMQError as e:
            if e.errno == zmq.EAGAIN:
                return False
            else:
                raise
        return True
    
    def recv_pyobj(self):
        return self.ans_port_recv(True)

    def send_pyobj(self,msg): 
        return self.ans_port_send(msg,True)     
    
    def recv_capnp(self):
        return self.ans_port_recv(False)

    def send_capnp(self, msg):
        return self.ans_port_send(False)
        
    def getInfo(self):
        return self.info
    