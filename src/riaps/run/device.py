'''
Device actor class to hold and manage a single device component. 
Created on Jan 7, 2017

@author: riaps
'''

from .part import Part
from .peripheral import Peripheral
from .exc import BuildError
import zmq
import time
from riaps.run.disco import DiscoClient
from riaps.run.deplc import DeplClient
from riaps.proto import disco_capnp
from riaps.consts.defs import *
from riaps.utils.ifaces import getNetworkInterfaces
from riaps.utils.config import Config
import getopt
import logging
from builtins import int, str
import re
import sys
import os
import importlib
import traceback
from .actor import Actor
from czmq import Zsys
import yaml
import zmq.auth
from zmq.auth.thread import ThreadAuthenticator

class Device(Actor):
    '''
    The actor class implements all the management and control functions over its components
    '''          
    def __init__(self, gModel, gModelName, dName, sysArgv):
        '''
        Constructor
        '''
        self.logger = logging.getLogger(__name__)
        self.inst_ = self
        self.appName = gModel["name"]
        self.modelName = gModelName
        self.name = dName
        self.pid = os.getpid()
        self.suffix = ""
        if dName not in gModel["devices"]:
            raise BuildError('Device "%s" unknown' % dName)
       
        # In order to make the rest of the code work, we build an actor model for the device
        devModel = gModel["devices"][dName]
        self.model = {}                             # The made-up actor model
        
        formals = devModel["formals"]               # Formals are the same as those of the device (component)
        self.model["formals"] = formals

        devInst = { "type" : dName }                # There is a single instance, containing the device component
        actuals = []
        for arg in  formals:
            name = arg["name"]
            actual = {}
            actual["name"] = name
            actual["param"] = name
            actuals.append(actual)
        devInst["actuals"] = actuals
        
        self.model["instances"] = { dName : devInst}
        
        self.model["locals"] = self.getMessageTypes(devModel)   # All messages are local
        self.model["internals"] =  { }                          # No internals 
        
        self.INT_RE = re.compile(r"^[-]?\d+$")
        self.parseParams(sysArgv)
        
        # Use czmq's context
        czmq_ctx = Zsys.init()
        self.context = zmq.Context.shadow(czmq_ctx.value)
        Zsys.handler_reset()            # Reset previous signal 
        
        # Context for app sockets
        self.appContext = zmq.Context()
        
        if Config.SECURITY:
            (self.public_key,self.private_key) = zmq.auth.load_certificate(const.appCertFile)
            hosts = ['127.0.0.1']
            try:
                with open(const.appDescFile,'r') as f:
                    content = yaml.load(f)
                    hosts += content.hosts
            except:
                pass

            self.auth = ThreadAuthenticator(self.appContext)
            self.auth.start()
            self.auth.allow(*hosts)
            self.auth.configure_curve(domain='*', location=zmq.auth.CURVE_ALLOW_ANY)
        else:
            (self.public_key,self.private_key) = (None,None)
            self.auth = None
            self.appContext = self.context
        
        try:
            if os.path.isfile(const.logConfFile) and os.access(const.logConfFile, os.R_OK):
                spdlog_setup.from_file(const.logConfFile)      
        except Exception as e:
            self.logger.error("error while configuring componentLogger: %s" % repr(e))  
        
        messages = gModel["messages"]              # Global message types (global on the network)
        self.messageNames = []
        for messageSpec in messages:
            self.messageNames.append(messageSpec["name"])
                   
        locals_ = self.model["locals"]                       # Local message types (local to the host)
        self.localNames = []
        for messageSpec in locals_:
            self.localNames.append(messageSpec["type"]) 
            
        internals = self.model["internals"]                 # Internal message types (internal to the actor process)
        self.internalNames = []
        for messageSpec in internals:
            self.internalNames.append(messageSpec["type"])
            
        self.components = {}
        instSpecs = self.model["instances"]
        compSpecs = gModel["components"]
        devSpecs = gModel["devices"]
        for instName in instSpecs:                          # Create the component instances: the 'parts'
            instSpec = instSpecs[instName]
            instType = instSpec['type']
            if instType in devSpecs: 
                typeSpec = devSpecs[instType]
            else:
                raise BuildError('Device type "%s" for instance "%s" is undefined' % (instType,instName))
            instFormals = typeSpec['formals']
            instActuals = instSpec['actuals']
            instArgs = self.buildInstArgs(instName,instFormals,instActuals)
            # Check whether the component is C++ component
            ccComponentFile = 'lib' + instType.lower() + '.so'
            ccComp = os.path.isfile(ccComponentFile)
            try:
                if ccComp:
                    modObj= importlib.import_module('lib'+instType.lower())
                    self.components[instName] = modObj.create_component_py(self,self.model,
                                                                           typeSpec,instName,
                                                                           instType,instArgs,
                                                                           self.appName,self.name)
                else:
                    self.components[instName]= Part(self,typeSpec,instName, instType, instArgs)
            except Exception as e:
                traceback.print_exc()
                self.logger.error("Error while constructing part '%s.%s': %s" % (instType,instName,str(e)))
                    
    
    def getPortMessageTypes(self,ports,key,kinds,res):
        for _name,spec in ports[key].items():
            for kind in kinds:
                typeName = spec[kind]
                res.append({"type" : typeName})
        
    def getMessageTypes(self,devModel):
        res = []
        ports = devModel["ports"]
        self.getPortMessageTypes(ports,"pubs",["type"],res)
        self.getPortMessageTypes(ports,"subs",["type"],res)
        self.getPortMessageTypes(ports,"reqs",["req_type","rep_type"],res)
        self.getPortMessageTypes(ports,"reps",["req_type","rep_type"],res)
        self.getPortMessageTypes(ports,"clts",["req_type","rep_type"],res)
        self.getPortMessageTypes(ports,"srvs",["req_type","rep_type"],res)
        self.getPortMessageTypes(ports,"qrys",["req_type","rep_type"],res)
        self.getPortMessageTypes(ports,"anss",["req_type","rep_type"],res)
        return res
        
