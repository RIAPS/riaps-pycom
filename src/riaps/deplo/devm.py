'''
Device manager service main class
Created on Oct 19, 2016

@author: riaps
'''
import zmq
import capnp
import os
import sys
import time
from os.path import join
import subprocess
import threading
from riaps.proto import devm_capnp
from riaps.consts.defs import *
from riaps.run.exc import BuildError
from riaps.utils.ifaces import getNetworkInterfaces
import logging
import psutil
  
class DevmService(threading.Thread):
    '''
    Device manager service main class, implemented as a thread 
    '''    
    def __init__(self,parent):
        threading.Thread.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.context = parent.context
        self.hostAddress = parent.hostAddress
        self.macAddress = parent.macAddress
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
        
    def terminate(self):
        self.terminated.set()
        
    def run(self):
        '''
        Main loop of the devm service
        '''
        self.logger.info("starting")
        # Socket and poller for comm
        self.server = self.context.socket(zmq.REP)              # Create main server socket for client requests
        endpoint = const.devmEndpoint + self.suffix
        self.server.bind(endpoint)
        self.poller = zmq.Poller()                              # Set up initial poller (only on the main server socket)  
        self.poller.register(self.server,zmq.POLLIN)
        # Map of clients
        self.clients = { }  
        # Event for termination
        self.terminated = threading.Event()     # Event flag to signal termination
        self.terminated.clear()
        self.logger.info("running")
        # 
        while 1:
            if self.terminated.is_set(): break
            sockets = dict(self.poller.poll(1000.0))            # Poll client messages, with timeout 1 sec
            if len(sockets) == 0:                               # If no message but timeout expired, 
                if self.terminated.is_set(): 
                    break              # break out if terminated
            elif self.server in sockets:               # If there is a server request, handle it 
                msg = self.server.recv()
                self.handle(msg)
                del sockets[self.server]
            else:
                pass
        self.stop()
    
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
        riaps_py_prog = 'riaps_device'      # Python executor
        riaps_cc_prog = 'start_actor'       # C++ executor
        
        riaps_prog = riaps_py_prog          # Use Python starter first
        riaps_mod = self.riaps_device_file  # Module file name for script 
        isPython = True
        
        appFolder = join(self.riapsApps,appName)
        appModelPath = join(appFolder,appModel)
        
        if not os.path.isdir(appFolder):
            raise BuildError('App folder is missing: %s' % appFolder)
        
        componentType = actorName 
        # Look up the Python version first
        pyFilePath = join(appFolder, componentType + '.py')
        if os.path.isfile(pyFilePath):
            pass                # Use the Python implementation
        else:                   # Find C++ implementation
            isPython = False
            ccFilePath = join(appFolder, 'lib' + componentType.lower() + '.so')
            if not os.path.isfile(ccFilePath):
                raise BuildError('Implementation of component %s is missing' % componentType)
            riaps_prog = riaps_cc_prog
        
        # Problem: How do we add a device actor to the resource manager?
        
        riaps_arg1 = appName 
        riaps_arg2 = appModelPath
        riaps_arg3 = actorName
        command = [riaps_prog,riaps_arg1,riaps_arg2,riaps_arg3]
        for arg in actorArgs:
            command.append(arg)
        self.logger.info("Launching %s " % str(command))
                
        try:
            proc = psutil.Popen(command,cwd=appFolder)
        except FileNotFoundError:
            try:
                if isPython: 
                    command = ['python3',riaps_mod] + command[1:]
                else:
                    command = [riaps_prog] + command[1:]
                proc = psutil.Popen(command,cwd=appFolder)
            except:
                raise BuildError("Error while starting device: %s" % sys.exc_info()[1])
        rc = proc.poll()
        if rc != None:
            raise BuildError("Device failed to start: %s " % (command,))
        # Problem: How do we add a device actor to the resource manager?
        key = str(appName) + "." + str(actorName)
        # ADD HERE: build comm channel to the device for control purposes
        self.launchMap[key] = proc

    def stopDevice(self,appName,appModel,actorName):
        '''
        Stop a device actor of an application 
        '''
        
        key = str(appName) + "." + str(actorName)
        if key in self.launchMap:
            proc = self.launchMap[key]
        
            self.logger.info("Stopping device %s" % key)
            proc.terminate()                             # Should check for errors
            del self.launchMap[key]
        else:
            raise BuildError("Device %s not found" % key)
    
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
        
        ok = True
        try:
            self.startDevice(appName, modelName, typeName, cmdArgs)
        except BuildError as buildError:
            ok = False
            self.logger.error(str(buildError.args[0]))

        #      
        rsp = devm_capnp.DevmRep.new_message()
        rspMessage = rsp.init('deviceReg')
        rspMessage.status = "ok" if ok else "err"
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
       
        ok = True
        try:
            self.stopDevice(appName, modelName, typeName)
        except BuildError as buildError:
            ok = False
            self.logger.error(str(buildError.args[1]))
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
        
    def stop(self):
        self.logger.info("stopping")
        # Clean up everything
        # Kill actors
        for proc in self.launchMap.values():
            proc.terminate()
        time.sleep(1.0)         # Allow actors terminate cleanly
        self.logger.info("stopped")
        
        
