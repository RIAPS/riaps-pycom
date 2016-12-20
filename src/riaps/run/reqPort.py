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
        parentActor = parentComponent.parent
        self.isLocalPort = parentActor.isLocalMessage(self.req_type) and parentActor.isLocalMessage(self.rep_type)
        self.replyHost = None
        self.replyPort = None

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
        return ('req',self.isLocalPort,self.name,str(self.req_type) + '#' + str(self.rep_type),self.host)
    
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
        return self.socket.recv_pyobj()
    
    def send_pyobj(self,msg):
        try:
            self.socket.send_pyobj(msg)
        except ZMQError as e:
            if e.errno == zmq.EAGAIN:
                return False
            else:
                raise
        return True

    def getInfo(self):
        return ("req",self.name,(self.req_type,self.rep_type),
                self.host,self.portNum,
                self.replyHost,self.replyPort)
    