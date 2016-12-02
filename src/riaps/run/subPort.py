'''
Created on Oct 10, 2016

@author: riaps
'''
import zmq
from .port import Port
from riaps.run.exc import OperationError

class SubPort(Port):
    '''
    classdocs
    '''


    def __init__(self, parentComponent, portName, portSpec):
        '''
        Constructor
        '''
        super(SubPort,self).__init__(parentComponent,portName)
        self.type = portSpec["type"]
        parentActor = parentComponent.parent
        self.isLocalPort = parentActor.isLocalMessage(self.type)
        self.pubs = []
    
    def setup(self):
        pass
       
    def setupSocket(self):
        self.socket = self.context.socket(zmq.SUB)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, '')
        self.host = ''
        if not self.isLocalPort:
            globalHost = self.getGlobalIface()
            self.portNum = -1 
            self.host = globalHost
        else:
            localHost = self.getLocalIface()
            self.portNum = -1 
            self.host = localHost
        return ('sub',self.isLocalPort,self.name,self.type,self.host)
    
    def getSocket(self):
        return self.socket
    
    def inSocket(self):
        return True
    
    def update(self,host,port):
        pubPort = "tcp://" + str(host) + ":" + str(port)
        self.pubs.append((host,port))
        self.socket.connect(pubPort)
     
    def recv_pyobj(self):
        return self.socket.recv_pyobj()
    
    def send_pyobj(self):
        raise OperationError("attempt to send through a subscriber port")

    def getInfo(self):
        return ("sub",self.name,self.type,self.host,self.portNum,self.pubs)
    