'''
Client port class
Created on Oct 10, 2016

@author: riaps
'''
import zmq
from .port import Port
from riaps.utils.config import Config
from zmq.error import ZMQError
#from .part import Part
#from .actor import Actor

class CltPort(Port):
    '''
    Client port is to access a server. Has a request and a response message type, and uses a REQ socket.
    '''


    def __init__(self, parentComponent, portName, portSpec):
        '''
        Initialize the client port object.
        '''
        super(CltPort,self).__init__(parentComponent,portName)
        
        self.req_type = portSpec["req_type"]
        self.rep_type = portSpec["rep_type"]
        parentActor = parentComponent.parent
        # The request and reply message types must be of the same kind (global/local)
        assert parentActor.isInnerMessage(self.req_type) == parentActor.isInnerMessage(self.rep_type)
        assert parentActor.isLocalMessage(self.req_type) == parentActor.isLocalMessage(self.rep_type)
        # Determine if the port is host-local 
        self.isLocalPort = parentActor.isLocalMessage(self.req_type) and parentActor.isLocalMessage(self.rep_type)
        self.serverHost = None
        self.serverPort = None


    def setup(self):
        '''
        Set up the port
        '''
        pass
  
    def setupSocket(self):
        '''
        Set up the socket of the port. Return a tuple suitable for querying the discovery service for the publishers
        '''
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
        return ('clt',self.isLocalPort,self.name,str(self.req_type) + '#' + str(self.rep_type),self.host)
    
    def getSocket(self):
        '''
        Return the socket of port
        '''
        return self.socket
    
    def inSocket(self):
        '''
        Return False because the socket is not used as direct input (client has to recv explicitly)
        '''
        return False
    
    def update(self,host,port):
        '''
        Update the client -- connect its socket to a server
        '''
        srvPort = "tcp://" + str(host) + ":" + str(port)
        self.serverHost = host
        self.serverPort = port
        self.socket.connect(srvPort)
    
    def recv_pyobj(self):
        '''
        Receive an object through this port
        '''
        return self.socket.recv_pyobj()
    
    def send_pyobj(self,msg):
        '''
        Send an object through this port
        '''
        try:
            self.socket.send_pyobj(msg)
        except ZMQError as e:
            if e.errno == zmq.EAGAIN:
                return False
            else:
                raise
        return True

    def recv_capnp(self):
        return self.socket.recv()
    
    def send_capnp(self, msg):
        try:
            self.socket.send(msg)
        except ZMQError as e:
            if e.errno == zmq.EAGAIN:
                return False
            else:
                raise
        return True
    
    def getInfo(self):
        '''
        Retrieve relevant information about this port
        '''
        return ("clt",self.name,(self.req_type,self.rep_type),self.host,self.portNum,self.serverHost,self.serverPort)
    