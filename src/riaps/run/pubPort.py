'''
Created on Oct 10, 2016

@author: riaps
'''
import zmq
from riaps.run.port import Port
from riaps.run.exc import OperationError
from riaps.utils.config import Config
from zmq.error import ZMQError
#from .part import Part
#from .actor import Actor

class PubPort(Port):
    '''
    classdocs
    '''


    def __init__(self, parentComponent, portName, portSpec):
        '''
        Constructor
        '''
        super(PubPort,self).__init__(parentComponent,portName)
        self.type = portSpec["type"]
        parentActor = parentComponent.parent
        self.isLocalPort = parentActor.isLocalMessage(self.type)
    
    def setup(self):
        pass
        
    def setupSocket(self):
        self.socket = self.context.socket(zmq.PUB)
        self.socket.setsockopt(zmq.SNDTIMEO,self.sendTimeout) 
        self.host = ''
        self.portNum = -1 
        if not self.isLocalPort:
            globalHost = self.getGlobalIface()
            self.portNum = self.socket.bind_to_random_port("tcp://" + globalHost)
            self.host = globalHost
        else:
            localHost = self.getLocalIface()
            self.portNum = self.socket.bind_to_random_port("tcp://" + localHost)
            self.host = localHost
        return ('pub',self.isLocalPort,self.name,self.type,self.host,self.portNum)
    
    def update(self, host, port):
        raise OperationError("Unsupported update() on PubPort")
    
    def getSocket(self):
        return self.socket
    
    def inSocket(self):
        return False
    
    def send_pyobj(self,msg):
        try:
            self.socket.send_pyobj(msg)
        except ZMQError as e:
            if e.errno == zmq.EAGAIN:
                return False
            else:
                raise
        return True
        
    def recv_pyobj(self):
        raise OperationError("attempt to receive through a publish port")
    
    def getInfo(self):
        return ("pub",self.name,self.type,self.host,self.portNum)
    