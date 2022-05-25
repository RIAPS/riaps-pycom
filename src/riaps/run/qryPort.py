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
        
        # self.req_type = portSpec["req_type"]
        # self.rep_type = portSpec["rep_type"]
        # self.isTimed = portSpec["timed"]
        # self.deadline = portSpec["deadline"] * 0.001  # msec
        # parentActor = parentComponent.parent
        # req_kind = parentActor.messageKind(self.req_type)
        # rep_kind = parentActor.messageKind(self.rep_type)
        # assert req_kind == rep_kind
        # self.portKind = req_kind
        # self.answers = set()
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
        # self.setOwner(owner)
        # self.socket = self.context.socket(zmq.DEALER)
        # self.socket.setsockopt_string(zmq.IDENTITY, str(id(self)), 'utf-8')  # FIXME: identity is not unique across nodes
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
        # self.info = PortInfo(portType='qry', portKind=self.portKind, portName=self.name, 
        #                      msgType=str(self.req_type) + '#' + str(self.rep_type), 
        #                      host=self.host, portNum=self.portNum)
        # return self.info

    def closeSocket(self):
        self.closeConnSocket()
        
    def reset(self):
        self.resetConnSocket(zmq.DEALER,[(zmq.IDENTITY,str(id(self)))] )
        # self.socket.setsockopt(zmq.LINGER, 0)
        # for (host,port) in self.answers:
        #     ansPort = "tcp://" + str(host) + ":" + str(port)
        #     self.socket.disconnect(ansPort)
        # self.owner.replaceSocket(self, newSocket)
        # self.socket = newSocket
        # self.setupCurve(False)
        # for (host,port) in self.answers:
        #     ansPort = "tcp://" + str(host) + ":" + str(port)
        #     self.socket.disconnect(ansPort)
    
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
    
    # def update(self, host, port):
    #     '''
    #     Update the query -- connect its socket to a server
    #     '''
    #     if (host,port) not in self.answers:
    #         ansPort = "tcp://" + str(host) + ":" + str(port)
    #         self.answers.add((host,port))
    #         self.socket.connect(ansPort)
    
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
    
