'''
Created on Oct 10, 2016

@author: riaps
'''
import time
import zmq
import struct
from .port import Port,PortScope,PortInfo,DuplexBindPort
from riaps.run.exc import OperationError, PortError
from riaps.utils.config import Config
from zmq.error import ZMQError
try:
    import cPickle
    pickle = cPickle
except:
    cPickle = None
    import pickle

    
class AnsPort(DuplexBindPort):
    '''
    classdocs
    '''

    def __init__(self, parentComponent, portName, portSpec):
        '''
        Constructor
        '''
        super().__init__(parentComponent, portName, portSpec)
        # self.req_type = portSpec["req_type"]
        # self.rep_type = portSpec["rep_type"]
        # self.isTimed = portSpec["timed"]
        # self.deadline = portSpec["deadline"] * 0.001  # msec
        # parentActor = parentComponent.parent
        # req_scope = parentActor.messageScope(self.req_type)
        # rep_scope = parentActor.messageScope(self.rep_type)
        # assert req_scope == rep_scope
        # self.portScope = req_scope
        self.identity = None
        self.info = None

    def setup(self):
        pass
  
    def setupSocket(self, owner):
        return self.setupBindSocket(owner,zmq.ROUTER,'ans',[(zmq.ROUTER_MANDATORY,1)])
        # self.setOwner(owner)
        # self.socket = self.context.socket(zmq.ROUTER)
        # self.socket.setsockopt(zmq.SNDTIMEO, self.sendTimeout)
        # self.setupCurve(True)
        # self.host = ''
        # if self.portKind == PortKind.GLOBAL:
        #     globalHost = self.getGlobalIface()
        #     self.portNum = self.socket.bind_to_random_port("tcp://" + globalHost)
        #     self.host = globalHost
        # else:
        #     localHost = self.getLocalIface()
        #     self.portNum = self.socket.bind_to_random_port("tcp://" + localHost)
        #     self.host = localHost
        # self.info = PortInfo(portKind='ans', portScope=self.portScope, portName=self.name, 
        #                      msgType=str(self.req_type) + '#' + str(self.rep_type), 
        #                      portHost=self.host, portNum=self.portNum)
        # return self.info

    def update(self, host, port):
        raise OperationError("Unsupported update() on AnsPort")
    
    def reset(self):
        pass
    
    def getSocket(self):
        return self.socket
    
    def inSocket(self):
        return True
    
    def get_identity(self):
        return self.identity
    
    def set_identity(self, identity):
        self.identity = identity
        
    def ans_port_recv(self, is_pyobj): 
        try:
            msgFrames = self.socket.recv_multipart()  # Receive multipart (IDENTITY + payload) message
        except zmq.error.ZMQError as e:
            raise PortError("recv error (%d)" % e.errno, e.errno) from e
        if self.isTimed:
            self.recvTime = time.time()
        self.identity = msgFrames[0]  # Separate identity, it is a Frame
        if is_pyobj:
            result = pickle.loads(msgFrames[1])  # Separate payload (pyobj)
        else:
            result = msgFrames[1]  # Separate payload (bytes)
        if len(msgFrames) == 3:  # If we have a send time stamp
            rawMsg = msgFrames[2]
            rawTuple = struct.unpack("d", rawMsg)
            self.sendTime = rawTuple[0]
        return result
        
    def ans_port_send(self, msg, is_pyobj):
        try:
            sendMsg = [self.identity]  # Identity is already a frame
            if is_pyobj:
                payload = zmq.Frame(pickle.dumps(msg))  # Pickle python payload
            else:
                payload = zmq.Frame(msg)  # Take bytes                        
            sendMsg += [payload]
            if self.isTimed:
                now = time.time()
                now = struct.pack("d", now)
                nowFrame = zmq.Frame(now)
                sendMsg += [nowFrame]
            self.socket.send_multipart(sendMsg)
        except zmq.error.ZMQError as e:
            raise PortError("send error (%d)" % e.errno, e.errno) from e
        return True
    
    def recv_pyobj(self):
        return self.ans_port_recv(True)

    def send_pyobj(self, msg): 
        return self.ans_port_send(msg, True)     
    
    def recv(self):
        return self.ans_port_recv(False)

    def send(self, msg):
        return self.ans_port_send(msg, False)
        
    def getInfo(self):
        return self.info
    
