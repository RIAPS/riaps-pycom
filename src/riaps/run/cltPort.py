'''
Client port class
Created on Oct 10, 2016

@author: riaps
'''
import zmq
from .port import Port,PortInfo,DuplexConnPort
from riaps.utils.config import Config
from zmq.error import ZMQError
# from .part import Part
# from .actor import Actor


class CltPort(DuplexConnPort):
    '''
    Client port is to access a server. Has a request and a response message type, and uses a REQ socket.
    '''

    def __init__(self, parentComponent, portName, portSpec):
        '''
        Initialize the client port object.
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
        return self.setupConnSocket(owner,zmq.REQ,'clt')

    def closeSocket(self):
        self.closeConnSocket()
    
    def reset(self):
        self.resetConnSocket(zmq.REQ)
    
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
        '''
        Retrieve relevant information about this port
        '''
        return self.info 
    
