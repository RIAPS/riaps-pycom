'''
Created on Oct 10, 2016

@author: riaps
'''
import zmq
from .port import Port
from riaps.run.exc import OperationError
from riaps.utils.config import Config
from zmq.error import ZMQError

class RepPort(Port):
    '''
    Similar to a server port, but it uses two separate sockets: in_socket for receiving requests, 
    out_socket for sending replies.
    One RepPort is connected to one ReqPort 
    '''


    def __init__(self, parentComponent, portName, portSpec):
        '''
        Constructor
        '''
        super(RepPort,self).__init__(parentComponent,portName)
        self.req_type = portSpec["req_type"]
        self.rep_type = portSpec["rep_type"]
        parentActor = parentComponent.parent
        self.isLocalPort = parentActor.isLocalMessage(self.req_type) and parentActor.isLocalMessage(self.rep_type)

    def setup(self):
        pass
        
    def setupSocket(self):
        self.socket = self.context.socket(zmq.REP)
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
        return ('rep',self.isLocalPort,self.name,str(self.req_type) + '#' + str(self.rep_type),self.host,self.portNum)
    
    def getSocket(self):
        return self.socket
    
    def inSocket(self):
        return True
    
    def update(self,host,port):
        raise OperationError("Unsupported update() on RepPort")
        
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

    def send_capnp(self, msg):
        try:
            self.socket.send(msg)
        except ZMQError as e:
            if e.errno == zmq.EAGAIN:
                return False
            else:
                raise
        return True

    def recv_capnp(self):
        return self.socket.recv()

    def getInfo(self):
        return ("rep",self.name,(self.req_type,self.rep_type), self.host, self.portNum)
    
