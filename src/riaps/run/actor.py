'''Actor class to hold and manage components.

Actors are processes that act as shells for components that run in their own thread.
 
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
import traceback
from builtins import int, str
import re
import os
import ipaddress

class Actor(object):
    '''The actor class implements all the management and control functions over its components
    
    :param gModel: the JSON-based dictionary holding the model for the app this actor belongs to.
    :type gModel: dict
    :param gModelName: the name of the top-level model for the app
    :type gModelName: str
    :param aName: name of the actor. It is an index into the gModel that points to the part of the model specific to the actor
    :type aName: str
    :param sysArgv: list of arguments for the actor: -key1 value1 -key2 value2 ...
    :type list:
         
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
        self.uuid = None
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
            try:
                if not ioComp:
                    self.components[instName]= Part(self,typeSpec,instName, instType, instArgs)
                else:
                    self.components[instName]= Peripheral(self,typeSpec,instName, instType, instArgs)
            except TypeError as e:
                traceback.print_exc()
                self.logger.error("Error while constructing part '%s.%s': %s" % (instType,instName,str(e)))
                
           
    def getParameterValueType(self,param,defaultType):
        ''' Infer the type of a parameter from its value unless a default type is provided. \
            In the latter case the parameter's value is converted to that type.
            
            :param param: a parameter value
            :type param: one of bool,int,float,str
            :param defaultType:
            :type defaultType: one of bool,int,float,str
            :return: a pair (value,type)
            :rtype: tuple
             
        '''
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
        '''Parse actor arguments from the command line
        
        Compares the actual arguments to the formal arguments (from the model) and
        fills out the local parameter table accordingly. Generates a warning on 
        extra arguments and raises an exception on required but missing ones.
           
        '''
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
        '''Return True if the message type is local
        
        '''
        return msgTypeName in self.localNames

    def isInnerMessage(self,msgTypeName):
        '''Return True if the message type is internal
        
        '''
        return msgTypeName in self.internalNames
        
    def getLocalIface(self):
        '''Return the IP address of the host-local network interface (usually 127.0.0.1) 
        '''
        return self.localHost
    
    def getGlobalIface(self):
        '''Return the IP address of the global network interface
        '''
        return self.globalHost

    def getActorName(self):
        '''Return the name of this actor (as defined in the app model)
        '''
        return self.name
    
    def getAppName(self):
        '''Return the name of the app this actor belongs to
        '''
        return self.appName 
        
    def getActorID(self):
        '''Returns an ID for this actor.
        
        The actor's id constructed from the host's IP address the actor's process id. 
        The id is unique for a given host and actor run.
        '''
        return self.actorID
    
    def setUUID(self,uuid):
        '''Sets the UUID for this actor.
        
        The UUID is dynamically generated (by the peer-to-peer network system)
        and is unique. 
        '''
        self.uuid = uuid
        
    def getUUID(self):
        '''Return the UUID for this actor. 
        '''
        return self.uuid
        
    def setupIfaces(self):
        '''Find the IP addresses of the (host-)local and network(-global) interfaces
        
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
        '''Perform a setup operation on the actor, after  the initial construction 
        but before the activation of parts
        
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
        '''Relay the device registration message to the device interface service client
        
        '''
        typeName,args = bundle
        msg = (self.appName,self.modelName,typeName,args)
        result = self.deplc.registerDevice(msg)
        return result

    def unregisterDevice(self,bundle):
        '''Relay the device unregistration message to the device interface service client
        
        '''
        typeName, = bundle
        msg = (self.appName,self.modelName,typeName)
        result = self.deplc.unregisterDevice(msg)
        return result
    
    def activate(self):
        '''Activate the parts
        
        '''
        self.logger.info("activate")
        for inst in self.components:
            self.components[inst].activate()
            
    def deactivate(self):
        '''Deactivate the parts
        
        '''
        self.logger.info("deactivate")
        for inst in self.components:
            self.components[inst].deactivate()
            
    def recvChannelMessages(self,channel):
        '''Collect all messages from the channel queue and return them in a list
        '''
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
        
        self.controls = { }
        self.controlMap = { }
        for inst in self.components:
            control = self.components[inst].getControl()
            if control != None: 
                self.controls[inst] = control
                self.controlMap[id(control)] = self.components[inst]
       
        self.poller = zmq.Poller()                          # Set up the poller
        self.poller.register(self.deplChannel,zmq.POLLIN)
        self.poller.register(self.discoChannel,zmq.POLLIN)
        for control in self.controls:
            self.poller.register(self.controls[control],zmq.POLLIN)
        
        while 1:
            sockets = dict(self.poller.poll())              
            if self.discoChannel in sockets:                # If there is a message from a service, handle it
                msgs = self.recvChannelMessages(self.discoChannel)
                for msg in msgs:
                    self.handleServiceUpdate(msg)           # Handle message from disco service
                del sockets[self.discoChannel]    
            elif self.deplChannel in sockets:
                msgs = self.recvChannelMessages(self.deplChannel)
                for msg in msgs:
                    self.handleDeplMessage(msg)             # Handle message from depl service
                del sockets[self.deplChannel]
            else:                                           # Handle messages from the components.  
                toDelete = []
                for s in sockets:
                    if s in self.controls.values():
                        part = self.controlMap[id(s)]
                        msg = s.recv_pyobj()
                        self.handleEventReport(part,msg)    # Report event
                    toDelete += [s]
                for s in toDelete:
                    del sockets[s]

            
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
        msgUpd = deplo_capnp.DeplCmd.from_bytes(msgBytes)     # Parse the incoming message

        which = msgUpd.which()
        if which == 'resourceMsg':
            what = msgUpd.resourceMsg.which()
            if what == 'resCPUX':
                self.handleCPULimit()
            elif what == 'resMemX':
                self.handleMemLimit()
            elif what == 'resSpcX':
                self.handleSpcLimit()
            elif what == 'resNetX':
                self.handleNetLimit()
            else:
                self.logger.error("unknown resource msg from deplo: '%s'" % what)
                pass
        elif which == 'reinstateCmd':
            self.handleReinstate()
        elif which == 'nicStateMsg' :
            stateMsg = msgUpd.nicStateMsg
            state = str(stateMsg.nicState)
            self.handleNICStateChange(state)
        elif which == 'peerInfoMsg':
            peerMsg = msgUpd.peerInfoMsg
            state = str(peerMsg.peerState)
            uuid = peerMsg.uuid
            self.handlePeerStateChange(state,uuid)
        else:
            self.logger.error("unknown msg from deplo: '%s'" % which)
            pass
           
    def handleReinstate(self):
        self.logger.info('handleReinstate')
        self.poller.unregister(self.discoChannel)
        self.disco.reconnect()
        self.discoChannel = self.disco.channel
        self.poller.register(self.discoChannel,zmq.POLLIN)
        for inst in self.components:
            self.components[inst].handleReinstate()
    
    def handleNICStateChange(self,state):
        '''
        Handle the NIC state change message: notify components   
        ''' 
        self.logger.info("handleNICStateChange")
        for component in self.components.values():
            component.handleNICStateChange(state)
            
    def handlePeerStateChange(self,state,uuid):
        '''
        Handle the peer state change message: notify components   
        ''' 
        self.logger.info("handlePeerStateChange")
        for component in self.components.values():
            component.handlePeerStateChange(state,uuid)
    
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
    
    def handleEventReport(self,part,msg):
        '''Handle event report from a part
        
        The event report is forwarded to the deplo service. 
        '''
        partName = part.getName()
        typeName = part.getTypeName() 
        bundle = (partName,typeName,) + msg
        self.deplc.reportEvent(bundle)
            
    def terminate(self):
        '''Terminate all functions of the actor. 
        
        Terminate all components, and connections to the deplo/disco services.
        Finally exit the process. 
        '''
        self.logger.info("terminating")
        for component in self.components.values():
            component.terminate()
        time.sleep(1.0)
        self.deplc.terminate()
        self.disco.terminate()
        # Clean up everything
        # self.context.destroy()
        # time.sleep(1.0)
        self.logger.info("terminated")
        os._exit(0)

    
    