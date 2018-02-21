'''
Actor class to hold and manage components. 
Created on Oct 9, 2016

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
from riaps.proto import deplo_capnp
from riaps.utils.ifaces import getNetworkInterfaces
import getopt
import logging
from builtins import int, str
import re
import sys
import os
import ipaddress

class Actor(object):
    '''
    The actor class implements all the management and control functions over its components
    '''          
    def __init__(self, gModel, gModelName, aName, sysArgv):
        '''
        Constructor
        '''
        self.logger = logging.getLogger(__name__)
        self.inst_ = self
        self.appName = gModel["name"]
        self.modelName = gModelName
        self.name = aName
        self.pid = os.getpid()
        self.setupIfaces()
        # Assumption : pid is a 4 byte int
        self.actorID = ipaddress.IPv4Address(self.globalHost).packed + self.pid.to_bytes(4,'big')
        self.suffix = ""
        if aName not in gModel["actors"]:
            raise BuildError('Actor "%s" unknown' % aName)
        self.model = gModel["actors"][aName]                # Fetch the relevant content from the model
        
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
        ioSpecs = gModel["devices"]
        for instName in instSpecs:                          # Create the component instances: the 'parts'
            instSpec = instSpecs[instName]
            instType = instSpec['type']
            if instType in compSpecs:
                typeSpec = compSpecs[instType]
                ioComp = False
            elif instType in ioSpecs:
                typeSpec = ioSpecs[instType]
                ioComp = True
            else:
                raise BuildError('Component type "%s" for instance "%s" is undefined' % (instType,instName))
            instFormals = typeSpec['formals']
            instActuals = instSpec['actuals']
            instArgs = self.buildInstArgs(instName,instFormals,instActuals)
            if not ioComp:
                self.components[instName]= Part(self,typeSpec,instName, instType, instArgs)
            else:
                self.components[instName]= Peripheral(self,typeSpec,instName, instType, instArgs)
           
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
            opts,_args = getopt.getopt(sysArgv, '', optList)
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

    def isInnerMessage(self,msgTypeName):
        '''
        Return True if the message type is internal
        '''
        return msgTypeName in self.internalNames
        
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

    def getActorName(self):
        return self.name
    
    def getAppName(self):
        return self.appName 
        
    def getActorID(self):
        return self.actorID
    
    def setupIfaces(self):
        '''
        Find the IP addresses of the (host-)local and network(-global) interfaces
        '''
        (globalIPs,globalMACs,_globalNames,localIP) = getNetworkInterfaces()
        try:
            assert len(globalIPs) > 0 and len(globalMACs) > 0
        except:
            self.logger.error("Error: no active network interface")
            raise
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
        self.suffix = self.macAddress
        self.disco = DiscoClient(self,self.suffix)
        self.disco.start()                  # Start the discovery service client
        self.disco.registerApp()            # Register this actor with the discovery service
        self.logger.info("actor registered with disco")
        self.deplc = DeplClient(self,self.suffix)
        self.deplc.start()
        ok = self.deplc.registerApp()
        self.logger.info("actor %s registered with depl" % ("is" if ok else "is not"))
        for inst in self.components:
            self.components[inst].setup()
    
    def registerEndpoint(self,bundle):
        '''
        Relay the endpoint registration message to the discovery service client 
        '''
        self.logger.info("registerEndpoint")
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
        result = self.deplc.registerDevice(msg)
        return result

    def unregisterDevice(self,bundle):
        '''
        Relay the device registration message to the device interface service client
        '''
        typeName, = bundle
        msg = (self.appName,self.modelName,typeName)
        result = self.deplc.unregisterDevice(msg)
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
            
    def recvChannelMessages(self,channel):
        msgs = []
        while True:
            try:
                msg = channel.recv(flags=zmq.NOBLOCK)
                msgs.append(msg)
            except zmq.Again:
                break
        return msgs   

    def start(self):
        '''
        Start and operate the actor (infinite polling loop)
        '''
        self.logger.info("starting")
        self.discoChannel = self.disco.channel              # Private channel to the discovery service
        self.deplChannel = self.deplc.channel
       
        self.poller = zmq.Poller()                          # Set up the poller
        self.poller.register(self.deplChannel,zmq.POLLIN)
        self.poller.register(self.discoChannel,zmq.POLLIN)
        
        while 1:
            sockets = dict(self.poller.poll())              
            if self.discoChannel in sockets:                # If there is a message from a service, handle it
                msgs = self.recvChannelMessages(self.discoChannel)
                for msg in msgs:
                    self.handleServiceUpdate(msg)               # Handle message from disco service
                del sockets[self.discoChannel]    
            elif self.deplChannel in sockets:
                msgs = self.recvChannelMessages(self.deplChannel)
                for msg in msgs:
                    self.handleDeplMessage(msg)                 # Handle message from depl service
                del sockets[self.deplChannel]
            else:
                pass
            
    def handleServiceUpdate(self,msgBytes):
        '''
        Handle a service update message from the discovery service
        '''
        msgUpd = disco_capnp.DiscoUpd.from_bytes(msgBytes)     # Parse the incoming message

        which = msgUpd.which()
        if which == 'portUpdate':
            msg = msgUpd.portUpdate
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
        
    def handleDeplMessage(self,msgBytes):
        '''
        Handle a message from the deployment service
        '''
        msgUpd = deplo_capnp.ResMsg.from_bytes(msgBytes)     # Parse the incoming message

        which = msgUpd.which()
        if which == 'resCPUX':
            self.handleCPULimit()
        elif which == 'resMemX':
            self.handleMemLimit()
        elif which == 'resSpcX':
            self.handleSpcLimit()
        elif which == 'resNetX':
            self.handleNetLimit()
        else:
            pass
           
    def handleCPULimit(self):
        '''
        Handle the case when the CPU limit is exceeded: notify each component.
        If the component has defined a handler, it will be called.   
        ''' 
        self.logger.info("handleCPULimit")
        for component in self.components.values():
            component.handleCPULimit()
            
    def handleMemLimit(self):
        '''
        Handle the case when the memory limit is exceeded: notify each component.
        If the component has defined a handler, it will be called.   
        ''' 
        self.logger.info("handleMemLimit")
        for component in self.components.values():
            component.handleMemLimit()
            
    def handleSpcLimit(self):
        '''
        Handle the case when the file space limit is exceeded: notify each component.
        If the component has defined a handler, it will be called.   
        ''' 
        self.logger.info("handleSpcLimit")
        for component in self.components.values():
            component.handleSpcLimit()
            
    def handleNetLimit(self):
        '''
        Handle the case when the net usage limit is exceeded: notify each component.
        If the component has defined a handler, it will be called.   
        ''' 
        self.logger.info("handleNetLimit")
        for component in self.components.values():
            component.handleNetLimit()
            
    def terminate(self):
        self.logger.info("terminating")
        for component in self.components.values():
            component.terminate()
        self.deplc.terminate()
        self.disco.terminate()
        # Clean up everything
        # self.context.destroy()
        # time.sleep(1.0)
        self.logger.info("terminated")
        os._exit(0)

    
    