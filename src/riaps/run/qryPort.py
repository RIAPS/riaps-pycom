'''
Query port class
Created on Oct 10, 2016

@author: riaps
'''
import zmq
from .port import Port,PortInfo,DuplexConnPort
from riaps.utils.config import Config
from zmq.error import ZMQError
# from .part import Part
# from .actor import Actor


class QryPort(DuplexConnPort):
    '''
    Query port is to access a server. Has a request and a response message type, and uses a DEALER socket.
    '''

    def __init__(self, parentComponent, portName, portSpec):
        '''
        Initialize the query port object.
        '''
        super().__init__(parentComponent, portName, portSpec)
        self.info = None

    def setup(self):
        '''
        Set up the port
        '''
        pass
  
    def setupSocket(self, owner):
        '''
        Set up the socket of the port. Return a tuple suitable for querying the discovery service for the publishers
        '''
        return self.setupConnSocket(owner,zmq.DEALER,'qry',[(zmq.IDENTITY,str(id(self)))])

    def closeSocket(self):
        self.closeConnSocket()
        
    def reset(self):
        self.resetConnSocket(zmq.DEALER,[(zmq.IDENTITY,str(id(self)))] )
    
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
    
    def recv_pyobj(self):
        '''
        Receive an object through this port
        '''
        if len(self.servers) == 0:
            return None
        else:
            return self.port_recv(True)
    
    def send_pyobj(self, msg):
        '''
        Send an object through this port
        '''
        if len(self.servers) == 0:
            return False
        else:
            return self.port_send(msg, True)              
    
    def recv(self):
        '''
        Receive a bytes through this port
        '''
        if len(self.servers) == 0:
            return None
        else:
            return self.port_recv(False)
    
    def send(self, msg):
        '''
        Send bytes through this port
        '''
        if len(self.servers) == 0:
            return False
        else:
            return self.port_send(msg, False) 
    
    def getInfo(self):
        '''
        Retrieve relevant information about this port
        '''
        return self.info
    
