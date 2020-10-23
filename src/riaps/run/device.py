'''
Device actor class to hold and manage a single device component. 
Created on Jan 7, 2017

@author: riaps
'''

from .part import Part
from .peripheral import Peripheral
from .exc import BuildError
import sys
import zmq
import time
from riaps.run.disco import DiscoClient
from riaps.run.deplc import DeplClient
from riaps.proto import disco_capnp
from riaps.consts.defs import *
from riaps.utils.ifaces import getNetworkInterfaces
from riaps.utils.config import Config
from riaps.utils.appdesc import AppDescriptor
import getopt
import logging
from builtins import int, str
import re
import sys
import os
import ipaddress
import importlib
import traceback
from .actor import Actor
from czmq import Zsys
from riaps.utils import spdlog_setup
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
        self.uuid = None
        self.suffix = ""
        self.setupIfaces()
        # Assumption : pid is a 4 byte int
        self.actorID = ipaddress.IPv4Address(self.globalHost).packed + self.pid.to_bytes(4,'big')
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
            _public = zmq.curve_public(self.private_key)
            if(self.public_key != _public):
                self.logger.error("bad security key(s)")
                raise BuildError("invalid security key(s)")
            hosts = ['127.0.0.1']
            try:
                with open(const.appDescFile,'r') as f:
                    content = yaml.load(f, Loader=yaml.Loader)
                    hosts += content.hosts
            except:
                self.logger.error("Error loading app descriptor:s",str(sys.exc_info()[1]))

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
            
        groups = gModel["groups"]
        self.groupTypes = {} 
        for group in groups:
            self.groupTypes[group["name"]] = { 
                "kind" : group["kind"],
                "message" :  group["message"],
                "timed" : group["timed"]
            }
            
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
                                                                           self.appName,self.name,groups)
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
                     
    def setup(self):
        '''
        Perform a setup operation on the actor (after  the initial construction but before the activation of parts)
        '''
        self.logger.info("setup")
        # self.setupIfaces()
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
        
