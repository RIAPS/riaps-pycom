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
    Similar to a server port.
    '''


    def __init__(self, parentComponent, portName, portSpec):
        '''
        Constructor
        '''
        super(RepPort,self).__init__(parentComponent,portName)
        self.req_type = portSpec["req_type"]
        self.rep_type = portSpec["rep_type"]
        self.isTimed = portSpec["timed"]
        self.deadline = portSpec["deadline"] * 0.001 # msec
        parentActor = parentComponent.parent
        self.isLocalPort = parentActor.isLocalMessage(self.req_type) and parentActor.isLocalMessage(self.rep_type)
        self.info = None

    def setup(self):
        pass
        
    def setupSocket(self,owner):
        self.setOwner(owner)
        self.socket = self.context.socket(zmq.REP)
        self.socket.setsockopt(zmq.SNDTIMEO,self.sendTimeout)
        self.setupCurve(True)
        self.host = ''
        if not self.isLocalPort:
            globalHost = self.getGlobalIface()
            self.portNum = self.socket.bind_to_random_port("tcp://" + globalHost) 
            self.host = globalHost
        else:
            localHost = self.getLocalIface()
            self.portNum = self.socket.bind_to_random_port("tcp://" + localHost)
            self.host = localHost
        self.info = ('rep',self.isLocalPort,self.name,str(self.req_type) + '#' + str(self.rep_type),self.host,self.portNum)
        return self.info
    
    def reset(self):
        pass
    
    def getSocket(self):
        return self.socket
    
    def inSocket(self):
        return True
    
    def update(self,host,port):
        raise OperationError("Unsupported update() on RepPort")
        
    def recv_pyobj(self):
        return self.port_recv(True)
    
    def send_pyobj(self,msg):
        return self.port_send(msg,True)              
    
    def recv(self):
        return self.port_recv(False)
    
    def send(self, msg):
        return self.port_send(msg,False) 
    
    def getInfo(self):
        return self.info
    
    
