'''
Created on Oct 19, 2016

@author: riaps
'''

import zmq
import capnp
from ..proto import disco_capnp
from riaps.consts.defs import *
from .exc import SetupError
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
        self.socket.setsockopt(zmq.RCVTIMEO,const.discoEndpointTimeout)
        endpoint = const.discoEndpoint + self.suffix
        self.socket.connect(endpoint)    
        self.channel = self.context.socket(zmq.PAIR)

    def registerApp(self):
        self.logger.info("registerApp")
        reqt = disco_capnp.DiscoReq.new_message()
        appMessage = reqt.init('actorReg')
        appMessage.appName = self.appName
        appMessage.version = '0.0.0'
        appMessage.actorName = self.actor.name
                  
        msgBytes = reqt.to_bytes()
        self.socket.send(msgBytes)
        
        try:
            respBytes = self.socket.recv()
        except Exception as e:
            print ("Exception: {1}".format(e.errno, e.strerror))
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
                self.channel.connect("tcp://localhost:" + str(port))
            else:
                raise SetupError("Actor registration error")
        else:
            assert False
        return 

    def handleRegReq(self,bundle):
        self.logger.info("handleRegReq: %s" % str(bundle))
        (partName,partType,kind,isLocal,portName,portType,portHost,portNum) = bundle[0:8]
        # All interactions below go via the REQ/REP socket ; the channel is for server pushes
        req = disco_capnp.DiscoReq.new_message()
        reqMsg = req.init('serviceReg')
        reqMsgPath = reqMsg.path
        reqMsg.socket.host = self.actor.localHost if isLocal else self.actor.globalHost
        reqMsg.socket.port = portNum
        reqMsgPath.appName = self.appName
        reqMsgPath.msgType = portType 
        reqMsgPath.kind = kind
        reqMsgPath.scope = 'local' if isLocal else 'global'
        msgBytes = req.to_bytes()
        self.socket.send(msgBytes)
        try:
            repBytes = self.socket.recv()
        except Exception as e:
            print ("Exception: {1}".format(e.errno, e.strerror))
            raise
        rep = disco_capnp.DiscoRep.from_bytes(repBytes)
        which = rep.which()
        if which == 'serviceReg':
            repMessage = rep.serviceReg
            status = repMessage.status
            if status == 'err':
                raise SetupError('Unable to register service')
            else:
                pass
        else:
            raise SetupError("Service registration error - bad response")
        return
    
    def handleLookupReq(self,bundle):
        self.logger.info("handleLookupReq: %s" % str(bundle))
        (partName,partType,kind,isLocal,portName,portType) = bundle[0:6]
        # All interactions below go via the REQ/REP socket ; the channel is for server pushes
        req = disco_capnp.DiscoReq.new_message()
        reqMsg = req.init('serviceLookup')
        reqMsgPath = reqMsg.path
        reqMsgPath.appName = self.appName
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
            print ("Exception: {1}".format(e.errno, e.strerror))
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
        kind = bundle[2]
        #(partName,partType,kind,isLocal,portName,portType) = bundle[0:6]
        # All interactions below go via the REQ/REP socket ; the channel is for server pushes
        result = []
        # Update component means: add command to component's message queue
        if kind == 'pub' or kind == 'srv' or kind == 'rep':
            # Registe publisher or server port
            self.handleRegReq(bundle)
        elif kind == 'sub' or kind == 'clt' or kind == 'req':
            # Request pub(s) or srv(s);  update component
            result = self.handleLookupReq(bundle)
        else:
            raise SetupError("Invalid registration message")
        return result
