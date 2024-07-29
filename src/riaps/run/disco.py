'''
Created on Oct 19, 2016

@author: riaps
'''

import os
import zmq
import capnp
from ..proto import disco_capnp
from .port import PortInfo,PortScope
from riaps.consts.defs import *
from .exc import SetupError, OperationError
import logging


class DiscoClient(object):
    '''
    Discovery service client of an actor
    '''

    def __init__(self, parentActor, suffix):
        '''
        Constructor
        '''
        self.logger = logging.getLogger(__name__)
        self.actor = parentActor
        self.suffix = suffix
        self.appName = parentActor.appName
        self.messageNames = parentActor.messageNames
        self.localNames = parentActor.localNames
        self.internalNames = parentActor.internalNames
        self.context = zmq.Context()
        self.pendingRpc = False
        
    def start(self):
        self.logger.info("starting")
        self.socket = self.context.socket(zmq.REQ)
        self.socket.setsockopt(zmq.RCVTIMEO, const.discoEndpointRecvTimeout)
        self.socket.setsockopt(zmq.SNDTIMEO, const.discoEndpointSendTimeout)
        endpoint = const.discoEndpoint
        self.socket.connect(endpoint)    
        self.channel = self.context.socket(zmq.PAIR)

    def sendToDisco(self,msgBytes,loc,shut):
        try:
            self.socket.send(msgBytes)
            return True
        except Exception as e:
            self.logger.error("%s: send to disco failed: %s" % (loc,str(e.args)))
            if shut:
                self.socket.close()
                self.socket = None
            return False

    def recvFromDisco(self,loc,shut):
        try:
            respBytes = self.socket.recv()
            return respBytes
        except Exception as e:
            self.logger.error("%s: recv from disco failed: %s" % (loc,str(e.args)))
            if shut:
                self.socket.close()
                self.socket = None
            return None
    
    def rpcDisco(self,msgBytes,loc,shut):
        if self.sendToDisco(msgBytes,loc,shut) is False: 
            raise SetupError("%s: Can't send to disco" % loc)
        self.pendingRpc = True
        respBytes = self.recvFromDisco(loc,True)
        self.pendingRpc = False
        if respBytes is None: 
            raise SetupError("%s: Can't receive from disco" %loc)
        return respBytes
        
    def registerActor(self):
        self.logger.info("registerActor")
        reqt = disco_capnp.DiscoReq.new_message()
        appMessage = reqt.init('actorReg')
        appMessage.appName = self.appName
        appMessage.version = '0.0.0'
        appMessage.actorName = self.actor.name
        appMessage.pid = self.actor.pid
        appMessage.isDevice = self.actor.isDevice()
                  
        msgBytes = reqt.to_bytes()
        respBytes = self.rpcDisco(msgBytes,"registerActor",True)
        with disco_capnp.DiscoRep.from_bytes(respBytes) as resp:
            which = resp.which()
            if which == 'actorReg':
                respMessage = resp.actorReg
                status = respMessage.status
                port = respMessage.port
                if status == 'ok':
                    self.logger.info("registerActor:connecting to 127.0.0.1:%s" % str(port))
                    self.channel.connect("tcp://127.0.0.1:" + str(port))
                else:
                    raise SetupError("registerActor: Error response from disco")
            else:
                raise SetupError("registerActor: Unexpected response from disco")
        return
     
    def reconnect(self):
        self.logger.info('reconnect')
        endpoint = const.discoEndpoint
        self.socket.disconnect(endpoint)
        self.socket.connect(endpoint)
        self.channel = self.context.socket(zmq.PAIR)
        self.registerActor()
        self.logger.info('reconnected')
        
    def handleRegReq(self, bundle):
        self.logger.info("handleRegReq: %s" % str(bundle))
        if self.socket == None:
            self.logger.error("handleRegReq: No disco - %s", str(bundle))
            return
        prefix,portInfo = bundle
        partName, partType = prefix
        portKind, portScope, portName, msgType, portHost, portNum = portInfo
        # (partName, partType, kind, isLocal, portName, portType, portHost, portNum) = bundle[0:8]
        # All interactions below go via the REQ/REP socket ; the channel is for server pushes
        req = disco_capnp.DiscoReq.new_message()
        reqMsg = req.init('serviceReg')
        reqMsgPath = reqMsg.path
        reqMsg.socket.host = self.actor.globalHost if portScope == PortScope.GLOBAL else self.actor.localHost
        reqMsg.socket.port = portNum
        reqMsg.pid = os.getpid()
        reqMsgPath.appName = self.appName
        reqMsgPath.actorName = self.actor.name
        reqMsgPath.msgType = msgType 
        reqMsgPath.kind = portKind
        reqMsgPath.scope = portScope.scope()
        
        msgBytes = req.to_bytes()
        respBytes = self.rpcDisco(msgBytes,"handleRegReq",True)
        with disco_capnp.DiscoRep.from_bytes(respBytes) as resp:          
            which = resp.which()
            if which == 'serviceReg':
                repMessage = resp.serviceReg
                status = repMessage.status
                if status == 'err':
                    raise SetupError("handleRegReq: Error response from disco")
                else:
                    pass
            else:
                raise SetupError("handleRegReq: Unexpected response from disco")
        return
    
    def handleLookupReq(self, bundle):
        self.logger.info("handleLookupReq: %s" % str(bundle))
        if self.socket == None:
            self.logger.info("handleLookupReq: No disco - %s", str(bundle))
            return []
        prefix,portInfo = bundle
        partName, _partType = prefix
        portKind, portScope, portName, msgType, _portHost, _portNum = portInfo
        # (partName, _partType, kind, isLocal, portName, portType) = bundle[0:6]
        # All interactions below go via the REQ/REP socket ; the channel is for server pushes
        req = disco_capnp.DiscoReq.new_message()
        reqMsg = req.init('serviceLookup')
        reqMsgPath = reqMsg.path
        reqMsgPath.appName = self.appName
        reqMsgPath.actorName = self.actor.name
        reqMsgPath.msgType = msgType 
        reqMsgPath.kind = portKind
        reqMsgPath.scope = portScope.scope()
        reqMsgClient = reqMsg.client
        reqMsgClient.actorHost = self.actor.getGlobalIface()
        reqMsgClient.actorName = self.actor.name # "%s.%s" % (self.actor.name,self.actor.iName) if self.actor.isDevice() else self.actor.name
        reqMsgClient.instanceName = partName
        reqMsgClient.portName = portName
        
        msgBytes = req.to_bytes()
        respBytes = self.rpcDisco(msgBytes,"handleLookupReq",True)
        returnValue = []
        with disco_capnp.DiscoRep.from_bytes(respBytes) as resp:
            which = resp.which()
            if which == 'serviceLookup':
                repMessage = resp.serviceLookup
                status = repMessage.status
                if status == 'err':
                    raise SetupError('handleLookupReq: error response from disco')
                sockets = repMessage.sockets
                for sock in sockets:
                    host = sock.host
                    port = sock.port
                    returnValue.append((partName, portName, host, port))
                else:
                    pass
            else:
                raise SetupError("handleLookupReq: Bad response from disco")
        return returnValue
    
    def handleUnregReq(self, bundle):
        self.logger.info("handleUnregReq: %s" % str(bundle))
        if self.socket == None:
            self.logger.error("handleUnregReq: No disco - %s", str(bundle))
            return
        prefix,portInfo = bundle
        partName, partType = prefix
        portKind, portScope, portName, msgType, portHost, portNum = portInfo
        # (partName, partType, kind, isLocal, portName, portType, portHost, portNum) = bundle[0:8]
        # All interactions below go via the REQ/REP socket ; the channel is for server pushes
        req = disco_capnp.DiscoReq.new_message()
        reqMsg = req.init('serviceUnreg')
        reqMsgPath = reqMsg.path
        reqMsg.socket.host = self.actor.globalHost if portScope == PortScope.GLOBAL else self.actor.localHost
        reqMsg.socket.port = portNum
        reqMsg.pid = os.getpid()
        reqMsgPath.appName = self.appName
        reqMsgPath.actorName = self.actor.name
        reqMsgPath.msgType = msgType 
        reqMsgPath.kind = portKind
        reqMsgPath.scope = portScope.scope()
        
        msgBytes = req.to_bytes()
        respBytes = self.rpcDisco(msgBytes,"handleUnregReq",True)
        
        with disco_capnp.DiscoRep.from_bytes(respBytes) as resp:  
            which = resp.which()
            if which == 'serviceUnreg':
                repMessage = resp.serviceUnreg
                status = repMessage.status
                if status == 'err':
                    raise SetupError("handleUnregReq: Error response from disco")
                else:
                    pass
            else:
                raise SetupError("handleUnregReq: Unexpected response from disco")
        return
    
    def handleUnlookupReq(self, bundle):
        self.logger.info("handleUnlookupReq: %s" % str(bundle))
        if self.socket == None:
            self.logger.info("handleUnlookupReq: No disco - %s", str(bundle))
            return []
        prefix,portInfo = bundle
        partName, _partType = prefix
        portKind, portScope, portName, msgType, _portHost, _portNum = portInfo
        # (partName, _partType, kind, isLocal, portName, portType) = bundle[0:6]
        # All interactions below go via the REQ/REP socket ; the channel is for server pushes
        req = disco_capnp.DiscoReq.new_message()
        reqMsg = req.init('serviceUnlookup')
        reqMsgPath = reqMsg.path
        reqMsgPath.appName = self.appName
        reqMsgPath.actorName = self.actor.name
        reqMsgPath.msgType = msgType 
        reqMsgPath.kind = portKind
        reqMsgPath.scope = portScope.scope()
        reqMsgClient = reqMsg.client
        reqMsgClient.actorHost = self.actor.getGlobalIface()
        reqMsgClient.actorName = self.actor.name # "%s.%s" % (self.actor.name,self.actor.iName) if self.actor.isDevice() else self.actor.name
        reqMsgClient.instanceName = partName
        reqMsgClient.portName = portName
        
        msgBytes = req.to_bytes()
        respBytes = self.rpcDisco(msgBytes,"handleUnlookupReq",True)
        returnValue = []
        with disco_capnp.DiscoRep.from_bytes(respBytes) as resp:
            which = resp.which()
            if which == 'serviceUnlookup':
                repMessage = resp.serviceUnlookup
                status = repMessage.status
                if status == 'err':
                    raise SetupError('handleUnlookupReq: error response from disco')
                else:
                    pass
            else:
                raise SetupError("handleUnlookupReq: Bad response from disco")
        return returnValue
    
    def registerEndpoint(self, bundle):
        # bundle = [(partName,partTypeName),PortInfo]
        self.logger.info("registerEndpoint: %r", bundle)
        # print ("DiscoClient.registerEndpoint",bundle)
        # Prefix: (partName, partType)
        # (pub,local,name,type,host,port)
        # (sub,local,name,type,host)
        # (clt,local,name,(req,rep),host)
        # (srv,local,name,(req,rep),host,port)
        # (req,local,name,(req,rep),host)
        # (rep,local,name,(req,rep),host,port)
        # (qry,local,name,(req,rep),host)
        # (ans,local,name,(req,rep),host,port)
        _prefix,portInfo = bundle
        portKind = portInfo.portKind
        # All interactions below go via the REQ/REP socket ; the channel is for server pushes
        result = []
        # Update component means: add command to component's message queue
        if portKind in {'pub', 'srv', 'rep', 'ans'}:
            # Register publisher or server port
            self.handleRegReq(bundle)
        elif portKind in {'sub', 'clt', 'req', 'qry'}:
            # Request pub(s) or srv(s);  update component
            result = self.handleLookupReq(bundle)
        else:
            raise SetupError("Invalid registration message")
        return result

    def registerGroup(self, bundle):
        self.logger.info("registerGroup: %s" % str(bundle))
        _key, groupType, groupName, messageType, host, pubPort, partName, partType, portName = bundle
        msgType = messageType + '@' + groupType + '.' + groupName    
        regReqBundle = [(partName, partType), 
                        PortInfo(portKind="gpub", portScope=PortScope.GLOBAL, 
                                 portName=portName, msgType=msgType, 
                                 portHost=host, portNum=pubPort)]
        lookupReqBundle = [(partName, partType), 
                           PortInfo(portKind="gsub", portScope=PortScope.GLOBAL,
                                    portName=portName, msgType=msgType,
                                    portHost='',portNum=0)]  
        # (1) lookupReq -> (2) regReq
        result = self.handleLookupReq(lookupReqBundle)
        self.handleRegReq(regReqBundle)
        return result
    
    def unregisterGroup(self, bundle):
        self.logger.info("unregisterGroup: %s" % str(bundle))
        _key, groupType, groupName, messageType, host, pubPort, partName, partType, portName = bundle
        msgType = messageType + '@' + groupType + '.' + groupName    
        unregReqBundle = [(partName, partType),
                            PortInfo(portKind="gpub", portScope=PortScope.GLOBAL, 
                                     portName=portName,msgType=msgType, 
                                     portHost=host, portNum=pubPort)]
        unlookupReqBundle = [(partName, partType),
                                PortInfo(portKind="gsub", portScope=PortScope.GLOBAL,
                                         portName=portName,msgType=msgType,
                                         portHost='',portNum=0)]  
        # (1) unlookupReq -> (2) unreqReq
        result = self.handleUnlookupReq(unlookupReqBundle)
        self.handleUnregReq(unregReqBundle)
        return result
    
    def terminate(self):
        self.logger.info("terminating")
        if self.socket == None:
            self.logger.info("terminate: No discovery service - skipping termination")
            return
        reqt = disco_capnp.DiscoReq.new_message()
        appMessage = reqt.init('actorUnreg')
        appMessage.appName = self.appName
        appMessage.version = '0.0.0'
        appMessage.actorName = self.actor.name 
        # "%s.%s" % (self.actor.name,self.actor.iName) if self.actor.isDevice() else self.actor.name
        appMessage.pid = self.actor.pid
                  
        msgBytes = reqt.to_bytes()
        
        try:
            if self.pendingRpc:             # Discard pending Rpc result
                self.logger.info("terminate: pending rpc")
                _discard = self.recvFromDisco("unregister",True) 
            self.logger.info("terminate: unregistering")
            respBytes = self.rpcDisco(msgBytes,"unregister",True)
            
            with disco_capnp.DiscoRep.from_bytes(respBytes) as resp:
                which = resp.which()
                if which == 'actorUnreg':
                    respMessage = resp.actorUnreg
                    status = respMessage.status
                    port = respMessage.port
                    if status == 'ok':
                        self.logger.info("terminate: disconnecting 127.0.0.1:%s" % str(port))
                        try:
                            self.channel.disconnect("tcp://127.0.0.1:" + str(port))
                        except:
                            pass
        except:
            pass                # Ignore all errors if disco is not running anymore

        self.logger.info("terminated")
    
