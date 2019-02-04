'''
Created on Oct 10, 2016

@author: riaps
'''
import zmq
import time
import struct
from riaps.run.port import Port
from riaps.run.exc import OperationError
from riaps.utils.config import Config
from zmq.error import ZMQError
try:
    import cPickle
    pickle = cPickle
except:
    cPickle = None
    import pickle

class PubPort(Port):
    '''
    classdocs
    '''
    def __init__(self, parentComponent, portName, portSpec):
        '''
        Constructor
        '''
        super(PubPort,self).__init__(parentComponent,portName)
        self.type = portSpec["type"]
        self.isTimed = portSpec["timed"]
        parentActor = parentComponent.parent
        self.isLocalPort = parentActor.isLocalMessage(self.type)
        self.info = None
    
    def setup(self):
        pass
        
    def setupSocket(self,owner):
        self.setOwner(owner)
        self.socket = self.context.socket(zmq.PUB)
        self.socket.setsockopt(zmq.SNDTIMEO,self.sendTimeout) 
        self.host = ''
        self.portNum = -1
        self.setupCurve(True) 
        if not self.isLocalPort:
            globalHost = self.getGlobalIface()
            self.portNum = self.socket.bind_to_random_port("tcp://" + globalHost)
            self.host = globalHost
        else:
            localHost = self.getLocalIface()
            self.portNum = self.socket.bind_to_random_port("tcp://" + localHost)
            self.host = localHost
        self.info = ('pub',self.isLocalPort,self.name,self.type,self.host,self.portNum)
        return self.info
        
    def reset(self):
        pass
    
    def update(self, host, port):
        raise OperationError("Unsupported update() on PubPort")
    
    def getSocket(self):
        return self.socket
    
    def inSocket(self):
        return False
    
    def send_pyobj(self,msg):
        return self.port_send(msg,True)

    def send(self, msg):
        return self.port_send(msg,False)
        
    def recv_pyobj(self):
        raise OperationError("attempt to receive through a publish port")
    
    def recv(self):
        raise OperationError("attempt to receive through a publish port")
    
    def getInfo(self):
        return self.info
    
    
    