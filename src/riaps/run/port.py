'''
Port
Base class for all Port objects
Created on Oct 9, 2016

@author: riaps
'''
from .exc import SetupError,OperationError
from riaps.utils.config import Config
import logging

class Port(object):
    '''
    classdocs
    '''

    def __init__(self, parentPart, portName):
        '''
        Constructor
        '''
        self.logger = logging.getLogger(__name__)
        self.parent = parentPart
        self.name = portName
        self.context = parentPart.context
        self.localIface = None
        self.globalIface = None
        self.sendTimeout = Config.SEND_TIMEOUT

    def getLocalIface(self):
        if self.localIface != None:
            pass
        else:
            self.localIface = self.parent.parent.getLocalIface()
        return self.localIface
    
    def getGlobalIface(self):
        if self.globalIface != None:
            pass
        else:
            self.globalIface = self.parent.parent.getGlobalIface()
        return self.globalIface
    
    def setup(self):
        '''
        Initialize the port object (after construction but before socket creation) 
        '''
        raise SetupError
    
    def setupSocket(self):
        '''
        Create the socket(s) used by the port
        '''
        raise SetupError
    
    def getSocket(self):
        '''
        Retrieve the socket(s) used by the port
        '''
        raise SetupError
    
    def inSocket(self):
        '''
        return True if the socket can be used for input
        '''
        raise SetupError
    
    def getInfo(self):
        '''
        Retrieve configuration information about the port
        Return value is a tuple (with a common prefix) formatted to the specific port type
        Prefix: ( Kind, portName, msgType )
        '''
        return ("port",None,None)
    
    def update(self,host,port):
        ''' 
        Update the socket(s) - typically connect them to another socket
        '''
        raise OperationError("abstract op")
    
    def activate(self):
        pass
    
    def deactivate(self):
        pass
    
    def terminate(self):
        pass
    
    def send_pyobj(self,msg):
        '''
        Send an object (if possible) out through the port
        '''
        pass
    
    def recv_pyobj(self):
        '''
        Receive an object (if possible) through the port
        '''
        return None
    