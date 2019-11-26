'''
Distributed coordination - Communication ports for the groups.

Created on Feb 23, 2019
Author: riaps
'''

import ctypes
import threading
import zmq
import time
import logging
import struct
import traceback
from riaps.run.port import Port
from riaps.consts.defs import *
from riaps.utils import spdlog_setup
import spdlog
import random
import string
from riaps.run.exc import BuildError,OperationError,PortError
import struct
import collections
from zmq.backend.cython.utils import ZMQError

try:
    import cPickle
    pickle = cPickle
except:
    cPickle = None
    import pickle

class GroupPubPort(Port):
    '''
    Group Publisher port is for publishing application and housekeeping messages for all group members.
    '''
    def __init__(self, parentPart, portName, groupSpec):
        '''
        Constructor
        '''
        super(GroupPubPort,self).__init__(parentPart,portName)
        self.type = groupSpec["message"]
        self.isTimed = groupSpec["timed"]
        self.isLocalPort = False
        self.info = None
    
    def setup(self):
        pass
        
    def setupSocket(self,owner):
        self.setOwner(owner)
        self.socket = self.context.socket(zmq.PUB)
        self.socket.setsockopt(zmq.SNDTIMEO,self.sendTimeout) 
        self.host = ''
        self.portNum = -1
        self.setupCurve(True) 
        globalHost = self.getGlobalIface()
        self.portNum = self.socket.bind_to_random_port("tcp://" + globalHost)
        self.host = globalHost
        self.info = ('gpub',False,self.name,self.type,self.host,self.portNum)
        return self.info
        
    def reset(self):
        pass
    
    def update(self, host, port):
        raise OperationError("Unsupported update() on GroupPubPort")
    
    def getSocket(self):
        return self.socket
    
    def inSocket(self):
        return False
    
    def send_pyobj(self,msg):
        raise OperationError("Unsupported send_pyobj() on GroupPubPort")
        # return self.port_send(msg,True)

    def send(self, msg):
        raise OperationError("Unsupported send() on GroupPubPort")
        # return self.port_send(msg,False)
    
    def sendGroup(self,msgType,msg):
        try:
            msgFrames = [zmq.Frame(msgType)]
            msgFrames += [zmq.Frame(msg)]
            if self.isTimed:
                now = time.time()
                now = struct.pack("d", now)
                nowFrame = zmq.Frame(now)
                msgFrames += [nowFrame]
            self.socket.send_multipart(msgFrames)
        except zmq.error.ZMQError as e:
            raise PortError("send error (%d)" % e.errno, e.errno) from e
        return True
        
    def recv_pyobj(self):
        raise OperationError("attempt to receive through a publish port")
    
    def recv(self):
        raise OperationError("attempt to receive through a publish port")
    
    def getInfo(self):
        return self.info
    
class GroupSubPort(Port):
    '''
    Group subscriber port is for receiving application and housekeeping messages from all group members.
    '''
    def __init__(self, parentPart, portName, groupSpec):
        '''
        Constructor
        '''
        super(GroupSubPort,self).__init__(parentPart,portName)
        self.type = groupSpec["message"]
        self.isTimed = groupSpec["timed"]
        self.deadline = None
        self.isLocalPort = False
        self.pubs = []
        self.sendTime = 0.0
        self.recvTime = 0.0
        self.info = None
    
    def setup(self):
        pass
       
    def setupSocket(self,owner):
        self.setOwner(owner)
        self.socket = self.context.socket(zmq.SUB)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, '')
        self.setupCurve(False)
        self.host = ''
        globalHost = self.getGlobalIface()
        self.portNum = -1 
        self.host = globalHost
        self.info = ('gsub',False,self.name,self.type,self.host)
        return self.info
    
    def reset(self):
        pass
    
    def getSocket(self):
        return self.socket
    
    def inSocket(self):
        return True
    
    def update(self,host,port):
        pubPort = "tcp://" + str(host) + ":" + str(port)
        self.pubs.append((host,port))
        self.socket.connect(pubPort)
    
    def recv_pyobj(self):
        raise OperationError("Unsupported recv_pyobj() on GroupSubPort")
        # return self.port_recv(True)

    def send_pyobj(self,msg):
        raise OperationError("attempt to send through a subscriber port")
    
    def recv(self):
        raise OperationError("Unsupported recv() on GroupSubPort")
        # return self.port_recv(False)
    
    def send(self):
        raise OperationError("attempt to send through a subscriber port")
    
    def recvGroup(self):
        try:
            msgFrames = self.socket.recv_multipart()
        except zmq.error.ZMQError as e:
            raise PortError("recv error (%d)" % e.errno, e.errno) from e
        if self.isTimed:
            self.recvTime = time.time()
        _msgType = msgFrames[0]
        _payload = msgFrames[1]
        if len(msgFrames) == 3:
            rawMsg = msgFrames[2]
            rawTuple = struct.unpack("d", rawMsg)
            self.sendTime = rawTuple[0]
        return msgFrames

    def getInfo(self):
        return self.info
     

