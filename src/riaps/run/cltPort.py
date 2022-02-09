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
        #
        # self.req_type = portSpec["req_type"]
        # self.rep_type = portSpec["rep_type"]
        # self.isTimed = portSpec["timed"]
        # parentActor = parentComponent.parent
        # req_scope = parentActor.messageScope(self.req_type)
        # rep_scope = parentActor.messageScope(self.rep_type)
        # assert req_scope == rep_scope
        # self.portScope = req_scope
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
        # self.info = PortInfo(portType='clt', portKind=self.portKind, portName=self.name, 
        #                      msgType=str(self.req_type) + '#' + str(self.rep_type), 
        #                      host=self.host, portNum=self.portNum) 
        # return self.info

    def reset(self):
        self.resetConnSocket(zmq.REQ)
        # newSocket = self.setupConnSocket(self.owner,zmq.REQ,'clt')
        # self.socket.setsockopt(zmq.LINGER, 0)
        # for (host,port) in self.servers:
        #     srvPort = "tcp://" + str(host) + ":" + str(port)
        #     self.socket.disconnect(srvPort)
        # self.owner.replaceSocket(self, newSocket)
        # self.socket = newSocket
        # self.setupCurve(False)
        # for (host,port) in self.servers:
        #     srvPort = "tcp://" + str(host) + ":" + str(port)
        #     self.socket.connect(srvPort)
    
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
    
    # def update(self, host, port):
    #     '''
    #     Update the client -- connect its socket to a server
    #     '''
    #     if (host,port) not in self.servers:
    #         srvPort = "tcp://" + str(host) + ":" + str(port)
    #         self.servers.add((host,port))
    #         self.socket.connect(srvPort)
        
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
    
