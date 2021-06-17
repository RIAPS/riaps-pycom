'''
Created on Oct 10, 2016

@author: riaps
'''
import zmq
import time
import struct
from .port import Port,PortScope,PortInfo,SimplexConnPort
from riaps.run.exc import OperationError
try:
    import cPickle
    pickle = cPickle
except:
    cPickle = None
    import pickle


class SubPort(SimplexConnPort):
    '''
    classdocs
    '''

    def __init__(self, parentComponent, portName, portSpec):
        '''
        Constructor
        '''
        super().__init__(parentComponent, portName, portSpec)
        self.pubs = []
    
    def setup(self):
        pass
       
    def setupSocket(self, owner):
        return self.setupConnSocket(owner,zmq.SUB,'sub',[(zmq.SUBSCRIBE,'')])
        # self.setOwner(owner)
        # self.socket = self.context.socket(zmq.SUB)
        # self.socket.setsockopt_string(zmq.SUBSCRIBE, '')
        # self.setupCurve(False)
        # self.host = ''
        # if self.portKind == PortKind.GLOBAL:
        #     globalHost = self.getGlobalIface()
        #     self.portNum = -1 
        #     self.host = globalHost
        # else:
        #     localHost = self.getLocalIface()
        #     self.portNum = -1 
        #     self.host = localHost
        # self.info = PortInfo(portType='sub', portKind=self.portKind, portName=self.name, 
        #                      msgType=self.type, host=self.host, portNum=self.portNum)
        # return self.info
    
    def reset(self):
        pass
    
    def getSocket(self):
        return self.socket
    
    def inSocket(self):
        return True
    
    def update(self, host, port):
        pubPort = "tcp://" + str(host) + ":" + str(port)
        self.pubs.append((host, port))
        self.socket.connect(pubPort)
    
    def recv_pyobj(self):
        return self.port_recv(True)

    def send_pyobj(self, msg):
        raise OperationError("attempt to send through a subscriber port")
    
    def recv(self):
        return self.port_recv(False)
    
    def send(self, _msg):
        raise OperationError("attempt to send through a subscriber port")

    def getInfo(self):
        return self.info
    