class GroupAnsPort(Port):
    '''
    Group answer port is for the leader to receive messages from members members. Based on a DEALER socket.  
    Group-internal communication port for messaging with the leader, no message type, but can be timed. 
    '''
    def __init__(self, parentPart, portName, groupSpec):
        '''
        Constructor
        '''
        super(GroupAnsPort,self).__init__(parentPart,portName)
        self.req_type = 'group-mtl'
        self.rep_type = 'group-mfl'
        self.isTimed = groupSpec["timed"]
        self.isLocalPort = False
        self.identity = None
        self.socket = None
        self.portNum = None
        self.info = None

    def setup(self):
        pass
  
    def setupSocket(self,owner):
        self.setOwner(owner)
        self.socket = self.context.socket(zmq.ROUTER)
        self.socket.setsockopt(zmq.SNDTIMEO,self.sendTimeout)
        self.setupCurve(True)
        globalHost = self.getGlobalIface()
        self.host = globalHost
        self.portNum = None 
        self.info = ('gans',False,self.name,str(self.req_type) + '#' + str(self.rep_type), self.host,self.portNum)
        return self.info

    def update(self):
        raise OperationError("Unsupported update() on GroupAnsPort")
    
    def updatePoller(self,poller):
        if self.portNum != None:
            self.socket.setsockopt(zmq.LINGER, 0)
            self.poller.register(self.self.socket,0)    # Unregister old socket as tainted
            self.socket.close()                         # Close and destroy old socket
            del self.socket
            self.socket = self.context.socket(zmq.ROUTER)   # Create new socket
            self.setupCurve(True)                           # Set up encryption
            self.poller.register(self.socket,zmq.POLLIN)    # Register with poller
        port = self.socket.bind_to_random_port("tcp://%s" % self.host)
        self.portNum = port
        self.info = ('gans',False,self.name,str(self.req_type) + '#' + str(self.rep_type), self.host,self.portNum)
        
    def reset(self):
        pass
    
    def getSocket(self):
        return self.socket
    
    def inSocket(self):
        return True
    
    def get_identity(self):
        return self.identity
    
    def set_identity(self,identity):
        self.identity = identity
        
    def getPortNumber(self):
        return self.portNum
        
    def recvFromMember(self):   
        try:
            msgFrames = self.socket.recv_multipart()    # Receive multipart (IDENTITY + payload) message
        except zmq.error.ZMQError as e:
            raise PortError("recv error (%d)" % e.errno, e.errno) from e
        if self.isTimed:
            self.recvTime = time.time()
        self.identity = msgFrames[0]                # Separate identity
        _msgType = msgFrames[1]
        _payload = msgFrames[2]
        if len(msgFrames) == 4:                     # If we have a send time stamp
            rawMsg = msgFrames[3]
            rawTuple = struct.unpack("d", rawMsg)
            self.sendTime = rawTuple[0]
        return msgFrames[1:]
        
    def sendToMember(self,msgType,msg):
        try:
            sendMsg = [zmq.Frame(self.identity)]    # Identity
            sendMsg += [zmq.Frame(msgType)]
            sendMsg += [zmq.Frame(msg)]             # Take bytearray  
            if self.isTimed:
                now = time.time()
                now = struct.pack("d", now)
                nowFrame = zmq.Frame(now)
                sendMsg += [nowFrame]
            self.socket.send_multipart(sendMsg)
        except zmq.error.ZMQError as e:
            raise PortError("send error (%d)" % e.errno, e.errno) from e
        return True
    
    def recv_pyobj(self):
        raise OperationError("Unsupported recv_pyobj() on GroupAnsPort")
        # return self.ans_port_recv(True)

    def send_pyobj(self,msg): 
        raise OperationError("Unsupported send_pyobj() on GroupAnsPort")
        # return self.ans_port_send(msg,True)     
    
    def recv(self):
        raise OperationError("Unsupported recv() on GroupAnsPort")
        # return self.ans_port_recv(False)

    def send(self, _msg):
        raise OperationError("Unsupported send() on GroupAnsPort")
        # return self.ans_port_send(False)
        
    def getInfo(self):
        return self.info
    

