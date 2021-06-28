'''
Created on Oct 10, 2016

@author: riaps
'''
import zmq
from .port import Port,PortInfo,DuplexBindPort
from riaps.run.exc import OperationError
from riaps.utils.config import Config
from zmq.error import ZMQError


class SrvPort(DuplexBindPort):
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
        # req_kind = parentActor.messageKind(self.req_type)
        # rep_kind = parentActor.messageKind(self.rep_type)
        # assert req_kind == rep_kind
        # self.portKind = req_kind
        # self.info = None

    def setup(self):
        pass
  
    def setupSocket(self, owner):
        return self.setupBindSocket(owner,zmq.REP,'srv')
        # self.setOwner(owner)
        # self.socket = self.context.socket(zmq.REP)
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
        # self.info = PortInfo(portType='srv', portKind=self.portKind, portName=self.name, 
        #                      msgType=str(self.req_type) + '#' + str(self.rep_type), 
        #                      host=self.host, portNum=self.portNum)
        # return self.info

    def reset(self):
        pass
    
    def update(self, host, port):
        raise OperationError("Unsupported update() on SrvPort")
    
    def getSocket(self):
        return self.socket
    
    def inSocket(self):
        return True
    
    def recv_pyobj(self):
        return self.port_recv(True)
    
    def send_pyobj(self, msg):
        return self.port_send(msg, True)              
    
    def recv(self):
        return self.port_recv(False)
    
    def send(self, msg):
        return self.port_send(msg, False) 
            
    def getInfo(self):
        return self.info
    
