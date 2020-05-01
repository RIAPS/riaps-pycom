'''Base class for all Port objects

'''
import zmq
import time
import struct
from .exc import SetupError,OperationError,PortError
from riaps.utils.config import Config
import logging

try:
    import cPickle
    pickle = cPickle
except:
    cPickle = None
    import pickle
    
class Port(object):
    '''Base class for all Port objects. 
    
        Port objects are used by a component to communicate with other components,
        in the same process, on the same host, or on the same network. Ports
        encapsulate low-level communication objects (zeromq sockets).
        
        :param parentPart: the Part object that owns this port.
        :type parentPart: Part
        
        :param portName: the name of the port (from the model)
        :type portName: str
 
    '''

    def __init__(self, parentPart, portName, portSpec=None):
        '''
        Constructor
        '''
        self.logger = logging.getLogger(__name__)
        self.parent = parentPart
        self.name = portName
        self.index = portSpec.get('index',None) if portSpec else None
        self.context = parentPart.appContext
        (self.public_key,self.private_key) = (parentPart.parent.public_key,parentPart.parent.private_key)
        self.security = (self.public_key != None) and (self.private_key != None)
        self.localIface = None
        self.globalIface = None
        self.sendTimeout = Config.SEND_TIMEOUT
        self.recvTimeout = Config.RECV_TIMEOUT
        self.sendTime = 0.0
        self.recvTime = 0.0
        self.socket = None
        self.isTimed = False
        self.deadline = 0.0
        self.info = None
        self.owner = None
    
    def setupCurve(self,server):
        if self.socket and self.security:
            self.socket.curve_secretkey = self.private_key
            self.socket.curve_publickey = self.public_key
            if server:
                self.socket.curve_server = True
            else:
                self.socket.curve_serverkey = self.public_key
                
    def setupSocket(self,owner):
        ''' Setup the socket. Abstract, subclasses must implement this method.
        
        :param owner: The Component the port belongs to. This operation must be called from the component thread only. 
        :type owner: Component
         
        '''
        pass
    
    def setOwner(self,owner):
        ''' Save owner thread into a data member.
        
        :param owner: The ComponentThread the port is handled in.
        :type owner: ComponentThread
        
        '''
        self.owner = owner
    
    def reset(self):
        ''' Reset the port object. Subclasses can override this method.
        
        Reset is to be used when a send or receive operation fails and the port needs to be re-initialized.  
        '''
        pass
    
    def getDeadline(self):
        ''' Return the deadline parameter associated with the port's operation
        
        :return: Deadline for the operation associated with the port, in seconds. 
        :rtype: float
        
        '''
        return self.deadline

    def getIndex(self):
        ''' Return the index of the port.
        
        For input ports the index is a small integer indicating its position in the port list of the component, for non-input ports it is None.
        The index is used to determine the priority order for the port among all the ports, the concrete value is irrelevant. 
        
        :return: Index value for the port among all input ports.
        :rtype: int
        '''
        return self.index
        
    def getLocalIface(self):
        '''Return the IP address of the local network interface (typically 127.0.0.1)
        
        The operation retrieves the result from the parent actor and caches it.
        
        :return: Local IP address of the form xxx.xxx.xxx.xxx
        :rtype: str
        
        '''
        if self.localIface != None:
            pass
        else:
            self.localIface = self.parent.parent.getLocalIface()
        return self.localIface
    
    def getGlobalIface(self):
        '''Return the IP address of the global network interface
        
        The operation retrieves the result from the parent actor and caches it.
        
        :return: Global IP address of the form xxx.xxx.xxx.xxx
        :rtype: str
        
        '''
        if self.globalIface != None:
            pass
        else:
            self.globalIface = self.parent.parent.getGlobalIface()
        return self.globalIface
    
    def setup(self):
        '''Initialize the port object (after construction but before socket creation).
        Abstract, subclasses must implement this method.
        
        '''
        raise SetupError
            
    def getSocket(self):
        '''Return the socket(s) used by the port object. 
        Abstract, subclasses must implement this method.
        
        :return: a low-level socket
        :rtype: zmq.Socket
        
        '''
        raise SetupError
    
    def inSocket(self):
        '''Return True if the socket can be used for input. 
        Abstract, subclasses must implement this method.
        
        :return: logical value indicating whether the socket is for input.
        :type: bool
        
        '''
        raise SetupError
    
    def getInfo(self):
        '''Retrieve configuration information about the port.
        Abstract, subclasses must implement this method.
        
        :returns: a tuple containing the name of the port's type: 
                req,rep,clt,srv,qry,ans,pub,sub,ins,or tim; the name of the
                port object, and the name of the message type the port handles.  
        :rtype: a tuple (portType, portName, msgType)
        '''
        return ("port",None,None)
    
    def update(self,host,port):
        ''' 
        Update the socket with information from the discovery service.
        Abstract, subclasses must implement this method.
        
        Called when the discovery service notifies the actor about a new
        service provide (e.g. server, publisher, etc.) the port needs to
        connect to. The operation will perform the connection.
        
        :param host: IP address of the service provider
        :type host: str 
        :param port: port number of the service provider
        :type port: int
        
        '''
        raise OperationError("abstract op")
    
    def activate(self):
        '''Activate the port object.
        Subclasses can override this method.
        
        '''
        pass
    
    def deactivate(self):
        '''Deactivate the port object.
        Subclasses can override this method.
        
        '''
        pass
    
    def terminate(self):
        '''Terminate all activities of the port.
        Subclasses can override this method.
        
        '''
        pass
    
    def send_pyobj(self,msg):
        '''Send a Python data object (if possible) out through the port. 
        Abstract, subclasses must implement this method.
        
        The object is serialized using pickle and sent. Messages sent using
        this method are received using the ``recv_pyobj`` method.
         
        :param msg: the message to be sent. 
        :type msg: any Python data type
        
        '''
        pass
    
    def recv_pyobj(self):
        '''Receive a Python data object (if possible) through the port. 
        Abstract, subclasses must implement this method.
        
        The raw message received is deserialized using pickle and returned.
        Messages received this way had to be sent using the ``send_pyobj`` method.
        
        :return: a Python data object
        :type: any Python data type
        
        '''
        return None

    def send_capnp(self,msg):
        '''DEPRECATED. Send a byte array (if possible) out through the port
        '''
        self.logger.warning("send_capnp: deprecated, use send() instead")
        pass
    
    def recv_capnp(self):
        '''DEPRECATED. Receive an object (if possible) through the port
        '''
        self.logger.warning("recv_capnp: deprecated, use recv() instead")
        return None
    
    def send(self,msg):
        '''Send a byte array (if possible) out through the port.

        Used for sending a message that has been serialized into bytes previously.
        
        :param msg: the message packed into a bytes
        :rtype: bytes
        
        '''
        pass
    
    def recv(self):
        '''Receive a byte array (if possible) through the port
        
        Used for receiving a message that is subsequently deserialized.
        
        :return: a message packed into a bytes.
        :rtype: bytes
        
        '''
        return None
    
    def port_send(self,msg,is_pyobj):
        '''Lowest level message sending operation.
        Subclasses can override this operation.
        
        If the message is to be sent as a Python object, it is pickled; otherwise
        it is assumed to be a bytes. The message is packed into a frame, and, 
        if the port is 'timed' a current timestamp is appended as another frame.
        The message is sent as a multi-part message. 
        
        :param msg: message to be sent
        :type msg: either a bytes or any Python data object  
        :param is_pyobj: flag to indicate if the message is a Python object.
        :type is_pyobj: bool 
        
        :return: True
        
        :except: Throws a ``PortError`` exception when the underlying network operation fails.  
           
        '''
        try:
            if is_pyobj:
                sendMsg = [zmq.Frame(pickle.dumps(msg))]
            else:
                sendMsg = [zmq.Frame(msg)]
            if self.isTimed:
                now = time.time()
                now = struct.pack("d", now)
                nowFrame = zmq.Frame(now)
                sendMsg += [nowFrame]
            self.socket.send_multipart(sendMsg)
        except zmq.error.ZMQError as e:
            raise PortError("send error (%d)" % e.errno, e.errno) from e
        return True
    
    def port_recv(self,is_pyobj):
        '''Lowest level message receiving operation.
        Subclasses can override this operation.
        
        The message is received as a multi-part message.If the receiving port is
        timed, the current timestamp is saved as the time of message reception.
        If the message is to be received as a Python object, it is unpickled,
        otherwise the message is returned as is (as a bytes).
        If the message included a timestamp, it is retrieved and saved as the
        time of message sending.         
 
        :param is_pyobj: flag to indicate if the expected message is a Python data object.
        :type is_pyobj: bool 
        
        :return: the message received 
        :type msg: either a bytes or any Python data object 
        
        :except: Throws a ``PortError`` exception when the underlying network operation fails.  
           
        '''
        try:
            msgFrames = self.socket.recv_multipart()
        except zmq.error.ZMQError as e:
            raise PortError("recv error (%d)" % e.errno, e.errno) from e
        if self.isTimed:
            self.recvTime = time.time()
        if is_pyobj:
            result = pickle.loads(msgFrames[0])
        else:
            result = msgFrames[0]
        if len(msgFrames) == 2:
            rawMsg = msgFrames[1]
            rawTuple = struct.unpack("d", rawMsg)
            self.sendTime = rawTuple[0]
        return result
        
    def get_recvTime(self):
        ''' Return the timestamp taken at the last receive operation.
        
        :return: time of the last message receive operation
        :rtype: float 
        '''
        return self.recvTime
    
    def get_sendTime(self):
        ''' Return the timestamp of the sending time of the last message receive.
        
        :return: time when the last message received was sent  
        :rtype: float 
        
        '''
        return self.sendTime
    
    def get_recv_timeout(self):
        '''Retrieve the receive timeout parameter for the port.
        
        Receive timeout determines how long a receive operation will block before
        throwing a PortError.EAGAIN exception. None means infinite timeout. 
        
        :return: None (if no timeout is set) or the timeout value in seconds. 
        :rtype: None or float
        '''
        rto = None if self.recvTimeout == -1 else self.recvTimeout * 0.001
        return rto
        
    def get_send_timeout(self):
        '''Retrieve the send timeout parameter for the port.
        
        Send timeout determines how long a send operation will block before
        throwing a PortError.EAGAIN exception. None means infinite timeout.
         
        :return: None (if no timeout is set) or the timeout value in seconds. 
        :rtype: None or float
        '''
        sto = None if self.sendTimeout == -1 else self.sendTimeout * 0.001
        return sto
    
    def set_recv_timeout(self,rto):
        '''Set the receive timeout for the port.
        
        Receive timeout determines how long a receive operation will block before
        throwing a PortError.EAGAIN exception. None means infinite timeout. 
        
        :param rto: None (if no timeout is set) or the timeout value in seconds. 
        :type rto: None or float
        
        '''
        assert rto == None or (type(rto) == float and rto >= 0.0)
        self.recvTimeout = -1 if rto == None else int(rto * 1000)
        self.socket.setsockopt(zmq.RCVTIMEO,self.recvTimeout)

    def set_send_timeout(self,sto):
        '''Set the send timeout for the port.
        
        Send timeout determines how long a send operation will block before
        throwing a PortError.EAGAIN exception. None means infinite timeout. 
        
        :param sto: None (if no timeout is set) or the timeout value in seconds. 
        :type sto: None or float
        
        '''
        assert sto == None or (type(sto) == float and sto >= 0.0)
        self.sendTimeout = -1 if sto == None else int(sto * 1000)
        self.socket.setsockopt(zmq.SNDTIMEO,self.sendTimeout)
    
