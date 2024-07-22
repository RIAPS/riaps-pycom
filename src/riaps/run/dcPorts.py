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
from riaps.run.port import Port,PortInfo,PortScope,BindPort,ConnPort
from riaps.consts.defs import *
from riaps.utils import spdlog_setup
import spdlog
import random
import string
from riaps.run.exc import BuildError, OperationError, PortError
import struct
import collections
from zmq.backend.cython.utils import ZMQError

try:
    import cPickle
    pickle = cPickle
except:
    cPickle = None
    import pickle

class GroupSimplexPort(Port):
    def __init__(self, parentComponent, portName, groupSpec):
        '''
        GroupSimplexPort constructor
        '''
        super().__init__(parentComponent, portName)
        self.type = groupSpec["message"]
        self.isTimed = groupSpec["timed"]
        self.portScope = PortScope.GLOBAL
        self.msgType = self.type
        self.info = None
            
class GroupPubPort(BindPort,GroupSimplexPort):
    '''
    Group Publisher port is for publishing application and housekeeping messages for all group members.
    '''

    def __init__(self, parentPart, portName, groupSpec):
        '''
        Constructor
        '''
        super(GroupPubPort, self).__init__(parentPart, portName,groupSpec)
           
    def setup(self):
        pass
        
    def setupSocket(self, owner):
        return self.setupBindSocket(owner, zmq.PUB, 'gpub',[(zmq.SNDTIMEO,self.sendTimeout)])
    
        # self.setOwner(owner)
        # self.socket = self.context.socket(zmq.PUB)
        # self.socket.setsockopt(zmq.SNDTIMEO, self.sendTimeout) 
        # self.host = ''
        # self.portNum = -1
        # self.setupCurve(True) 
        # globalHost = self.getGlobalIface()
        # self.bindAddr = "tcp://" + globalHost
        # self.portNum = self.socket.bind_to_random_port(self.bindAddr)
        # self.host = globalHost
        # self.info = PortInfo(portKind='gpub', portScope=self.portScope, portName=self.name, 
        #                      msgType=self.type, 
        #                      portHost=self.host, portNum=self.portNum)
        # return self.info
        
    def closeSocket(self):
        self.closeBindSocket()
        
    def reset(self):
        pass
    
    def update(self, host, port):
        raise OperationError("Unsupported update() on GroupPubPort")
    
    def getSocket(self):
        return self.socket
    
    def inSocket(self):
        return False
    
    def send_pyobj(self, msg):
        raise OperationError("Unsupported send_pyobj() on GroupPubPort")
        # return self.port_send(msg,True)

    def send(self, msg):
        raise OperationError("Unsupported send() on GroupPubPort")
        # return self.port_send(msg,False)
    
    def sendGroup(self, msgType, msg):
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
   
class GroupSubPort(ConnPort,GroupSimplexPort):
    '''
    Group subscriber port is for receiving application and housekeeping messages from all group members.
    '''

    def __init__(self, parentPart, portName, groupSpec):
        '''
        Constructor
        '''
        super(GroupSubPort, self).__init__(parentPart, portName,groupSpec)
        # self.type = groupSpec["message"]
        # self.isTimed = groupSpec["timed"]
        self.deadline = None
        # self.portScope = PortScope.GLOBAL
        # self.pubs = []
        self.sendTime = 0.0
        self.recvTime = 0.0
        self.info = None
    
    def setup(self):
        pass
       
    def setupSocket(self, owner):
        return self.setupConnSocket(owner,zmq.SUB,'gsub',[(zmq.SUBSCRIBE,'')])
        # self.setOwner(owner)
        # self.socket = self.context.socket(zmq.SUB)
        # self.socket.setsockopt_string(zmq.SUBSCRIBE, '')
        # self.setupCurve(False)
        # self.host = ''
        # globalHost = self.getGlobalIface()
        # self.portNum = -1 
        # self.host = globalHost
        # self.info = PortInfo(portKind='gsub', portScope=self.portScope, portName=self.name, 
        #                      msgType=self.type, 
        #                      portHost=self.host, portNum=self.portNum)
        # return self.info
    
    def closeSocket(self):
        self.closeConnSocket()
        
    def reset(self):
        self.resetConnSocket(zmq.SUB,[(zmq.SUBSCRIBE,'')])
    
    def getSocket(self):
        return self.socket
    
    def inSocket(self):
        return True
    
    # def update(self, host, port):
    #     pubPort = "tcp://" + str(host) + ":" + str(port)
    #     self.pubs.append((host, port))
    #     self.socket.connect(pubPort)
    
    def recv_pyobj(self):
        raise OperationError("Unsupported recv_pyobj() on GroupSubPort")
        # return self.port_recv(True)

    def send_pyobj(self, msg):
        raise OperationError("attempt to send through a subscriber port")
    
    def recv(self):
        raise OperationError("Unsupported recv() on GroupSubPort")
        # return self.port_recv(False)
    
    def send(self, _msg):
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
     
