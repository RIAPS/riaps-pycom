'''
Deployment manager client
Created on Jan 3, 2017

@author: riaps
'''

import os
import zmq
import capnp
from riaps.proto import deplo_capnp
from riaps.consts.defs import *
from .exc import SetupError
import logging

class DeplClient(object):
    '''
    Deployment service client of an actor
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
        self.socket.setsockopt(zmq.RCVTIMEO,const.deplEndpointRecvTimeout)
        self.socket.setsockopt(zmq.SNDTIMEO,const.deplEndpointSendTimeout)
        endpoint = const.deplEndpoint
        self.socket.connect(endpoint)    
        self.channel = self.context.socket(zmq.PAIR)
        self.logger.info("started")

    def registerApp(self,isDevice=False):
        self.logger.info("registerApp")
        reqt = deplo_capnp.DeplReq.new_message()
        appMessage = reqt.init('actorReg')
        appMessage.appName = self.appName
        appMessage.version = '0.0.0'
        appMessage.actorName = self.actor.name
        appMessage.pid = os.getpid()
        appMessage.isDevice = isDevice
                  
        msgBytes = reqt.to_bytes()

        try:
            self.socket.send(msgBytes)
        except Exception as e:
            self.logger.error("registerApp - failed to send: {1}".format(e.errno, e.strerror))
            # self.socket.close()
            # self.socket = None
            return False
        
        try:
            respBytes = self.socket.recv()
        except Exception as e:
            self.logger.error("registerApp - no response: {1}".format(e.errno, e.strerror))
            # self.socket.close()
            # self.socket = None
            return False
      
        resp = deplo_capnp.DeplRep.from_bytes(respBytes)
        which = resp.which()
        if which == 'actorReg':
            respMessage = resp.actorReg
            status = respMessage.status
            port = respMessage.port
            uuid = respMessage.uuid
            if status == 'ok':
                self.channel.connect("tcp://127.0.0.1:" + str(port))
                self.actor.setUUID(uuid)
                return True
            else:
                errMsg = "registerApp - can't connect to deplo channel"
                self.logger.error(errMsg)
                # raise SetupError("registerApp - can't connect to deplo channel")
                return False
        else:
            errMsg = "registerApp - unexpected response from deplo"
            self.logger.error(errMsg)
            # raise SetupError("registerApp - unexpected response from deplo")
            return False

    def registerDevice(self,bundle):
        self.logger.info("registerDevice %s" % str(bundle))
        
        if self.socket == None:
            self.logger.info("No deplo service - skipping device registration: %s", str(bundle))
            return False

        appName,modelName,typeName,args = bundle

        reqt = deplo_capnp.DeplReq.new_message()
        devMessage = reqt.init('deviceGet')
        devMessage.appName = appName
        devMessage.modelName = modelName
        devMessage.typeName = typeName
        devMessage.init('deviceArgs',len(args))
        i = 0
        for argName,argValue in args.items():
            deviceArg = devMessage.deviceArgs[i]
            deviceArg.name = argName
            deviceArg.value = str(argValue)
            i += 1 

        msgBytes = reqt.to_bytes()
 
        try:
            self.socket.send(msgBytes)
        except Exception as e:
            self.logger.error("registerDevice - failed to send: %s" % str(e.args))
            # self.socket.close()
            # self.socket = None
            return False
         
        try:
            respBytes = self.socket.recv()
        except Exception as e:
            self.logger.error("registerDevice - no response: %s" % str(e.args))
            # self.socket.close()
            # self.socket = None
            return False
       
        resp = deplo_capnp.DeplRep.from_bytes(respBytes)
        which = resp.which()
        if which == 'deviceGet':
            respMessage = resp.deviceGet
            status = respMessage.status
            if status == 'ok':
                return True
            else:
                errMsg = "registerDevice - error response from deplo"
                self.logger.error(errMsg)
                # raise SetupError("registerDevice - error response from deplo")
                return False
        else:
            errMsg = "registerDevice - unexpected response from deplo"
            self.logger.errro(errMsg)
            # raise SetupError("registerDevice - unexpected response from deplo")
            return False
    
    def unregisterDevice(self,bundle):
        self.logger.info("unregisterDevice %s" % str(bundle))
        
        if self.socket == None:
            self.logger.info("No deplo service - skipping device unregistration: %s", str(bundle))
            return False

        appName,modelName,typeName = bundle

        reqt = deplo_capnp.DeplReq.new_message()
        devMessage = reqt.init('deviceRel')
        devMessage.appName = appName
        devMessage.modelName = modelName
        devMessage.typeName = typeName

        msgBytes = reqt.to_bytes()
 
        try:
            self.socket.send(msgBytes)
        except Exception as e:
            self.logger.error("unregisterDevice - failed to send: %s" % str(e.args))
#             self.socket.close()
#             self.socket = None
            return False
         
        try:
            respBytes = self.socket.recv()
        except Exception as e:
            self.logger.error("unregisterDevice - no response: %s" % str(e.args))
#             self.socket.close()
#             self.socket = None
            return False
       
        resp = deplo_capnp.DeplRep.from_bytes(respBytes)
        which = resp.which()
        if which == 'deviceRel':
            respMessage = resp.deviceRel
            status = respMessage.status
            if status == 'ok':
                return True
            else:
                errMsg = "unregisterDevice - error response from deplo"
                self.logger.error(errMsg)
                # raise SetupError(errMsg)
                return False
        else:
            errMsg = "unregisterDevice - unexpected response from deplo"
            self.logger.error(errMsg)
            # raise SetupError(errMsg)
            return False
    
    def reportEvent(self,bundle):
        self.logger.info("reportEvent %s" % str(bundle))
        
        if self.socket == None:
            self.logger.info("No deplo service - skipping event reporting: %s", str(bundle))
            return False
        
        reqt = deplo_capnp.DeplReq.new_message()
        appMessage = reqt.init('reportEvent')
        appMessage.appName = self.appName
        appMessage.version = '0.0.0'
        appMessage.actorName = self.actor.name
        appMessage.msg = str(bundle)
                  
        msgBytes = reqt.to_bytes()

        try:
            self.socket.send(msgBytes)
        except Exception as e:
            self.logger.error("reportEvent - failed to send: {1}".format(e.errno, e.strerror))
            # self.socket.close()
            # self.socket = None
            return False
        
        try:
            respBytes = self.socket.recv()
        except Exception as e:
            self.logger.error("reportEvent - no response: {1}".format(e.errno, e.strerror))
            # self.socket.close()
            # self.socket = None
            return False
      
        resp = deplo_capnp.DeplRep.from_bytes(respBytes)
        which = resp.which()
        if which == 'reportEvent':
            respMessage = resp.reportEvent
            status = respMessage.status
            if status == 'ok':
                return True
            else:
                errMsg = "reportEvent -  err status from deplo"
                self.logger.error(errMsg)
                # raise SetupError("reportEvent - can't connect to deplo channel")
                return False
        else:
            errMsg = "reportEvent - unexpected response from deplo"
            self.logger.error(errMsg)
            # raise SetupError("reportEvent - unexpected response from deplo")
            return False
        
    
    def terminate(self):
        self.logger.info("terminating")
        pass
    