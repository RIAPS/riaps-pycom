'''
Created on Oct 10, 2016

@author: riaps
'''
import zmq
from .port import Port
from riaps.run.exc import OperationError
from riaps.utils.config import Config
from zmq.error import ZMQError
try:
    import cPickle
    pickle = cPickle
except:
    cPickle = None
    import pickle
    
class AnsPort(Port):
    '''
    classdocs
    '''

    def __init__(self, parentComponent, portName, portSpec):
        '''
        Constructor
        '''
        super(AnsPort,self).__init__(parentComponent,portName)
        self.req_type = portSpec["req_type"]
        self.rep_type = portSpec["rep_type"]
        parentActor = parentComponent.parent
        self.isLocalPort = parentActor.isLocalMessage(self.req_type) and parentActor.isLocalMessage(self.rep_type)
        self.identity = None

    def setup(self):
        pass
  
    def setupSocket(self):
        self.socket = self.context.socket(zmq.ROUTER)
        self.socket.setsockopt(zmq.SNDTIMEO,self.sendTimeout)
        self.host = ''
        if not self.isLocalPort:
            globalHost = self.getGlobalIface()
            self.portNum = self.socket.bind_to_random_port("tcp://" + globalHost)
            self.host = globalHost
        else:
            localHost = self.getLocalIface()
            self.portNum = self.socket.bind_to_random_port("tcp://" + localHost)
            self.host = localHost
        return ('ans',self.isLocalPort,self.name,str(self.req_type) + '#' + str(self.rep_type), self.host,self.portNum)

    def update(self, host, port):
        raise OperationError("Unsupported update() on AnsPort")
    
    def getSocket(self):
        return self.socket
    
    def inSocket(self):
        return True
                
    def recv_pyobj(self):
        multipart = self.socket.recv_multipart()    # Receive multipart (IDENTITY + payload) message
        self.identity = multipart[0]                # Separate identity, it is a Frame
        py_message = pickle.loads(multipart[1])     # Assuming pickle was used on qry
        # return self.socket.recv_pyobj()
        return py_message
    
    def send_pyobj(self,msg):      
        try:
            content = pickle.dumps(msg)             # Assuming pickle on the qry side
            payload = zmq.Frame(content)
            self.socket.send_multipart([self.identity,payload])
            # self.socket.send_pyobj(msg)
        except ZMQError as e:
            if e.errno == zmq.EAGAIN:
                return False
            else:
                raise
        return True
    
    def get_identity(self):
        return self.identity
    
    def set_identity(self,identity):
        self.identity = identity
    
    def recv_capnp(self):
        multipart = self.socket.recv_multipart()    # Receive multipart (IDENTITY + payload) message
        self.identity = multipart[0]                # Separate identity, it is a Frame
        message = pickle.loads(multipart[1])
        return message
        # return self.socket.recv()

    def send_capnp(self, msg):
        try:
            content = msg             
            payload = zmq.Frame(content)
            self.socket.send_multipart([self.identity,payload])
            # self.socket.send(msg)
        except ZMQError as e:
            if e.errno == zmq.EAGAIN:
                return False
            else:
                raise
        return True
        
    def getInfo(self):
        return ("ans",self.Name,self.Type,self.host,self.portNum)