class GroupDuplexPort(Port):
    def __init__(self, parentComponent, portName, groupSpec):
        '''
        GroupDuplexPort constructor
        '''
        super().__init__(parentComponent, portName)
        self.req_type = 'group-mtl'
        self.rep_type = 'group-mfl'
        self.isTimed = groupSpec["timed"]
        self.portScope = PortScope.GLOBAL
        self.msgType = str(self.req_type) + '#' + str(self.rep_type)
        self.info = None
        
class GroupAnsPort(BindPort,GroupDuplexPort):
    '''
    Group answer port is for the leader to receive messages from members. Based on a DEALER socket.  
    Group-internal communication port for messaging with the leader, no message type, but can be timed. 
    '''

    def __init__(self, parentPart, portName, groupSpec):
        '''
        Constructor
        '''
        super(GroupAnsPort, self).__init__(parentPart, portName, groupSpec)
        # self.req_type = 'group-mtl'
        # self.rep_type = 'group-mfl'
        # self.isTimed = groupSpec["timed"]
        # self.portScope = PortScope.GLOBAL
        self.identity = None
        self.socket = None
        self.portNum = None
        self.bindAddr = None
        self.poller = None
        # self.info = None

    def setup(self):
        pass
  
    def setupSocket(self, owner):   
        self.setOwner(owner)
        self.socket = self.context.socket(zmq.ROUTER)
        self.socket.setsockopt(zmq.SNDTIMEO, self.sendTimeout)
        self.setupCurve(True)
        globalHost = self.getGlobalIface()
        self.host = globalHost
        self.portNum = None 
        self.info = PortInfo(portKind='gans', portScope=self.portScope, portName=self.name, 
                             msgType=str(self.req_type) + '#' + str(self.rep_type), 
                             portHost=self.host, portNum=self.portNum)
        return self.info

    def closeSocket(self):
        if self.portNum != None:
            self.socket.setsockopt(zmq.LINGER, 0)
            self.socket.unbind(self.bindAddr)
            self.portNum = None
        if self.socket != None:
            self.socket.close()  # Close and destroy old socket
            del self.socket
            self.socket = None
        
    def update(self):
        raise OperationError("Unsupported update() on GroupAnsPort")
    
    def updatePoller(self, poller):
        if self.portNum != None:
            self.socket.setsockopt(zmq.LINGER, 0)
            poller.unregister(self.self.socket)     # Unregister old socket as tainted
            self.socket.close()                     # Close and destroy old socket
            del self.socket
            self.socket = self.context.socket(zmq.ROUTER)  # Create new socket
            self.setupCurve(True)  # Set up encryption
            poller.register(self.socket, zmq.POLLIN)  # Register with poller
        bindAddr = "tcp://" + self.host
        self.portNum = self.socket.bind_to_random_port(bindAddr)
        self.bindAddr = "%s:%d" % (bindAddr, self.portNum)
        self.info = PortInfo(portKind='gans', portScope=self.portScope, portName=self.name, 
                             msgType=str(self.req_type) + '#' + str(self.rep_type), 
                             portHost=self.host, portNum=self.portNum)
        
    def reset(self):
        pass
    
    def getSocket(self):
        return self.socket
    
    def inSocket(self):
        return True
    
    def get_identity(self):
        return self.identity
    
    def set_identity(self, identity):
        self.identity = identity
        
    def getPortNumber(self):
        return self.portNum
        
    def recvFromMember(self): 
        try:
            msgFrames = self.socket.recv_multipart()  # Receive multipart (IDENTITY + payload) message
        except zmq.error.ZMQError as e:
            raise PortError("recv error (%d)" % e.errno, e.errno) from e
        if self.isTimed:
            self.recvTime = time.time()
        self.identity = msgFrames[0]  # Separate identity
        _msgType = msgFrames[1]
        _payload = msgFrames[2]
        if len(msgFrames) == 4:  # If we have a send time stamp
            rawMsg = msgFrames[3]
            rawTuple = struct.unpack("d", rawMsg)
            self.sendTime = rawTuple[0]
        return msgFrames[1:]
        
    def sendToMember(self, msgType, msg):
        try:
            sendMsg = [zmq.Frame(self.identity)]  # Identity
            sendMsg += [zmq.Frame(msgType)]
            sendMsg += [zmq.Frame(msg)]  # Take bytes  
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

    def send_pyobj(self, msg): 
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
    

