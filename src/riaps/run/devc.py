'''
Device manager client
Created on Jan 3, 2017

@author: riaps
'''

import zmq
import capnp
from riaps.proto import devm_capnp
from riaps.consts.defs import *
from .exc import SetupError
import logging

class DevmClient(object):
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
        self.socket.setsockopt(zmq.RCVTIMEO,const.devmEndpointRecvTimeout)
        self.socket.setsockopt(zmq.SNDTIMEO,const.devmEndpointRecvTimeout)
        endpoint = const.devmEndpoint + self.suffix
        self.socket.connect(endpoint)    
        self.channel = self.context.socket(zmq.PAIR)

    def registerApp(self):
        self.logger.info("registerApp")
        reqt = devm_capnp.DevmReq.new_message()
        appMessage = reqt.init('actorReg')
        appMessage.appName = self.appName
        appMessage.version = '0.0.0'
        appMessage.actorName = self.actor.name
                  
        msgBytes = reqt.to_bytes()

        try:
            self.socket.send(msgBytes)
        except Exception as e:
            self.logger.error("Unable to register app with devm: {1}".format(e.errno, e.strerror))
            self.socket.close()
            self.socket = None
            return
        
        try:
            respBytes = self.socket.recv()
        except Exception as e:
            self.logger.error("No response from devm service {1}".format(e.errno, e.strerror))
            self.socket.close()
            self.socket = None
            return
      
        resp = devm_capnp.DevmRep.from_bytes(respBytes)
        which = resp.which()
        if which == 'actorReg':
            respMessage = resp.actorReg
            status = respMessage.status
            port = respMessage.port
            if status == 'ok':
                self.channel.connect("tcp://localhost:" + str(port))
            else:
                raise SetupError("Error response from devm service at app registration")
        else:
            raise SetupError("Unexpected response from devm service at app registration")
        return 

    def registerDevice(self,bundle):
        self.logger.info("registerDevice")
        
        if self.socket == None:
            self.logger.info("No devm service - skipping device registration: %s", str(bundle))
            return False

        appName,modelName,typeName,args = bundle

        reqt = devm_capnp.DevmReq.new_message()
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
            self.logger.error("Unable to register device with devm service: {1}".format(e.errno, e.strerror))
            self.socket.close()
            self.socket = None
            return
         
        try:
            respBytes = self.socket.recv()
        except Exception as e:
            self.logger.error("No response from devm service: {1}".format(e.errno, e.strerror))
            self.socket.close()
            self.socket = None
            return
       
        resp = devm_capnp.DevmRep.from_bytes(respBytes)
        which = resp.which()
        if which == 'deviceReg':
            respMessage = resp.deviceReg
            status = respMessage.status
            if status == 'ok':
                return True
            else:
                raise SetupError("Error response from devm service at device registration")
        else:
            raise SetupError("Unexpected response from devm service at device registration")
        return False
    
    def unregisterDevice(self,bundle):
        self.logger.info("unregisterDevice")
        
        if self.socket == None:
            self.logger.info("No devm service - skipping device unregistration: %s", str(bundle))
            return False

        appName,modelName,typeName = bundle

        reqt = devm_capnp.DevmReq.new_message()
        devMessage = reqt.init('deviceUnreg')
        devMessage.appName = appName
        devMessage.modelName = modelName
        devMessage.typeName = typeName

        msgBytes = reqt.to_bytes()
 
        try:
            self.socket.send(msgBytes)
        except Exception as e:
            self.logger.error("Unable to unregister device with devm service: {1}".format(e.errno, e.strerror))
            self.socket.close()
            self.socket = None
            return
         
        try:
            respBytes = self.socket.recv()
        except Exception as e:
            self.logger.error("No response from devm service: {1}".format(e.errno, e.strerror))
            self.socket.close()
            self.socket = None
            return
       
        resp = devm_capnp.DevmRep.from_bytes(respBytes)
        which = resp.which()
        if which == 'deviceUnreg':
            respMessage = resp.deviceUnreg
            status = respMessage.status
            if status == 'ok':
                return True
            else:
                raise SetupError("Error response from devm service at device unregistration")
        else:
            raise SetupError("Unexpected response from devm service at device unregistration")
        return False
    
    