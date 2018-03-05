'''
Device manager service main class
Created on Oct 19, 2016

@author: riaps
'''
import zmq
import capnp
import os,signal
import sys
import time
from os.path import join
import subprocess
import threading
import logging
import traceback
import concurrent.futures

import psutil
from psutil import TimeoutExpired

from riaps.proto import deplo_capnp
from riaps.consts.defs import *
from riaps.run.exc import BuildError
from concurrent.futures.thread import ThreadPoolExecutor
from _thread import RLock
  
class DeviceManager(threading.Thread):
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
        self.mapLock = RLock()
        self.riapsApps = parent.riapsApps
        self.riaps_device_file = 'riaps_device'       # Default name for the executable riaps device shell
        try:
            import riaps.riaps_device          # We try to import the python riaps_device first so that we know is correct file name
            self.riaps_device_file = riaps.riaps_device.__file__
        except:
            pass
        self.devmCommandEndpoint = parent.devmCommandEndpoint
        self.executor = ThreadPoolExecutor(max_workers=3)
        self.started = False
        
    def terminate(self):
        if self.started:
            self.terminated.set()
        
    def run(self):
        '''
        Main loop of the depl service
        '''
        self.logger.info("starting")
        try:
            # Socket for commands from deplo
            self.ctrl = self.context.socket(zmq.PAIR)            
            self.ctrl.bind(self.devmCommandEndpoint)
            # Initial poller (on server and command sockets) 
            self.poller = zmq.Poller()                               
#             self.poller.register(self.server,zmq.POLLIN)
            self.poller.register(self.ctrl,zmq.POLLIN)
            # Map of clients
            self.clients = { }  
            # Event for termination
            self.terminated = threading.Event()     # Event flag to signal termination
            self.terminated.clear()
            self.logger.info("running")
            self.started = True
        # 
        except:
            self.logger.error("start failed")
            self.stop()
        while True:
            if self.terminated.is_set(): break
            sockets = dict(self.poller.poll(1000.0))            # Poll client messages, with timeout 1 sec
            if len(sockets) == 0:                               # If no message but timeout expired, 
                # self.logger.info("poller timeout")
                if self.terminated.is_set(): 
                    break              # break out if terminated
            if self.ctrl in sockets:
                msg = self.ctrl.recv()
                self.handleCommand(msg)
                del sockets[self.ctrl]
#             if self.server in sockets:              # If there is a server request, handle it 
#                 msg = self.server.recv()
#                 # self.handle(msg)
#                 del sockets[self.server]
        self.stop()
    
    def handleCommand(self,msgBytes):
        '''
        Dispatch the request based on the message type
        '''
        self.logger.info("handleCommand")
        msg = deplo_capnp.DeplReq.from_bytes(msgBytes)
        which = msg.which()
        if which == 'deviceReg':
            self.handleDeviceReq(msg)
        elif which == 'deviceUnreg':
            self.handleDeviceUnreq(msg)
        else:
            self.logger.warning('unknown command: %s' % which)
    
    
    def startDevice(self,appName,appModel,actorName,actorArgs):
        '''
        Start a device actor of an application 
        '''
        riaps_py_prog = 'riaps_device'      # Python executor
        riaps_cc_prog = 'start_device'      # C++ executor
        
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
            proc = subprocess.Popen(command,cwd=appFolder)
        except FileNotFoundError:
            try:
                if isPython: 
                    command = ['python3',riaps_mod] + command[1:]
                else:
                    command = [riaps_prog] + command[1:]
                proc = subprocess.Popen(command,cwd=appFolder)
            except:
                raise BuildError("Error while starting device: %s" % sys.exc_info()[1])
        try:
            rc = proc.wait(1.0)
        except:
            rc = None
        if rc != None:
            raise BuildError("Device failed to start: %s " % (command,))
        # Problem: How do we add a device actor to the resource manager?
        key = str(appName) + "." + str(actorName)
        # ADD HERE: build comm channel to the device for control purposes
        with self.mapLock:
            self.launchMap[key] = proc

    def stopDevice(self,appName,actorName):
        '''
        Stop a device actor of an application 
        '''        
        key = str(appName) + "." + str(actorName)
        proc = None
        with self.mapLock:
            if key in self.launchMap:
                proc = self.launchMap[key]
                del self.launchMap[key]
        if proc != None:
            self.logger.info("Stopping device %s" % key)
            try: 
                proc.terminate()            # Should check for errors
                proc.wait(None)             # TODO: (3.0)
            except psutil.TimeoutExpired:
                self.logger.info("Device %s did not stop - killing it" % key)
                proc.send_signal(signal.SIGKILL)
                time.sleep(1.0)
            except:
                traceback.print_exc()
            self.logger.info("Stopped %s" % key)
    
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
        rsp = deplo_capnp.DeplRep.new_message()
        rspMessage = rsp.init('deviceReg')
        rspMessage.status = "ok" if ok else "err"
        rspBytes = rsp.to_bytes()
        self.ctrl.send(rspBytes)
        self.logger.info("handleDeviceReq: done")

    def handleDeviceUnreq(self,msg):
        '''
        Handle the 'unreq' (release) for a device 
        '''
        devReg = msg.deviceUnreg
        appName = devReg.appName 
        _modelName = devReg.modelName
        typeName = devReg.typeName
        self.logger.info("handleDeviceUnreq: %s,%s" % (appName,typeName))
       
        ok = True
        try:
            # self.stopDevice(appName, typeName)
            self.executor.submit(self.stopDevice,appName,typeName)
        except BuildError as buildError:
            ok = False
            self.logger.error(str(buildError.args[1]))
        #      
        rsp = deplo_capnp.DeplRep.new_message()
        rspMessage = rsp.init('deviceUnreg')
        rspMessage.status = "ok" if ok else "err"
        rspBytes = rsp.to_bytes()
        self.ctrl.send(rspBytes)
        self.logger.info("handleDeviceUnreq: done")
        
    def stop(self):
        self.logger.info("stopping")
        # Clean up everything
        # Kill actors
        for key in self.launchMap.keys():
            appName,actorName = key.split('.')
            #self.stopDevice(appName, actorName)
            self.executor.submit(self.stopDevice,appName,actorName)
        time.sleep(1.0)         # Allow actors terminate cleanly
        self.logger.info("stopped")
        
        
