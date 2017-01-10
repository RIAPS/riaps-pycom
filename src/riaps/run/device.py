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
from .disco import DiscoClient
#from .devm import DevmClient
from riaps.proto import disco_capnp
from riaps.utils.ifaces import getNetworkInterfaces
from riaps.utils.config import Config
import getopt
import logging
from builtins import int, str
import re
import sys
from .actor import Actor

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
        
        self.context = zmq.Context()
        
        messages = gModel["messages"]                       # Global message types (global on the network)
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
            self.components[instName]= Part(self,typeSpec,instName, instType, instArgs)
    
    def getPortMessageTypes(self,ports,key,kinds,res):
        for name,spec in ports[key].items():
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
        return res
        
    def getParameterValueType(self,param,defaultType):
        paramValue, paramType = None, None
        if defaultType != None:
            if defaultType == str:
                paramValue, paramType = param, str
            elif defaultType == int:
                paramValue, paramType = int(param),int
            elif defaultType == float:
                paramValue, paramType = float(param),float
            elif defaultType == bool:
                paramType = bool
                paramValue = False if param == "False" else True if param == "True" else None
                paramValue, paramType = bool(param),float
        else:
            if param == 'True':
                paramValue, paramType = True, bool
            elif param == 'False':
                paramValue, paramType = True, bool
            elif self.INT_RE.match(param) is not None:
                paramValue, paramType = int(param),int
            else:
                try:
                    paramValue, paramType = float(param),float
                except:
                    paramValue,paramType = str(param), str
        return (paramValue,paramType)

    def parseParams(self,sysArgv):
        self.params = { } 
        formals = self.model["formals"]
        optList = []
        for formal in formals:
            key = formal["name"]
            default = None if "default" not in formal else formal["default"]
            self.params[key] = default
            optList.append("%s=" % key) 
        try:
            opts,args = getopt.getopt(sysArgv, '', optList)
        except:
            self.logger.info("Error parsing actor options %s" % str(sysArgv))
            return
#        try:
        for opt in opts:
            optName2,optValue = opt 
            optName = optName2[2:] # Drop two leading dashes 
            if optName in self.params:
                defaultType = None if self.params[optName] == None else type(self.params[optName])
                paramValue,paramType = self.getParameterValueType(optValue,defaultType)
                if self.params[optName] != None:
                    if paramType != type(self.params[optName]):
                        raise BuildError("Type of default value does not match type of argument %s" 
                                         % str((optName,optValue)))
                self.params[optName] = paramValue
            else:
                self.logger.info("Unknown argument %s - ignored" % optName)
        for param in self.params:
            if self.params[param] == None:
                raise BuildError("Required parameter %s missing" % param) 

    def buildInstArgs(self,instName,formals,actuals):
        args = {}
        for formal in formals:
            argName = formal['name']
            argValue = None
            actual = next((actual for actual in actuals if actual['name'] == argName), None)
            defaultValue = None
            if 'default' in formal:
                defaultValue = formal['default'] 
            if actual != None:
                assert(actual['name'] == argName)
                if 'param'in actual:
                    paramName = actual['param']
                    if paramName in self.params:
                        argValue = self.params[paramName]
                    else:
                        raise BuildError("Unspecified parameter %s referenced in %s" 
                                         %(paramName,instName))
                elif 'value' in actual:
                    argValue = actual['value']
                else:
                    raise BuildError("Actual parameter %s has no value" % argName)
            elif defaultValue != None:
                argValue = defaultValue
            else:
                raise BuildError("Argument %s in %s has no defined value" % (argName,instName))
            args[argName] = argValue
        return args
    
    def isLocalMessage(self,msgTypeName):
        '''
        Return True if the message type is local
        '''
        return msgTypeName in self.localNames
        
    def getLocalIface(self):
        '''
        Return the IP address of the host-local network interface (usually 127.0.0.1) 
        '''
        return self.localHost
    
    def getGlobalIface(self):
        '''
        Return the IP address of the global network interface
        '''
        return self.globalHost
    
    def setupIfaces(self):
        '''
        Find the IP addresses of the (host-)local and network(-global) interfaces
        '''
        (globalIPs,globalMACs,localIP) = getNetworkInterfaces()
        assert len(globalIPs) > 0 and len(globalMACs) > 0
        globalIP = globalIPs[0]
        globalMAC = globalMACs[0]
        self.localHost = localIP
        self.globalHost = globalIP
        self.macAddress = globalMAC
               
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
        # This is a device - does not register with the device manager
#         self.devc = DevmClient(self,self.suffix)
#         self.devc.start()
#         self.devc.registerApp()
        for inst in self.components:
            self.components[inst].setup()
    
    def registerEndpoint(self,bundle):
        '''
        Relay the endpoint registration message to the discovery service client 
        '''
        result = self.disco.registerEndpoint(bundle)
        for res in result:
            (partName,portName,host,port) = res
            self.updatePart(partName,portName,host,port)

    def registerDevice(self,bundle):
        '''
        Relay the device registration message to the device interface service client
        '''
        typeName,args = bundle
        msg = (self.appName,self.modelName,typeName,args)
        result = self.devc.registerDevice(msg)
        return result

    def activate(self):
        '''
        Activate the parts
        '''
        self.logger.info("activate")
        for inst in self.components:
            self.components[inst].activate()
            
    def deactivate(self):
        '''
        Deactivate the parts
        '''
        self.logger.info("deactivate")
        for inst in self.components:
            self.components[inst].deactivate()

    def start(self):
        '''
        Start and operate the actor (infinite polling loop)
        '''
        self.logger.info("starting")
        self.discoChannel = self.disco.channel              # Private channel to the discovery service
#        self.devcChannel = self.devc.channel
       
        self.poller = zmq.Poller()                          # Set up the poller
#        self.poller.register(self.devcChannel,zmq.POLLIN)
        self.poller.register(self.discoChannel,zmq.POLLIN)
        
        while 1:
            sockets = dict(self.poller.poll())              
            if self.discoChannel in sockets:                # If there is a message from a service, handle it
                msg = self.discoChannel.recv()
                self.handleServiceUpdate(msg)               # Handle message from disco service
                del sockets[self.discoChannel]
#            elif self.devicChannel in sockets:
#                msg = self.devcChannel.recv()
#                pass                                        # Handle message from devm service
#                del sockets[self.devcChannel]
            else:
                pass
            
    def handleServiceUpdate(self,msgBytes):
        '''
        Handle a service update message from the discovery service
        '''
        msg = disco_capnp.DiscoUpd.from_bytes(msgBytes)     # Parse the incoming message
        client = msg.client
        actorHost = client.actorHost
        assert actorHost == self.globalHost                 # It has to be addressed to this actor
        actorName = client.actorName
        assert actorName == self.name
        instanceName = client.instanceName
        assert instanceName in self.components              # It has to be for a part of this actor
        portName = client.portName
        scope = msg.scope
        socket = msg.socket
        host = socket.host
        port = socket.port 
        if scope == "local":
            assert host == self.localHost
        self.updatePart(instanceName,portName,host,port)    # Update the selected part
    
    def updatePart(self,instanceName,portName,host,port):
        '''
        Ask a part to update itself
        '''
        self.logger.info("updatePart %s" % str((instanceName,portName,host,port)))
        part = self.components[instanceName]
        part.handlePortUpdate(portName,host,port)
        