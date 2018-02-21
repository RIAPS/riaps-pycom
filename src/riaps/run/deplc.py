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
    Devmvery service client of an actor
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

    def registerApp(self):
        self.logger.info("registerApp")
        reqt = deplo_capnp.DeplReq.new_message()
        appMessage = reqt.init('actorReg')
        appMessage.appName = self.appName
        appMessage.version = '0.0.0'
        appMessage.actorName = self.actor.name
        appMessage.pid = os.getpid()
                  
        msgBytes = reqt.to_bytes()

        try:
            self.socket.send(msgBytes)
        except Exception as e:
            self.logger.error("Unable to register app with depl: {1}".format(e.errno, e.strerror))
            self.socket.close()
            self.socket = None
            return False
        
        try:
            respBytes = self.socket.recv()
        except Exception as e:
            self.logger.error("No response from depl service: {1}".format(e.errno, e.strerror))
            self.socket.close()
            self.socket = None
            return False
      
        resp = deplo_capnp.DeplRep.from_bytes(respBytes)
        which = resp.which()
        if which == 'actorReg':
            respMessage = resp.actorReg
            status = respMessage.status
            port = respMessage.port
            if status == 'ok':
                self.channel.connect("tcp://127.0.0.1:" + str(port))
                return True
            else:
                raise SetupError("Error response from depl service at app registration")
        else:
            raise SetupError("Unexpected response from depl service at app registration")

    def registerDevice(self,bundle):
        self.logger.info("registerDevice")
        
        if self.socket == None:
            self.logger.info("No depl service - skipping device registration: %s", str(bundle))
            return False

        appName,modelName,typeName,args = bundle

        reqt = deplo_capnp.DeplReq.new_message()
        devMessage = reqt.init('deviceReg')
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
            self.logger.error("Unable to register device with depl service: {1}".format(e.errno, e.strerror))
            self.socket.close()
            self.socket = None
            return False
         
        try:
            respBytes = self.socket.recv()
        except Exception as e:
            self.logger.error("No response from depl service: {1}".format(e.errno, e.strerror))
            self.socket.close()
            self.socket = None
            return False
       
        resp = deplo_capnp.DeplRep.from_bytes(respBytes)
        which = resp.which()
        if which == 'deviceReg':
            respMessage = resp.deviceReg
            status = respMessage.status
            if status == 'ok':
                return True
            else:
                raise SetupError("Error response from depl service at device registration")
        else:
            raise SetupError("Unexpected response from depl service at device registration")
    
    def unregisterDevice(self,bundle):
        self.logger.info("unregisterDevice")
        
        if self.socket == None:
            self.logger.info("No depl service - skipping device unregistration: %s", str(bundle))
            return False

        appName,modelName,typeName = bundle

        reqt = deplo_capnp.DeplReq.new_message()
        devMessage = reqt.init('deviceUnreg')
        devMessage.appName = appName
        devMessage.modelName = modelName
        devMessage.typeName = typeName

        msgBytes = reqt.to_bytes()
 
        try:
            self.socket.send(msgBytes)
        except Exception as e:
            self.logger.error("Unable to unregister device with depl service: {1}".format(e.errno, e.strerror))
            self.socket.close()
            self.socket = None
            return False
         
        try:
            respBytes = self.socket.recv()
        except Exception as e:
            self.logger.error("No response from depl service: {1}".format(e.errno, e.strerror))
            self.socket.close()
            self.socket = None
            return False
       
        resp = deplo_capnp.DeplRep.from_bytes(respBytes)
        which = resp.which()
        if which == 'deviceUnreg':
            respMessage = resp.deviceUnreg
            status = respMessage.status
            if status == 'ok':
                return True
            else:
                raise SetupError("Error response from depl service at device unregistration")
        else:
            raise SetupError("Unexpected response from depl service at device unregistration")
    
    def terminate(self):
        self.logger.info("terminating")
        pass
    