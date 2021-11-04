'''
Created on Oct 10, 2016

@author: riaps
'''
import zmq
from .port import Port,PortInfo,DuplexConnPort
from riaps.run.exc import OperationError
from riaps.utils.config import Config
from zmq.error import ZMQError

class ReqPort(DuplexConnPort):
    '''
    Similar to a client port
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

    def setup(self):
        pass
  
    def setupSocket(self, owner):
        return self.setupConnSocket(owner,zmq.REQ,'req',[(zmq.REQ_RELAXED,1),(zmq.REQ_CORRELATE,1)])
        # self.setOwner(owner)
        # self.socket = self.context.socket(zmq.REQ)
        # self.socket.setsockopt(zmq.SNDTIMEO, self.sendTimeout)
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
        # self.info = PortInfo(portType='req', portKind=self.portKind, portName=self.name, 
        #                      msgType=str(self.req_type) + '#' + str(self.rep_type), 
        #                      host=self.host, portNum=self.portNum) 
        # return self.info
    
    def reset(self):
        self.resetConnSocket(zmq.REQ)
    
    def getSocket(self):
        return self.socket
    
    def inSocket(self):
        return True
    
    # def update(self, host, port):
    #     if (host,port) not in self.repliers:
    #         repPort = "tcp://" + str(host) + ":" + str(port)
    #         self.repliers.add((host,port))
    #         self.socket.connect(repPort)
        
    def recv_pyobj(self):
        if len(self.servers) == 0:
            return None
        else:
            return self.port_recv(True)
    
    def send_pyobj(self, msg):
        if len(self.servers) == 0:
            return False
        else:
            return self.port_send(msg, True)              
    
    def recv(self):
        if len(self.servers) == 0:
            return None
        else:
            return self.port_recv(False)
    
    def send(self, msg):
        if len(self.servers) == 0:
            return False
        else:
            return self.port_send(msg, False) 

    def getInfo(self):
        return self.info 
    