class GroupQryPort(ConnPort, GroupDuplexPort):
    '''
    Group query port is for accessing the leader from members. Based on a DEALER socket.  
    Group-internal communication port for messaging with the leader, no message type, but can be timed. 
    '''

    def __init__(self, parentPart, portName, groupSpec):
        '''
        Initialize the query port object.
        '''
        super(GroupQryPort, self).__init__(parentPart, portName, groupSpec)
        
        # self.req_type = 'group-mtl'
        # self.rep_type = 'group-mfl'
        # self.isTimed = groupSpec["timed"]
        # self.portScope = PortScope.GLOBAL
        self.serverHost = None
        self.serverPort = None
        self.info = None

    def setup(self):
        '''
        Set up the port
        '''
        pass
  
    def setupSocket(self, owner):
        '''
        Set up the socket of the port. 
        Return a tuple suitable for querying the discovery service for the servers (not used currently).
        '''
        self.setOwner(owner)
        self.socket = self.context.socket(zmq.DEALER)
        self.socket.setsockopt_string(zmq.IDENTITY, str(id(self)), 'utf-8')  # FIXME: identity is not unique across nodes
        self.socket.setsockopt(zmq.SNDTIMEO, self.sendTimeout)
        self.setupCurve(False) 
        globalHost = self.getGlobalIface()
        self.portNum = -1 
        self.host = globalHost
        self.info = PortInfo(portKind='gqry', portScope=self.portScope, portName=self.name, 
                             msgType=str(self.req_type) + '#' + str(self.rep_type), 
                             portHost=self.host, portNum=self.portNum)
        return self.info
    
    def closeSocket(self):
        if self.socket != None:
            if self.serverHost != None and self.serverPort != None:  # Old connection
                self.socket.setsockopt(zmq.LINGER, 0)
                oldConn = "tcp://" + str(self.serverHost) + ":" + str(self.serverPort)
                self.socket.disconnect(oldConn)
            self.socket.close()
            del self.socket
            self.socket = None
    
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
    
    def update(self, host, port):
        '''
        Update the query port -- connect its socket to a server
        '''
        if self.serverHost == host and self.serverPort == port:
            return
        if self.serverHost != None and self.serverPort != None:  # Old connection
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
        self.serverHost, self.serverPort = host, port
        if self.serverHost != None and self.serverPort != None:
            newConn = "tcp://" + str(self.serverHost) + ":" + str(self.serverPort)
            self.socket.connect(newConn)
    
    def recv_pyobj(self):
        raise OperationError("Unsupported recv_pyobj() on GroupQryPort")
        # return self.port_recv(True)
    
    def send_pyobj(self, msg):
        raise OperationError("Unsupported send_pyobj() on GroupQryPort")
        # return self.port_send(msg,True)              
    
    def recv(self):
        raise OperationError("Unsupported recv() on GroupQryPort")
        # return self.port_recv(False)
    
    def send(self, _msg):
        raise OperationError("Unsupported send() on GroupQryPort")
        # return self.port_send(msg,True)     
    
    def sendToLeader(self, msgType, msg):
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
    