#     def getParameterValueType(self,param,defaultType):
#         paramValue, paramType = None, None
#         if defaultType != None:
#             if defaultType == str:
#                 paramValue, paramType = param, str
#             elif defaultType == int:
#                 paramValue, paramType = int(param),int
#             elif defaultType == float:
#                 paramValue, paramType = float(param),float
#             elif defaultType == bool:
#                 paramType = bool
#                 paramValue = False if param == "False" else True if param == "True" else None
#                 paramValue, paramType = bool(param),float
#         else:
#             if param == 'True':
#                 paramValue, paramType = True, bool
#             elif param == 'False':
#                 paramValue, paramType = True, bool
#             elif self.INT_RE.match(param) is not None:
#                 paramValue, paramType = int(param),int
#             else:
#                 try:
#                     paramValue, paramType = float(param),float
#                 except:
#                     paramValue,paramType = str(param), str
#         return (paramValue,paramType)

#     def parseParams(self,sysArgv):
#         self.params = { } 
#         formals = self.model["formals"]
#         optList = []
#         for formal in formals:
#             key = formal["name"]
#             default = None if "default" not in formal else formal["default"]
#             self.params[key] = default
#             optList.append("%s=" % key) 
#         try:
#             opts,args = getopt.getopt(sysArgv, '', optList)
#         except:
#             self.logger.info("Error parsing actor options %s" % str(sysArgv))
#             return
# #        try:
#         for opt in opts:
#             optName2,optValue = opt 
#             optName = optName2[2:] # Drop two leading dashes 
#             if optName in self.params:
#                 defaultType = None if self.params[optName] == None else type(self.params[optName])
#                 paramValue,paramType = self.getParameterValueType(optValue,defaultType)
#                 if self.params[optName] != None:
#                     if paramType != type(self.params[optName]):
#                         raise BuildError("Type of default value does not match type of argument %s" 
#                                          % str((optName,optValue)))
#                 self.params[optName] = paramValue
#             else:
#                 self.logger.info("Unknown argument %s - ignored" % optName)
#         for param in self.params:
#             if self.params[param] == None:
#                 raise BuildError("Required parameter %s missing" % param) 

