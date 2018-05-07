'''
Created on Oct 19, 2016

@author: riaps
'''

import os
import zmq
import capnp
from ..proto import disco_capnp
from riaps.consts.defs import *
from .exc import SetupError, OperationError
import logging

class DiscoClient(object):
    '''
    Discovery service client of an actor
    '''
    def __init__(self, parentActor,suffix):
        '''
        Constructor
        '''
        self.logger = logging.getLogger(__name__)
        self.actor = parentActor
        self.suffix = suffix
        self.appName = parentActor.appName
        self.messageNames = parentActor.messageNames
        self.localNames = parentActor.localNames
        self.context = zmq.Context()
        
    def start(self):
        self.logger.info("starting")
        self.socket = self.context.socket(zmq.REQ)
        self.socket.setsockopt(zmq.RCVTIMEO,const.discoEndpointRecvTimeout)
        self.socket.setsockopt(zmq.SNDTIMEO,const.discoEndpointSendTimeout)
        endpoint = const.discoEndpoint
        self.socket.connect(endpoint)    
        self.channel = self.context.socket(zmq.PAIR)

    def registerApp(self):
        self.logger.info("registerApp")
        reqt = disco_capnp.DiscoReq.new_message()
        appMessage = reqt.init('actorReg')
        appMessage.appName = self.appName
        appMessage.version = '0.0.0'
        appMessage.actorName = self.actor.name
        appMessage.pid = self.actor.pid
                  
        msgBytes = reqt.to_bytes()
        
        try:
            self.socket.send(msgBytes)
        except Exception as e:
            self.logger.error("Unable to register app with discovery: %s" % e.args)
            self.socket.close()
            self.socket = None
            return
        
        try:
            respBytes = self.socket.recv()
        except Exception as e:
            self.logger.error("No response from discovery service: %s" % e.args)
            self.socket.close()
            self.socket = None
            return
        
        resp = disco_capnp.DiscoRep.from_bytes(respBytes)
        
        which = resp.which()
        if which == 'actorReg':
            respMessage = resp.actorReg
            status = respMessage.status
            port = respMessage.port
            if status == 'ok':
                self.logger.info("connecting to 127.0.0.1:%s" % str(port))
                self.channel.connect("tcp://127.0.0.1:" + str(port))
            else:
                raise SetupError("Error response from disco service at app registration")
        else:
            raise SetupError("Unexpected response from disco service at app registration")
        return
     
    def reconnect(self):
        self.logger.info('reconnect')
        endpoint = const.discoEndpoint
        self.socket.disconnect(endpoint)
        self.socket.connect(endpoint)
        self.channel = self.context.socket(zmq.PAIR)
        self.registerApp()
        self.logger.info('reconnected')
        
    def handleRegReq(self,bundle):
        self.logger.info("handleRegReq: %s" % str(bundle))
        if self.socket == None:
            self.logger.info("No disco service - skipping registration: %s", str(bundle))
            return 
        (partName,partType,kind,isLocal,portName,portType,portHost,portNum) = bundle[0:8]
        # All interactions below go via the REQ/REP socket ; the channel is for server pushes
        req = disco_capnp.DiscoReq.new_message()
        reqMsg = req.init('serviceReg')
        reqMsgPath = reqMsg.path
        reqMsg.socket.host = self.actor.localHost if isLocal else self.actor.globalHost
        reqMsg.socket.port = portNum
        reqMsg.pid = os.getpid()
        reqMsgPath.appName = self.appName
        reqMsgPath.actorName = self.actor.name
        reqMsgPath.msgType = portType 
        reqMsgPath.kind = kind
        reqMsgPath.scope = 'local' if isLocal else 'global'
        msgBytes = req.to_bytes()
        self.socket.send(msgBytes)
        try:
            repBytes = self.socket.recv()
        except Exception as e:
            raise SetupError("No response from disco service : {1}".format(e.errno, e.strerror))
        rep = disco_capnp.DiscoRep.from_bytes(repBytes)
        which = rep.which()
        if which == 'serviceReg':
            repMessage = rep.serviceReg
            status = repMessage.status
            if status == 'err':
                raise SetupError("Error response from disco service at service registration")
            else:
                pass
        else:
            raise SetupError("Unexpected response from disco service at service registration")
        return
    
    def handleLookupReq(self,bundle):
        self.logger.info("handleLookupReq: %s" % str(bundle))
        if self.socket == None:
            self.logger.info("No disco service - skipping lookup: %s", str(bundle))
            return []
        (partName,_partType,kind,isLocal,portName,portType) = bundle[0:6]
        # All interactions below go via the REQ/REP socket ; the channel is for server pushes
        req = disco_capnp.DiscoReq.new_message()
        reqMsg = req.init('serviceLookup')
        reqMsgPath = reqMsg.path
        reqMsgPath.appName = self.appName
        reqMsgPath.actorName = self.actor.name
        reqMsgPath.msgType = portType 
        reqMsgPath.kind = kind
        reqMsgPath.scope = 'local' if isLocal else 'global'
        reqMsgClient = reqMsg.client
        reqMsgClient.actorHost = self.actor.getGlobalIface()
        reqMsgClient.actorName = self.actor.name
        reqMsgClient.instanceName = partName
        reqMsgClient.portName = portName
        
        msgBytes = req.to_bytes()
        self.socket.send(msgBytes)
        try:
            repBytes = self.socket.recv()
        except Exception as e:
            raise SetupError("No response from disco service : {1}".format(e.errno, e.strerror))
            raise
        rep = disco_capnp.DiscoRep.from_bytes(repBytes)
        which = rep.which()
        returnValue = []
        if which == 'serviceLookup':
            repMessage = rep.serviceLookup
            status = repMessage.status
            if status == 'err':
                raise SetupError('Unable to lookup service')
            sockets = repMessage.sockets
            for sock in sockets:
                host = sock.host
                port = sock.port
                returnValue.append((partName,portName,host,port))
            else:
                pass
        else:
            raise SetupError("Service lookup error - bad response")
        return returnValue
 
        
    def registerEndpoint(self,bundle):
        self.logger.info("registerEndpoint: %s" % str(bundle))
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
        kind = bundle[2]
        #(partName,partType,kind,isLocal,portName,portType) = bundle[0:6]
        # All interactions below go via the REQ/REP socket ; the channel is for server pushes
        result = []
        # Update component means: add command to component's message queue
        if kind == 'pub' or kind == 'srv' or kind == 'rep' or kind == 'ans':
            # Register publisher or server port
            self.handleRegReq(bundle)
        elif kind == 'sub' or kind == 'clt' or kind == 'req' or kind == 'qry':
            # Request pub(s) or srv(s);  update component
            result = self.handleLookupReq(bundle)
        else:
            raise SetupError("Invalid registration message")
        return result

    def terminate(self):
        self.logger.info("terminating")
        if self.socket == None:
            self.logger.info("No disco service - skipping termination")
            return
        req = disco_capnp.DiscoReq.new_message()
        reqt = disco_capnp.DiscoReq.new_message()
        appMessage = reqt.init('actorUnreg')
        appMessage.appName = self.appName
        appMessage.version = '0.0.0'
        appMessage.actorName = self.actor.name
        appMessage.actorName = self.actor.pid
                  
        msgBytes = reqt.to_bytes()
        
        try:
            self.socket.send(msgBytes)
        except Exception as e:
            self.logger.error("Unable to unregister app with discovery: %s" % e.args)
            self.socket.close()
            self.socket = None
            return
        
        try:
            respBytes = self.socket.recv()
        except Exception as e:
            self.logger.error("No response from discovery service: %s" % e.args)
            self.socket.close()
            self.socket = None
            return
        
        resp = disco_capnp.DiscoRep.from_bytes(respBytes)
        
        which = resp.which()
        if which == 'actorUnreg':
            respMessage = resp.actorUnreg
            status = respMessage.status
            port = respMessage.port
            if status == 'ok':
                self.logger.info("disconnecting 127.0.0.1: %s" % str(port))
                self.channel.disconnect("tcp://127.0.0.1:" + str(port))
            else:
                raise SetupError("Error response from disco service at app unregistration")
        else:
            raise SetupError("Unexpected response from disco service at app unregistration")
        self.logger.info("terminated")
    
