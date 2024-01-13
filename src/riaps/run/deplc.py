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
        self.context = zmq.Context()
        
    def start(self):
        self.logger.info("starting")
        self.socket = self.context.socket(zmq.REQ)
        self.socket.setsockopt(zmq.RCVTIMEO, const.deplEndpointRecvTimeout)
        self.socket.setsockopt(zmq.SNDTIMEO, const.deplEndpointSendTimeout)
        endpoint = const.deplEndpoint
        self.socket.connect(endpoint)    
        self.channel = self.context.socket(zmq.PAIR)
        self.logger.info("started")

    def registerActor(self):
        self.logger.info("registerActor")
        if self.socket == None:
            self.logger.error("registerActor: No deplo")
            return False
        
        reqt = deplo_capnp.DeplReq.new_message()
        appMessage = reqt.init('actorReg')
        appMessage.appName = self.appName
        appMessage.version = '0.0.0'
        isDevice = self.actor.isDevice()
        appMessage.actorName = self.actor.name
        appMessage.pid = os.getpid()
        appMessage.isDevice = isDevice
        
        msgBytes = reqt.to_bytes()

        try:
            self.socket.send(msgBytes)
        except Exception as e:
            self.logger.error("registerActor: Failed to send: {1}".format(e.errno, e.strerror))
            # self.socket.close()
            # self.socket = None
            return False
        
        try:
            respBytes = self.socket.recv()
        except Exception as e:
            self.logger.error("registerActor: No response: {1}".format(e.errno, e.strerror))
            # self.socket.close()
            # self.socket = None
            return False
      
        with deplo_capnp.DeplRep.from_bytes(respBytes) as resp:
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
                    self.logger.error("registerActor: can't connect to deplo")
                    # raise SetupError("registerActor - can't connect to deplo channel")
                    return False
            else:
                self.logger.error("registerActor: unexpected response from deplo")
                # raise SetupError("registerActor - unexpected response from deplo")
                return False

    def requestDevice(self, bundle):
        self.logger.info("requestDevice %s" % str(bundle))
        
        if self.socket == None:
            self.logger.error("requestDevice: No deplo")
            return False

        appName, modelName, typeName, instName, args = bundle

        reqt = deplo_capnp.DeplReq.new_message()
        devMessage = reqt.init('deviceGet')
        devMessage.appName = appName
        devMessage.modelName = modelName
        devMessage.typeName = typeName
        devMessage.instName = instName
        devMessage.init('deviceArgs', len(args))
        i = 0
        for argName, argValue in args.items():
            deviceArg = devMessage.deviceArgs[i]
            deviceArg.name = argName
            deviceArg.value = str(argValue)
            i += 1 

        msgBytes = reqt.to_bytes()
 
        try:
            self.socket.send(msgBytes)
        except Exception as e:
            self.logger.error("requestDevice: failed to send: %s" % str(e.args))
            # self.socket.close()
            # self.socket = None
            return False
         
        try:
            respBytes = self.socket.recv()
        except Exception as e:
            self.logger.error("requestDevice: no response: %s" % str(e.args))
            # self.socket.close()
            # self.socket = None
            return False
       
        with deplo_capnp.DeplRep.from_bytes(respBytes) as resp:
            which = resp.which()
            if which == 'deviceGet':
                respMessage = resp.deviceGet
                status = respMessage.status
                if status == 'ok':
                    return True
                else:
                    self.logger.error("requestDevice: error response from deplo")
                    # raise SetupError("requestDevice - error response from deplo")
                    return False
            else:
                self.logger.error("requestDevice: unexpected response from deplo")
                # raise SetupError("requestDevice - unexpected response from deplo")
                return False
    
    def releaseDevice(self, bundle):
        self.logger.info("releaseDevice %s" % str(bundle))
        
        if self.socket == None:
            self.logger.error("releaseDevice: No deplo")
            return False

        appName, modelName, typeName, instName = bundle

        reqt = deplo_capnp.DeplReq.new_message()
        devMessage = reqt.init('deviceRel')
        devMessage.appName = appName
        devMessage.modelName = modelName
        devMessage.typeName = typeName
        devMessage.instName = instName

        msgBytes = reqt.to_bytes()
 
        try:
            self.socket.send(msgBytes)
        except Exception as e:
            self.logger.error("releaseDevice: failed to send: %s" % str(e.args))
#             self.socket.close()
#             self.socket = None
            return False
         
        try:
            respBytes = self.socket.recv()
        except Exception as e:
            self.logger.error("releaseDevice - no response: %s" % str(e.args))
#             self.socket.close()
#             self.socket = None
            return False
       
        with deplo_capnp.DeplRep.from_bytes(respBytes) as resp:
            which = resp.which()
            if which == 'deviceRel':
                respMessage = resp.deviceRel
                status = respMessage.status
                if status == 'ok':
                    return True
                else:
                    self.logger.error("releaseDevice: error response from deplo")
                    # raise SetupError(errMsg)
                    return False
            else:
                self.logger.error("releaseDevice: unexpected response from deplo")
                # raise SetupError(errMsg)
                return False
    
    def reportEvent(self, bundle):
        self.logger.info("reportEvent %s" % str(bundle))
        
        if self.socket == None:
            self.logger.error("reportEvent: No deplo", str(bundle))
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
            self.logger.error("reportEvent: failed to send: {1}".format(e.errno, e.strerror))
            # self.socket.close()
            # self.socket = None
            return False
        
        try:
            respBytes = self.socket.recv()
        except Exception as e:
            self.logger.error("reportEvent: no response: {1}".format(e.errno, e.strerror))
            # self.socket.close()
            # self.socket = None
            return False
      
        with deplo_capnp.DeplRep.from_bytes(respBytes) as resp:
            which = resp.which()
            if which == 'reportEvent':
                respMessage = resp.reportEvent
                status = respMessage.status
                if status == 'ok':
                    return True
                else:
                    self.logger.error("reportEvent: error response from deplo")
                    # raise SetupError("reportEvent - can't connect to deplo channel")
                    return False
            else:
                self.logger.error("reportEvent: unexpected response from deplo")
                # raise SetupError("reportEvent - unexpected response from deplo")
                return False
    
    def terminate(self):
        self.socket.setsockopt(zmq.LINGER, 0)
        endpoint = const.deplEndpoint
        self.socket.disconnect(endpoint) 
        self.logger.info("terminated")
        pass
    