#     def buildInstArgs(self,instName,formals,actuals):
#         args = {}
#         for formal in formals:
#             argName = formal['name']
#             argValue = None
#             actual = next((actual for actual in actuals if actual['name'] == argName), None)
#             defaultValue = None
#             if 'default' in formal:
#                 defaultValue = formal['default'] 
#             if actual != None:
#                 assert(actual['name'] == argName)
#                 if 'param'in actual:
#                     paramName = actual['param']
#                     if paramName in self.params:
#                         argValue = self.params[paramName]
#                     else:
#                         raise BuildError("Unspecified parameter %s referenced in %s" 
#                                          %(paramName,instName))
#                 elif 'value' in actual:
#                     argValue = actual['value']
#                 else:
#                     raise BuildError("Actual parameter %s has no value" % argName)
#             elif defaultValue != None:
#                 argValue = defaultValue
#             else:
#                 raise BuildError("Argument %s in %s has no defined value" % (argName,instName))
#             args[argName] = argValue
#         return args
    
#     def isLocalMessage(self,msgTypeName):
#         '''
#         Return True if the message type is local
#         '''
#         return msgTypeName in self.localNames
#         
#     def getLocalIface(self):
#         '''
#         Return the IP address of the host-local network interface (usually 127.0.0.1) 
#         '''
#         return self.localHost
#     
#     def getGlobalIface(self):
#         '''
#         Return the IP address of the global network interface
#         '''
#         return self.globalHost
#     
#     def setupIfaces(self):
#         '''
#         Find the IP addresses of the (host-)local and network(-global) interfaces
#         '''
#         (globalIPs,globalMACs,globalNames,localIP) = getNetworkInterfaces()
#         assert len(globalIPs) > 0 and len(globalMACs) > 0
#         globalIP = globalIPs[0]
#         globalMAC = globalMACs[0]
#         self.localHost = localIP
#         self.globalHost = globalIP
#         self.macAddress = globalMAC
#                
    def setup(self):
        '''
        Perform a setup operation on the actor (after  the initial construction but before the activation of parts)
        '''
        self.logger.info("setup")
        self.setupIfaces()
        self.suffix = self.macAddress
        self.disco = DiscoClient(self,self.suffix)
        self.disco.start()                  # Start the discovery service client
        self.disco.registerApp()            # Register this actor with the discovery service
        self.logger.info("device registered with disco")
        self.deplc = DeplClient(self,self.suffix)
        self.deplc.start()
        ok = self.deplc.registerApp(isDevice=True)       
        self.logger.info("device %s registered with depl" % ("is" if ok else "is not"))
        self.controls = { }
        self.controlMap = { }
        for inst in self.components:
            comp = self.components[inst]
            control = self.context.socket(zmq.PAIR)
            control.bind('inproc://part_' + inst + '_control')
            self.controls[inst] = control
            self.controlMap[id(control)] = comp 
            if isinstance(comp, Part):
                self.components[inst].setup(control)
            else:
                self.components[inst].setup()
    
#     def start(self):
#         '''
#         Start and operate the actor (infinite polling loop)
#         '''
#         self.logger.info("starting")
#         self.discoChannel = self.disco.channel              # Private channel to the discovery service
#         self.deplChannel = self.deplc.channel
#        
#         self.poller = zmq.Poller()                          # Set up the poller
#         self.poller.register(self.deplChannel,zmq.POLLIN)
#         self.poller.register(self.discoChannel,zmq.POLLIN)
#         
#         while 1:
#             sockets = dict(self.poller.poll())              
#             if self.discoChannel in sockets:                # If there is a message from a service, handle it
#                 msgs = self.recvChannelMessages(self.discoChannel)
#                 for msg in msgs:
#                     self.handleServiceUpdate(msg)               # Handle message from disco service
#                 del sockets[self.discoChannel]    
#             elif self.deplChannel in sockets:
#                 msgs = self.recvChannelMessages(self.deplChannel)
#                 for msg in msgs:
#                     self.handleDeplMessage(msg)                 # Handle message from depl service
#                 del sockets[self.deplChannel]
#             else:
#                 pass

    def terminate(self):
        self.logger.info("terminating")
        for component in self.components.values():
            component.terminate()
        # self.devc.terminate()
        self.disco.terminate()
        # Clean up everything
        # self.context.destroy()
        time.sleep(1.0)
        self.logger.info("terminated")
        os._exit(0)
        