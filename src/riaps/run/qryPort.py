'''
Query port class
Created on Oct 10, 2016

@author: riaps
'''
import zmq
from .port import Port
from riaps.utils.config import Config
from zmq.error import ZMQError
#from .part import Part
#from .actor import Actor

class QryPort(Port):
    '''
    Query port is to access a server. Has a request and a response message type, and uses a DEALER socket.
    '''


    def __init__(self, parentComponent, portName, portSpec):
        '''
        Initialize the query port object.
        '''
        super(QryPort,self).__init__(parentComponent,portName)
        
        self.req_type = portSpec["req_type"]
        self.rep_type = portSpec["rep_type"]
        self.isTimed = portSpec["timed"]
        self.deadline = portSpec["deadline"] * 0.001 # msec
        parentActor = parentComponent.parent
        # The request and reply message types must be of the same kind (global/local)
        assert parentActor.isInnerMessage(self.req_type) == parentActor.isInnerMessage(self.rep_type)
        assert parentActor.isLocalMessage(self.req_type) == parentActor.isLocalMessage(self.rep_type)
        # Determine if the port is host-local 
        self.isLocalPort = parentActor.isLocalMessage(self.req_type) and parentActor.isLocalMessage(self.rep_type)
        self.serverHost = None
        self.serverPort = None
        self.info = None


    def setup(self):
        '''
        Set up the port
        '''
        pass
  
    def setupSocket(self,owner):
        '''
        Set up the socket of the port. Return a tuple suitable for querying the discovery service for the publishers
        '''
        self.setOwner(owner)
        self.socket = self.context.socket(zmq.DEALER)
        self.socket.setsockopt_string(zmq.IDENTITY, str(id(self)), 'utf-8')  # FIXME: identity is not unique across nodes
        self.socket.setsockopt(zmq.SNDTIMEO,self.sendTimeout)
        self.setupCurve(False) 
        self.host = ''
        if not self.isLocalPort:
            globalHost = self.getGlobalIface()
            self.portNum = -1 
            self.host = globalHost
        else:
            localHost = self.getLocalIface()
            self.portNum = -1 
            self.host = localHost
        self.info = ('qry',self.isLocalPort,self.name,str(self.req_type) + '#' + str(self.rep_type),self.host)
        return self.info
    
    def reset(self):
        pass
    
    def getSocket(self):
        '''
        Return the socket of port
        '''
        return self.socket
    
    def inSocket(self):
        '''
        Return True because the socket is used of input
        '''
        return True
    
    def update(self,host,port):
        '''
        Update the query -- connect its socket to a server
        '''
        srvPort = "tcp://" + str(host) + ":" + str(port)
        self.serverHost = host
        self.serverPort = port
        self.socket.connect(srvPort)
    
    def recv_pyobj(self):
        '''
        Receive an object through this port
        '''
        if self.serverHost == None or self.serverPort == None:
            return None
        return self.port_recv(True)
    
    def send_pyobj(self,msg):
        '''
        Send an object through this port
        '''
        if self.serverHost == None or self.serverPort == None:
            return False
        return self.port_send(msg,True)              
    
    def recv(self):
        '''
        Receive a bytes through this port
        '''
        if self.serverHost == None or self.serverPort == None:
            return None
        return self.port_recv(False)
    
    def send(self, msg):
        '''
        Send bytes through this port
        '''
        if self.serverHost == None or self.serverPort == None:
            return None
        return self.port_send(msg,False) 
    
    def getInfo(self):
        '''
        Retrieve relevant information about this port
        '''
        return self.info
    
    