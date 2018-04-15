'''
Created on Oct 10, 2016

@author: riaps
'''
import zmq
from .port import Port
from riaps.run.exc import OperationError
from riaps.utils.config import Config
from zmq.error import ZMQError


class ReqPort(Port):
    '''
    Similar to a client port, but it uses two separate sockets: out_socket for sending requests, 
    in_socket for receiving replies.
    One ReqPort is connected to one RepPort 
    '''

    def __init__(self, parentComponent, portName, portSpec):
        '''
        Constructor
        '''
        super(ReqPort,self).__init__(parentComponent,portName)
        self.req_type = portSpec["req_type"]
        self.rep_type = portSpec["rep_type"]
        self.isTimed = portSpec["timed"]
        self.deadline = portSpec["deadline"] * 0.001 # msec
        parentActor = parentComponent.parent
        self.isLocalPort = parentActor.isLocalMessage(self.req_type) and parentActor.isLocalMessage(self.rep_type)
        self.replyHost = None
        self.replyPort = None
        self.info = None

    def setup(self):
        pass
  
    def setupSocket(self):
        self.socket = self.context.socket(zmq.REQ)
        self.socket.setsockopt(zmq.SNDTIMEO,self.sendTimeout)   
        self.host = ''
        if not self.isLocalPort:
            globalHost = self.getGlobalIface()
            self.portNum = -1
            self.host = globalHost
        else:
            localHost = self.getLocalIface()
            self.portNum = -1
            self.host = localHost
        self.info = ('req',self.isLocalPort,self.name,str(self.req_type) + '#' + str(self.rep_type),self.host)
        return self.info
    
    def getSocket(self):
        return self.socket
    
    def inSocket(self):
        return True
    
    def update(self,host,port):
        repPort = "tcp://" + str(host) + ":" + str(port)
        self.replyHost = host
        self.replyPort = port
        self.socket.connect(repPort)
        
    def recv_pyobj(self):
        return self.port_recv(True)
    
    def send_pyobj(self,msg):
        return self.port_send(msg,True)              
    
    def recv_capnp(self):
        return self.port_recv(False)
    
    def send_capnp(self, msg):
        return self.port_send(msg,False) 

    def getInfo(self):
        return self.info 
    
    
    