class GroupQryPort(Port):
    '''
    Group query port is for accessing the leader from members. Based on a DEALER socket.  
    Group-internal communication port for messaging with the leader, no message type, but can be timed. 
    '''
    def __init__(self, parentPart, portName, groupSpec):
        '''
        Initialize the query port object.
        '''
        super(GroupQryPort,self).__init__(parentPart,portName)
        
        self.req_type = 'group-mtl'
        self.rep_type = 'group-mfl'
        self.isTimed = groupSpec["timed"]
        self.isLocalPort = False
        self.serverHost = None
        self.serverPort = None
        self.info = None

    def setup(self):
        '''
        Set up the port
        '''
        pass
  
    def setupSocket(self,owner):
        '''
        Set up the socket of the port. 
        Return a tuple suitable for querying the discovery service for the servers (not used currently).
        '''
        self.setOwner(owner)
        self.socket = self.context.socket(zmq.DEALER)
        self.socket.setsockopt_string(zmq.IDENTITY, str(id(self)), 'utf-8')  # FIXME: identity is not unique across nodes
        self.socket.setsockopt(zmq.SNDTIMEO,self.sendTimeout)
        self.setupCurve(False) 
        globalHost = self.getGlobalIface()
        self.portNum = -1 
        self.host = globalHost
        self.info = ('gqry',False,self.name,str(self.req_type) + '#' + str(self.rep_type),self.host)
        return self.info
    
    def reset(self):
        pass
    
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
    
    def update(self,host,port):
        '''
        Update the query port -- connect its socket to a server
        '''
        if self.serverHost == host and self.serverPort == port:
            return
        if self.serverHost != None and self.serverPort != None: # Old connection
            self.socket.setsockopt(zmq.LINGER, 0)
            oldConn = "tcp://" + str(self.serverHost) + ":" + str(self.serverPort)
            self.socket.disconnect(oldConn)
            # Alternate code below - more radical update
            # self.poller.register(self.qry,0)    # Unregister old socket as tainted
            # self.qry.close()                    # Close it
            # del self.qry
            # self.qry = self.context.socket(zmq.DEALER)      # Create new socket 
            # self.qry.setsockopt_string(zmq.IDENTITY, str(id(self)), 'utf-8')
            # self.poller.register(self.qry,zmq.POLLIN)       # Register it
        else:
            pass
        self.serverHost,self.serverPort = host,port
        if self.serverHost != None and self.serverPort != None:
            newConn = "tcp://" + str(self.serverHost) + ":" + str(self.serverPort)
            self.socket.connect(newConn)
    
    def recv_pyobj(self):
        raise OperationError("Unsupported recv_pyobj() on GroupQryPort")
        # return self.port_recv(True)
    
    def send_pyobj(self,msg):
        raise OperationError("Unsupported send_pyobj() on GroupQryPort")
        # return self.port_send(msg,True)              
    
    def recv(self):
        raise OperationError("Unsupported recv() on GroupQryPort")
        # return self.port_recv(False)
    
    def send(self, msg):
        raise OperationError("Unsupported send() on GroupQryPort")
        # return self.port_send(msg,True)     
    
    def sendToLeader(self,msgType,msg):
        if self.serverHost == None or self.serverPort == None:
            return False
        try:
            msgFrames = [zmq.Frame(msgType)]
            msgFrames += [zmq.Frame(msg)]
            if self.isTimed:
                now = time.time()
                now = struct.pack("d", now)
                nowFrame = zmq.Frame(now)
                msgFrames += [nowFrame]
            self.socket.send_multipart(msgFrames)
        except zmq.error.ZMQError as e:
            raise PortError("send error (%d)" % e.errno, e.errno) from e
        return True
        
    def recvFromLeader(self):
        try:
            msgFrames = self.socket.recv_multipart()
        except zmq.error.ZMQError as e:
            raise PortError("recv error (%d)" % e.errno, e.errno) from e
        if self.isTimed:
            self.recvTime = time.time()
        _msgType = msgFrames[0]
        _payload = msgFrames[1]
        if len(msgFrames) == 3:
            rawMsg = msgFrames[2]
            rawTuple = struct.unpack("d", rawMsg)
            self.sendTime = rawTuple[0]
        return msgFrames
    
    def getInfo(self):
        '''
        Retrieve relevant information about this port
        '''
        return self.info
    
    