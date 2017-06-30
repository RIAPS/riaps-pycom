'''
Devmvery Service main class
Created on Oct 19, 2016

@author: riaps
'''
import zmq
import capnp
import os
import sys
from os.path import join
import subprocess

from riaps.proto import devm_capnp
from riaps.consts.defs import *
from riaps.utils.ifaces import getNetworkInterfaces
import logging

class DevmService(object):
    '''
    Devmvery service main class. 
    '''
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.context = zmq.Context()
        self.setupIfaces()
        self.suffix = self.macAddress
        self.launchMap = { }            # Map of launched actors
        self.riapsApps = os.getenv('RIAPSAPPS', './')
        self.logger.info("Starting with apps in %s" % self.riapsApps)
        self.riaps_device_file = 'riaps_device'       # Default name for the executable riaps device shell
        try:
            import riaps.riaps_device          # We try to import the python riaps_device first so that we know is correct file name
            self.riaps_device_file = riaps.riaps_device.__file__
        except:
            pass
    
    def setupIfaces(self):
        '''
        Find the IP addresses of the (host-)local and network(-global) interfaces
        '''
        (globalIPs,globalMACs,localIP) = getNetworkInterfaces()
        try:
            assert len(globalIPs) > 0 and len(globalMACs) > 0
        except:
            self.logger.error("Error: no active network interface")
            raise
        globalIP = globalIPs[0]
        globalMAC = globalMACs[0]
        self.hostAddress = globalIP
        self.macAddress = globalMAC
        
    def start(self):
        self.logger.info("starting")
        self.server = self.context.socket(zmq.REP)              # Create main server socket for client requests
        endpoint = const.devmEndpoint + self.suffix
        self.server.bind(endpoint)
        
        self.poller = zmq.Poller()                              # Set up initial poller (only on the main server socket)  
        self.poller.register(self.server,zmq.POLLIN)
        self.portMap = { }
        self.clients = { }  
        self.clientUpdates = []
    
    def run(self):
        '''
        Main loop of the devm service
        '''
        self.logger.info("running")
           
        while 1:
            self.clientUpdates = []
            sockets = dict(self.poller.poll())       # Poll client messages
            if self.server in sockets:               # If there is a server request, handle it 
                msg = self.server.recv()
                self.handle(msg)
                del sockets[self.server]
            else:
                pass
            for note in self.clientUpdates:          # Handle all client updates (received from dcas)
                pass

    
    def setupClient(self,appName,appVersion,appActorName):
        '''
        Set up a new client of the devm service. The client actors are to register with
        the service using the 'server' (REQ/REP) socket. The service will then create a dedicated
        (PAIR) socket for the client to connect to. This socket is used as a private communication
        channel between a specific client actor and the service.   
        '''
        sock = self.context.socket(zmq.PAIR)
        port = sock.bind_to_random_port('tcp://*')
        clientKeyBase = "/" + appName + '/' + appActorName + "/"
        self.clients[clientKeyBase] = sock
        clientKeyLocal = clientKeyBase + self.macAddress
        self.clients[clientKeyLocal] = port
        clientKeyGlobal = clientKeyBase + self.hostAddress
        self.clients[clientKeyGlobal] = port
        return port
    
    def handleActorReg(self,msg):
        '''
        Handle the registration of an application actor with the service. 
        '''
        actReg = msg.actorReg
        appName = actReg.appName
        appVersion = actReg.version   
        appActorName = actReg.actorName
         
        self.logger.info("handleActorReg: %s %s" % (appName, appActorName))
        
        clientPort = self.setupClient(appName,appVersion,appActorName)
        
        # OptionL store in db host.app.vers.actr -> port? 
        
        rsp = devm_capnp.DevmRep.new_message()
        rspMessage = rsp.init('actorReg')
        rspMessage.status = "ok"
        rspMessage.port = clientPort
        rspBytes = rsp.to_bytes()
        self.server.send(rspBytes)
    
    def startDevice(self,appName,appModel,actorName,actorArgs):
        '''
        Start a device actor of an application 
        '''
        riaps_prog = 'riaps_device'
        riaps_mod = self.riaps_device_file   #  File name for python script 'riaps_device.py'
        
        appFolder = join(self.riapsApps,appName)
        appModelPath = join(appFolder,appModel)
        riaps_arg1 = appName 
        riaps_arg2 = appModelPath
        riaps_arg3 = actorName
        command = [riaps_prog,riaps_arg1,riaps_arg2,riaps_arg3]
        for arg in actorArgs:
            command.append(arg)
        self.logger.info("Launching %s " % str(command))
                
        try:
            proc = subprocess.Popen(command,cwd=appFolder)
        except FileNotFoundError:
            try:
                command = ['python3',riaps_mod] + command[1:]
                proc = subprocess.Popen(command,cwd=appFolder)
            except:
                self.logger.error("Error while starting actor: %s" % sys.exc_info()[0])
                raise
        key = str(appName) + "." + str(actorName)
        # ADD HERE: build comm channel to the device for control purposes
        self.launchMap[key] = proc

    def stopDevice(self,appName,appModel,actorName):
        '''
        Stop a device actor of an application 
        '''
        
        key = str(appName) + "." + str(actorName)
        proc = self.launchMap[key]
        
        self.logger.info("Stopping device %s" % key)
        proc.terminate()                             # Should check for errors
        del self.launchMap[key]
    
    def handleDeviceReq(self,msg):
        '''
        Handle the req for a device 
        '''
        devReg = msg.deviceReg
        appName = devReg.appName 
        modelName = devReg.modelName
        typeName = devReg.typeName
        self.logger.info("handleDeviceReq: %s,%s,%s " % (appName,typeName,str(devReg.deviceArgs)))
        
        cmdArgs = []
        for deviceArg in devReg.deviceArgs:
            argName = deviceArg.name
            argValue = deviceArg.value
            cmdArgs.append('--' + argName)
            cmdArgs.append(argValue)
        
        self.startDevice(appName, modelName, typeName, cmdArgs)

        #      
        rsp = devm_capnp.DevmRep.new_message()
        rspMessage = rsp.init('deviceReg')
        rspMessage.status = "ok"
        rspBytes = rsp.to_bytes()
        self.server.send(rspBytes)

    def handleDeviceUnreq(self,msg):
        '''
        Handle the 'unreq' (release) for a device 
        '''
        devReg = msg.deviceUnreg
        appName = devReg.appName 
        modelName = devReg.modelName
        typeName = devReg.typeName
        self.logger.info("handleDeviceUnreq: %s,%s" % (appName,typeName))
       
        self.stopDevice(appName, modelName, typeName)

        #      
        rsp = devm_capnp.DevmRep.new_message()
        rspMessage = rsp.init('deviceUnreg')
        rspMessage.status = "ok"
        rspBytes = rsp.to_bytes()
        self.server.send(rspBytes)
        
    def handle(self,msgBytes):
        '''
        Dispatch the request based on the message type
        '''
        msg = devm_capnp.DevmReq.from_bytes(msgBytes)
        which = msg.which()
        if which == 'actorReg':
            self.handleActorReg(msg)
        elif which == 'deviceReg':
            self.handleDeviceReq(msg)
        elif which == 'deviceUnreg':
            self.handleDeviceUnreq(msg)
        else:
            pass
        
    def terminate(self):
        pass
        
