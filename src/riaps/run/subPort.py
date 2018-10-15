'''
Created on Oct 10, 2016

@author: riaps
'''
import zmq
import time
import struct
from .port import Port
from riaps.run.exc import OperationError
try:
    import cPickle
    pickle = cPickle
except:
    cPickle = None
    import pickle

class SubPort(Port):
    '''
    classdocs
    '''
    def __init__(self, parentComponent, portName, portSpec):
        '''
        Constructor
        '''
        super(SubPort,self).__init__(parentComponent,portName)
        self.type = portSpec["type"]
        self.isTimed = portSpec["timed"]
        self.deadline = portSpec["deadline"] * 0.001 # msec
        parentActor = parentComponent.parent
        self.isLocalPort = parentActor.isLocalMessage(self.type)
        self.pubs = []
        self.sendTime = 0.0
        self.recvTime = 0.0
        self.info = None
    
    def setup(self):
        pass
       
    def setupSocket(self,owner):
        self.setOwner(owner)
        self.socket = self.context.socket(zmq.SUB)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, '')
        self.host = ''
        if not self.isLocalPort:
            globalHost = self.getGlobalIface()
            self.portNum = -1 
            self.host = globalHost
        else:
            localHost = self.getLocalIface()
            self.portNum = -1 
            self.host = localHost
        self.info = ('sub',self.isLocalPort,self.name,self.type,self.host)
        return self.info
    
    def reset(self):
        pass
    
    def getSocket(self):
        return self.socket
    
    def inSocket(self):
        return True
    
    def update(self,host,port):
        pubPort = "tcp://" + str(host) + ":" + str(port)
        self.pubs.append((host,port))
        self.socket.connect(pubPort)
    
    def recv_pyobj(self):
        return self.port_recv(True)

    def send_pyobj(self,msg):
        raise OperationError("attempt to send through a subscriber port")
    
    def recv(self):
        return self.port_recv(False)
    
    def send(self):
        raise OperationError("attempt to send through a subscriber port")

    def getInfo(self):
        return self.info
    
