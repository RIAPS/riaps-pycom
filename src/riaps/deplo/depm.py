'''
Device manager service main class
Created on Oct 19, 2016

@author: riaps
'''

import os,signal
import sys
import time
import json
import hashlib
from os.path import join
from collections import namedtuple
import subprocess
import threading
import logging
import traceback
import psutil
import pwd
from concurrent.futures.thread import ThreadPoolExecutor
from _thread import RLock

import zmq
from zmq import devices

from riaps.consts.defs import *
from riaps.utils.config import Config
from riaps.proto import deplo_capnp
from riaps.run.exc import BuildError
from riaps.deplo.resm import ResourceManager

DeploAppRecord = namedtuple('DeploAppRecord', 'model hash file')
DeploUserRecord = namedtuple('DeploUserRecord', 'name home uid gid')
DeploActorRecord = namedtuple('DeploActorRecord', 'app actor device')

class DeploymentManager(threading.Thread):
    '''
    Deployment manager service main class, implemented as a thread 
    '''    
    def __init__(self,parent,resm,devm):
        threading.Thread.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.context = parent.context
        self.hostAddress = parent.hostAddress
        self.macAddress = parent.macAddress
        self.suffix = self.macAddress
        self.riapsApps = parent.riapsApps
        self.launchMap = { }            # Map of launched actors
        self.mapLock = RLock()
        self.disco = None
        self.dbaseHost = None 
        self.dbasePort = None
        self.devm = devm        # Device manager
        self.resm = resm        # Resource manager
        self.appModels = { }    # App models loaded
        self.users = { } 
        self.setupUser(Config.TARGET_USER)
        self.appUser = { }
        self.actors = { }       # Actors started

        self.riaps_actor_file = 'riaps_actor'   # Default name for the executable riaps actor shell
        try:
            import riaps.riaps_actor            # Try to import the python riaps_actor first so that we know is correct file name
            self.riaps_actor_file = riaps.riaps_actor.__file__
        except:
            pass
        
        self.riaps_disco_file = 'riaps_disco'   # Default name for the executable riaps disco 
        try:
            import riaps.riaps_disco            # Try to import the python riaps_disco first so that we know is correct file name
            self.riaps_disco_file = riaps.riaps_disco.__file__
        except:
            pass
        
        self.riaps_device_file = 'riaps_device'       # Default name for the executable riaps device shell
        try:
            import riaps.riaps_device          # We try to import the python riaps_device first so that we know is correct file name
            self.riaps_device_file = riaps.riaps_device.__file__
        except:
            pass
        
        self.depmCommandEndpoint = parent.depmCommandEndpoint
        self.devmCommandEndpoint = parent.devmCommandEndpoint
        self.command = self.context.socket(zmq.PAIR)              # Socket to command inner thread
        self.command.bind(self.depmCommandEndpoint)
        self.executor = ThreadPoolExecutor(max_workers=3)
        self.started = False

    def doCommand(self,cmd):
        self.logger.info("doCommand: %s" % str(cmd))
        self.command.send_pyobj(cmd)
        
    def setupUser(self,user_name):
        if user_name in self.users: return
        pw_record = pwd.getpwnam(user_name)
        user_record = DeploUserRecord(
                    name = pw_record.pw_name, 
                    home = pw_record.pw_dir, 
                    uid = pw_record.pw_uid, 
                    gid = pw_record.pw_gid)
        self.users[user_name] = user_record
        
    def delUser(self,user_name):
        if user_name not in self.users: return
        del self.users[user_name]
    
    def makeUserEnv(self,user_name):
        user_env = os.environ.copy()
        user_record = self.users[user_name]
        user_env[ 'HOME'     ]  = user_record.home
        user_env[ 'LOGNAME'  ]  = user_record.name
        user_env[ 'PWD'      ]  = os.getcwd()
        user_env[ 'USER'     ]  = user_record.name
        return user_env

    @staticmethod
    def demote(user_uid,user_gid):
        def result():
            os.setgid(user_gid)
            os.setuid(user_uid)
        return result
        
    def startDisco(self):
        '''
        Start the Discovery Service process 
        '''
        self.logger.info("starting disco")
        disco_prog = 'riaps_disco'
        disco_mod = self.riaps_disco_file   # File name for python script riaps_disco.py

        disco_arg1 = '--database'
        disco_arg2 = '%s:%s' % (self.dbaseHost,self.dbasePort)
        user_record = self.users[Config.TARGET_USER]
        user_env = self.makeUserEnv(Config.TARGET_USER)
        user_uid = user_record.uid
        user_gid = user_record.gid
        user_cwd = os.getcwd()
        command = [disco_prog,disco_arg1,disco_arg2]
        try: 
            self.disco = psutil.Popen(command,
                                      preexec_fn=self.demote(user_uid, user_gid), 
                                      cwd=user_cwd, env=user_env)
        except FileNotFoundError:
            try:
                command = ['python3',disco_mod] + command[1:]
                self.disco = psutil.Popen(command,
                                          preexec_fn=DeploymentManager.demote(user_uid, user_gid), 
                                          cwd=user_cwd, env=user_env)
            except:
                self.logger.error("Error while starting disco: %s" % sys.exc_info()[0])
                raise
        self.logger.info("disco started")


    def setDisco(self,msg):
        assert type(msg) == tuple and len(msg) == 2
        self.dbaseHost, self.dbasePort = msg
        if self.disco == None:
            self.startDisco()
        else:
            self.logger.info('disco already started')
            # Reconnect to new disco dbase?
            pass
    
    def setupApp(self,msg):
        ''' Set up model and unique user name for app'''
        assert type(msg) == tuple and len(msg) == 2
        
        appName,appModelName = msg
        appFolder = join(self.riapsApps, appName)
        appModelPath = join(appFolder, appModelName)
        
        if not os.path.isdir(appFolder):
            raise BuildError('app folder is missing: %s' % appFolder)
        
        # Load the app model
        self.loadModel(appName,appModelPath)
        # Make it unique (to last 4 digits of suffix)
        userName = appName.lower() + self.suffix[-4:]  
        self.appUser[appName] = userName
        self.resm.setupApp(appName,appFolder,userName)  # Adds user 
        self.setupUser(userName)
        
    def cleanupApp(self,msg):
        ''' Clean up everything related to an app'''
        assert type(msg) == tuple and len(msg) == 1
        (appName,) = msg
        if appName not in self.appModels:
            return
        del self.appModels[appName]
        self.resm.cleanupApp(appName)
        if appName not in self.appUser:
            return
        userName = self.appUser[appName]
        del self.appUser[appName]
        self.delUser(userName)
    
    def cleanupApps(self,msg):
        ''' Clean up all known apps '''
        assert type(msg) == tuple and len(msg) == 0
        for k in self.appModels.keys():
            del self.appModels[k]
        self.resm.cleanupApps()
                
    def loadModel(self,appName,modelFileName):
        try:
            fp = open(modelFileName, 'rb')  
        except IOError as e:
            self.logger.error("I/O error({0}): {1}".format(e.errno, e.strerror))
            raise
        except:
            self.logger.error("Unexpected error:", sys.exc_info()[0])
            raise
        # Check if the app model is already loaded
        _fileHash = 0
        fileData = fp.read()
        fileHash = hashlib.md5(fileData).digest()
        fp.close()
        if appName in self.appModels:   # There is an app with this name
            appRecord = self.appModels[appName]
            appHash = appRecord.hash
            if fileHash == appHash:     # Hash is the same, we have the model loaded
                return
        else:
            pass 
        # Not loaded yet (or new)
        fp = open(modelFileName, 'r')  
        try:
            model = json.load(fp)
        except IOError as e:
            self.logger.error("I/O error({0}): {1}".format(e.errno, e.strerror))
            raise
        except:
            self.logger.error("Unexpected error:", sys.exc_info()[0])
            raise
        self.appModels[appName] = DeploAppRecord(hash=fileHash, model=model, file=modelFileName)
        fp.close()
    
    def getAppRecord(self,appName):
        if appName not in self.appModels:
            raise BuildError('App "%s" unknown' % appName)
        return self.appModels[appName]
    
    def getAppModel(self,appName):
        return self.getAppRecord(appName).model
        
    def startActor(self,msg):
        '''
        Start an actor of an application 
        '''
        assert type(msg) == tuple and len(msg) == 4
        appName,appModel,actorName,actorArgs = msg
                
        # Python / C++ starters
        riaps_py_prog = 'riaps_actor'
        riaps_cc_prog = 'start_actor'

        appFolder = join(self.riapsApps, appName)
        appModelPath = join(appFolder, appModel)
         
        if not os.path.isdir(appFolder):
            raise BuildError('App folder is missing: %s' % appFolder)

        # Use Python starter by default
        riaps_prog = riaps_py_prog
        isPython = True

        componentTypes = self.getComponentTypes(appName, actorName)
        if len(componentTypes) == 0:
            raise BuildError('Actor has no components: %s.%s.' % (appName,actorName))
        for componentType in componentTypes:
            # Look up the Python version first
            pyFilePath = join(appFolder, componentType + '.py')
            if not os.path.isfile(pyFilePath):
                isPython = False
        # Mixed mode actors (C++/Python) are not supported. 
        # Better solution: run C++ binaries inside the Python framework
        if not isPython:
            for componentType in componentTypes:
                # Look up the python version
                ccFilePath = join(appFolder, 'lib' + componentType.lower() + '.so')
                if not os.path.isfile(ccFilePath):
                    raise BuildError('Implementation of component %s is missing' % componentType)
            riaps_prog = riaps_cc_prog

        self.resm.addActor(appName, actorName, self.getActorModel(appName, actorName))
        riaps_mod = self.riaps_actor_file   #  File name for python script 'riaps_actor.py'
    
        userName = self.appUser[appName]
        user_record = self.users[userName]
        user_env = self.makeUserEnv(userName)
        user_uid = user_record.uid
        user_gid = user_record.gid
        user_cwd = appFolder
        
        riaps_arg1 = appName
        riaps_arg2 = appModelPath
        riaps_arg3 = actorName
        command = [riaps_prog,riaps_arg1,riaps_arg2,riaps_arg3]
        for arg in actorArgs:
            command.append(arg)
        self.logger.info("Launching %s " % str(command))
        try:
            proc = psutil.Popen(command,
                                preexec_fn=self.demote(user_uid, user_gid), 
                                cwd=user_cwd, env=user_env)
        except (FileNotFoundError,PermissionError):
            try:
                if isPython:
                    command = ['python3',riaps_mod] + command[1:]
                else:
                    command = [riaps_prog] + command[1:]
                proc = psutil.Popen(command,
                                    preexec_fn=self.demote(user_uid, user_gid), 
                                    cwd=user_cwd, env=user_env)
            except:
                self.logger.error("Error while starting actor: %s -- %s" % (command,sys.exc_info()[0]))
                raise
        try:
            rc = proc.wait(1.0)
        except:
            rc = None
        if rc != None:
            raise BuildError("Actor failed to start: %s.%s " % (appName,actorName))
        self.resm.startActor(appName, actorName, proc)
        key = str(appName) + "." + str(actorName)
        with self.mapLock:
            self.launchMap[key] = proc
            self.actors[key] = DeploActorRecord(app = appName, actor=actorName, device=None)

    def getActorModel(self,appName,actorName):
        model = self.getAppModel(appName)
        
        if actorName not in model["actors"]:
            raise BuildError('Actor "%s" unknown' % actorName)
        actorModel = model["actors"][actorName]
        return actorModel
    
    def getComponentTypes(self,appName, actorName):
        '''
        Collects all the component types of an actor.
        '''
        componentTypes = []
        appModel = self.getAppModel(appName)
        componentDefs = appModel["components"]
        actorModel = self.getActorModel(appName,actorName)

        for key in actorModel["instances"]:
            compType = actorModel["instances"][key]["type"]
            if compType in componentDefs:           # Component
                componentTypes.append(compType)
            else:
                pass                                # Device component
            
        return componentTypes
    
    def stopActor(self,appName,actorName):
        '''
        Stop (terminate) the actor of an application  
        '''
        key = str(appName) + "." + str(actorName)
        proc = None
        with self.mapLock:
            if key in self.launchMap:
                proc = self.launchMap[key]
                del self.launchMap[key]
        if proc != None:
            self.logger.info("Halting actor %s" % key)
            self.resm.stopActor(appName, actorName, proc)
            try:          
                proc.terminate()        # Should check for errors
                proc.wait(None)         # TODO (3.0)
            except psutil.TimeoutExpired:
                    self.logger.info("Actor %s did not terminate - killing it" % key)
                    proc.send_signal(signal.SIGKILL)
                    time.sleep(1.0)
            self.logger.info("Halted %s" % key)

    def haltActor(self,msg):
        '''
        Halt (terminate) the actor of an application  
        '''
        assert type(msg) == tuple and len(msg) == 2
        appName,actorName = msg 
        try:
            # self.stopActor(appName, typeName)
            self.executor.submit(self.stopActor,appName,actorName)
        except BuildError as buildError:
            self.logger.error(str(buildError.args[1]))
            
            
    def handleCommand(self,msg):
        self.logger.info("handleCommand: %s" % (str(msg)))
        try: 
            cmd = msg[0]
            if cmd == 'launch':             # Launch an actor
                self.startActor(msg[1:])
            elif cmd == "halt":             # Halt an actor
                self.haltActor(msg[1:])
            elif cmd == "setupApp":         # Setup an app
                self.setupApp(msg[1:])
            elif cmd == "cleanupApp":       # Cleanup an app
                self.cleanupApp(msg[1:])
            elif cmd == "cleanupApps":      # Cleanup all apps
                self.cleanupApps(msg[1:])
            elif cmd == "setDisco":         # Set up disco 
                self.setDisco(msg[1:])
            else:
                pass
        except: 
            info = sys.exc_info()
            self.logger.error("Error in handleCommand '%s': %s %s" % (cmd, info[0], info[1]))
            traceback.print_exc()
        
    def run(self):
        '''
        Main loop of the depl service
        '''
        self.logger.info("starting")
        try:
            # Create main server socket for client requests
            self.server = self.context.socket(zmq.REP)  
            endpoint = const.deplEndpoint
            self.server.bind(endpoint)
            # Control socket for main thread  commands
            self.ctrl = self.context.socket(zmq.PAIR)   
            self.ctrl.connect(self.depmCommandEndpoint)
            # Control socket to devm
            self.devc = self.context.socket(zmq.PAIR)    
            self.devc.connect(self.devmCommandEndpoint)
            # Poller for commands and requests             
            self.poller = zmq.Poller()                   
            self.poller.register(self.server,zmq.POLLIN)
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
        while 1:
            if self.terminated.is_set(): break
            sockets = dict(self.poller.poll(1000.0))            # Poll client messages, with timeout 1 sec
            if len(sockets) == 0:                               # If no message but timeout expired, 
                if self.terminated.is_set(): 
                    break              # break out if terminated
            if self.ctrl in sockets:                # Handle commands
                msg = self.ctrl.recv_pyobj()
                self.handleCommand(msg)
                del sockets[self.ctrl]
            if self.server in sockets:            # Handle client requests
                msg = self.server.recv()
                self.handleClient(msg)
                del sockets[self.server]
            else:
                pass
        self.stop()
    
            
    def handleClient(self,msgBytes):
        '''
        Handle a message form a client 
        '''
        self.logger.info("handleClient")
        try:
            msg = deplo_capnp.DeplReq.from_bytes(msgBytes)
            which = msg.which()
            if which == 'actorReg':
                self.handleActorReg(msg)
            elif which == 'deviceReg':
                self.handleDeviceReq(msgBytes)
            elif which == 'deviceUnreg':
                self.handleDeviceUnreq(msgBytes)
            else:
                pass
        except: 
            info = sys.exc_info()
            self.logger.error("Error in handleClient '%s': %s %s" % (which, info[0], info[1]))
            traceback.print_exc()


    def setupClient(self,appName,appVersion,appActorName):
        '''
        Set up a new client of the deplo manager. The client actors are to register with
        the manager using the 'server' (REQ/REP) socket. The manager will then create a dedicated
        (PAIR) socket for the client to connect to. This socket is used as a private communication
        channel between a specific client actor and the service.   
        '''
        sock = self.context.socket(zmq.PAIR)
        port = sock.bind_to_random_port('tcp://127.0.0.1')
        clientKeyBase = "/" + appName + '/' + appActorName + "/"
        self.clients[clientKeyBase] = sock
        clientKeyLocal = clientKeyBase + self.macAddress
        self.clients[clientKeyLocal] = port
        clientKeyGlobal = clientKeyBase + self.hostAddress
        self.clients[clientKeyGlobal] = port
        sock.close()
        time.sleep(0.1)
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
        
        key = str(appName) + "." + str(appActorName)
        if key not in self.launchMap:
            self.logger.error('unknown actor: %s - rejected' % key)
            rsp = deplo_capnp.DeplRep.new_message()
            rspMessage = rsp.init('actorReg')
            rspMessage.status = 'err'
            rspBytes = rsp.to_bytes()
            self.server.send(rspBytes)   
            return
        
        _actorRecord = self.actors[key]
        
        clientPort = self.setupClient(appName,appVersion,appActorName)
        
        # OptionL store in db host.app.vers.actr -> port? 
        
        device = devices.ThreadDevice(zmq.QUEUE,zmq.DEALER,zmq.PAIR)
        device.setsockopt_in(zmq.IDENTITY, str(key).encode(encoding='utf_8'))
        # device.setsockopt_in(zmq.RCVTIMEO,const.deplEndpointRecvTimeout)
        # device.setsockopt_out(zmq.SNDTIMEO,const.deplEndpointSendTimeout)
        device.bind_out('tcp://127.0.0.1:%i' % clientPort)
        
        self.resm.addClientDevice(appName,appActorName,device)
        time.sleep(0.1)
        device.start()
        
        self.actors[key] = DeploActorRecord(app = appName, actor=appActorName, device=device)
        
        rsp = deplo_capnp.DeplRep.new_message()
        rspMessage = rsp.init('actorReg')
        rspMessage.status = "ok"
        rspMessage.port = clientPort
        rspBytes = rsp.to_bytes()
        self.server.send(rspBytes)
    
    def handleDeviceReq(self,msgBytes):
        '''
        Handle the req for a device 
        '''
        self.devc.send(msgBytes)
        rspBytes = self.devc.recv()
        self.server.send(rspBytes)

    def handleDeviceUnreq(self,msgBytes):
        '''
        Handle the 'unreq' (release) for a device 
        '''
        self.devc.send(msgBytes)
        rspBytes = self.devc.recv() 
        self.server.send(rspBytes)
                
    def stop(self):
        self.logger.info("terminating")
        # Clean up everything
        # Logout from service
        # Kill actors
        for key in self.launchMap.keys():
            appName,actorName = key.split('.')
            self.haltActor(appName, actorName)
        time.sleep(1.0) # Allow actors terminate cleanly
        # Cleanup resm 
        self.resm.cleanupApps()
        # Terminate devm
        if self.devm != None:
            self.devm.terminate()
            self.devm.join()
            self.devm = None
        # Terminate disco
        if self.disco != None:
            self.disco.terminate()
            self.disco = None
        self.logger.info("terminated")


    def terminate(self):
        if self.started:
            self.terminated.set()
