'''
Created on Nov 6, 2016

@author: riaps
'''
import rpyc
import time
import sys
import os
import json
from os.path import join
import subprocess
import zmq
from riaps.consts.defs import *
from riaps.run.exc import *
from riaps.utils.ifaces import getNetworkInterfaces
import logging
from riaps.deplo.resm import ResourceManager
import hashlib
from collections import namedtuple
import psutil
from riaps.deplo.devm import *
import traceback

DeploAppRecord = namedtuple('DeploAppRecord', 'model hash file')

class DeploService(object):
    '''
    Deployment service main class. Each RIAPS mode runs a copy of the Deployment Service, which is
    responsible for starting and managing all RIAPS processes. 
    '''
    def __init__(self,host,port):
        self.logger = logging.getLogger(__name__)
        '''
        Initialize the service with the host:port of the controller node (if provided)
        Note: if the python implementation of the discovery service and/or actor is used, the corresponding python
        script must be in the path. One way to achieve this is to run this script in the same folder 
        '''
        self.ctrlrHost = host 
        self.ctrlrPort = port
        self.conn = None
        self.bgsrv = None
        self.context = zmq.Context()
        self.launchMap = { }            # Map of launched actors
        self.riapsApps = os.getenv('RIAPSAPPS', './')
        self.logger.info("Starting with apps in %s" % self.riapsApps)
        self.disco = None
        self.devm = None
        self.resm = ResourceManager()
        self.appModels = { }    # App models loaded
        
        self.riaps_actor_file = 'riaps_actor'       # Default name for the executable riaps actor shell
        try:
            import riaps.riaps_actor          # We try to import the python riaps_actor first so that we know is correct file name
            self.riaps_actor_file = riaps.riaps_actor.__file__
        except:
            pass
        
        self.riaps_disco_file = 'riaps_disco'       # Default name for the executable riaps disco 
        try:
            import riaps.riaps_disco         # We try to import the python riaps_disco first so that we know is correct file name
            self.riaps_disco_file = riaps.riaps_disco.__file__
        except:
            pass
        
#         self.riaps_devm_file = 'riaps_devm'       # Default name for the executable riaps devm 
#         try:
#             import riaps.riaps_devm         # We try to import the python riaps_devm first so that we know is correct file name
#             self.riaps_devm_file = riaps.riaps_devm.__file__
#         except:
#             pass

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
        self.nodeName = str(self.hostAddress)
        self.conn = None
        self.bgsrv = None
        self.dbaseHost = None
        self.dbasePort = None
           
    def login(self,retry = True):
        '''
        Log in to the controller. First  to reach the controller via the standard service registry, 
        if that fails try to access it via the supplied hostname/port arguments. If that fails, sleep a
        little and try again. 
        '''
        while True:
            try:
                self.logger.info("try to login with rpyc service registry %s" %const.ctrlServiceName)
                self.conn = rpyc.connect_by_service(const.ctrlServiceName)
                break
            except:
                self.logger.warning(" failed to login with rpyc service registry %s" %const.ctrlServiceName)
                try:  
                    self.logger.info("try to connect to rpyc with hostname/port %s/%s" %(self.ctrlrHost, self.ctrlrPort))
                    self.conn = rpyc.connect(self.ctrlrHost,self.ctrlrPort)
                    break
                except:
                    self.logger.warning("Failed to connect to rpyc with hostname/port %s/%s" %(self.ctrlrHost, self.ctrlrPort))                
                    if retry == False:
                        return False
                    time.sleep(5)
                    continue
        self.bgsrv = rpyc.BgServingThread(self.conn,self.handleBgServingThreadException)       
        resp = self.conn.root.login(self.hostAddress,self.callback,self.riapsApps)
        if type(resp) == tuple and resp[0] == 'dbase':   # Expected response: (redis) database host:port pair
            (_,host,port) = resp
            self.dbaseHost = host
            self.dbasePort = port
            return True
        else:
            pass    # Ignore any other response
            return False
        
    def startDisco(self):
        '''
        Start the Discovery Service process 
        '''
        disco_prog = 'riaps_disco'
        disco_mod = self.riaps_disco_file   # File name for python script riaps_disco.py

        disco_arg1 = '--database'
        disco_arg2 = '%s:%s' % (self.dbaseHost,self.dbasePort)
        command = [disco_prog,disco_arg1,disco_arg2]
        try: 
            self.disco = subprocess.Popen(command)
        except FileNotFoundError:
            try:
                command = ['python3',disco_mod] + command[1:]
                self.disco = subprocess.Popen(command)
            except:
                self.logger.error("Error while starting disco: %s" % sys.exc_info()[0])
                raise
    
    def startDevm(self):
        '''
        Start the Device manager service process 
        '''
        self.devm = DevmService(self)
        try:
            self.devm.start()
        except:
            self.logger.error("Error while starting devm: %s" % sys.exc_info()[0])
            raise
        
#         devm_prog = 'riaps_devm'
#         devm_mod = self.riaps_devm_file   # File name for python script riaps_devm.py
# 
#         command = [devm_prog]
#         try: 
#             self.devm = subprocess.Popen(command)
#         except FileNotFoundError:
#             try:
#                 command = ['python3',devm_mod] + command[1:]
#                 self.devm = subprocess.Popen(command)
#             except:
#                 self.logger.error("Error while starting devm: %s" % sys.exc_info()[0])
#                 raise

    def setupApp(self,appName,appModelName):
        appFolder = join(self.riapsApps, appName)
        appModelPath = join(appFolder, appModelName)
        
        if not os.path.isdir(appFolder):
            raise BuildError('App folder is missing: %s' % appFolder)
        
        # Load the app model
        self.loadModel(appName,appModelPath)
        
        #The startApp and cleanupApp do not depend on the json 
        self.resm.startApp(appName)
        
    def cleanupApp(self,appName):
        del self.appModels[appName]
        #The startApp and cleanupApp do not depend on the json 
        self.resm.cleanupApp(appName)
    
    def cleanupApps(self):
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
        fileHash = 0
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
        
    def startActor(self,appName,appModel,actorName,actorArgs):
        '''
        Start an actor of an application 
        '''

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
        # We don't allow mixed mode actors (C++ and Python components in the same actor).
        # A better solution is to support running C++ binaries into the Python framework. 
        if not isPython:
            for componentType in componentTypes:
                # Look up the python version
                ccFilePath = join(appFolder, 'lib' + componentType.lower() + '.so')
                if not os.path.isfile(ccFilePath):
                    raise BuildError('Implementation of component %s is missing' % componentType)
            riaps_prog = riaps_cc_prog


        #This around resm.addActor is a measure to handle the fact that the 
        # dsml generated json does not have the "usage" key. 
        # self.RM is used to either enable or disable the resource manager commands. 
        ActorModel = self.getActorModel(appName, actorName)
        if "usage" in ActorModel:
            print("can create resource manager")
            self.RM = True
        else:
            print("don't create resource manager")
            self.RM = False
        
        if self.RM:
            self.resm.addActor(appName, actorName, self.getActorModel(appName, actorName))
        riaps_mod = self.riaps_actor_file   #  File name for python script 'riaps_actor.py'
        #---------------------------------------------------------------------------------
        
        riaps_arg1 = appName
        riaps_arg2 = appModelPath
        riaps_arg3 = actorName
        command = [riaps_prog,riaps_arg1,riaps_arg2,riaps_arg3]
        for arg in actorArgs:
            command.append(arg)
        self.logger.info("Launching %s " % str(command))
        try:
            self.logger.warning("appFolder %s" %str(appFolder))
            self.logger.warning("cwd %s" %os.getcwd())
            os.makedirs(os.path.dirname(appFolder+"/logs/"), exist_ok=True)
            with open(appFolder+"/logs/"+actorName+".txt","w") as out:
                out.write('some text, as header of the file\n')
                out.flush()  # <-- here's something not to forget!
                proc = psutil.Popen(command,cwd=appFolder, stdout=out,stderr=out, universal_newlines = True)
        except FileNotFoundError:
            try:
                if isPython:
                    command = ['python3',riaps_mod] + command[1:]
                else:
                    command = [riaps_prog] + command[1:]
                proc = psutil.Popen(command,cwd=appFolder)
            except:
                self.logger.error("Error while starting actor: %s -- %s" % (command,sys.exc_info()[0]))
                raise
        try:
            rc = proc.wait(1.0)
        except:
            rc = None
        if rc != None:
            raise BuildError("Actor failed to start: %s.%s " % (appName,actorName))
        
        if self.RM:
            self.resm.startActor(appName, actorName, proc)
        
        
        key = str(appName) + "." + str(actorName)
        # ADD HERE: build comm channel to the actor for control purposes
        self.launchMap[key] = proc

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
    
    def haltActor(self,appName,actorName):
        '''
        Halt (terminate) the actor of an application  
        '''
        key = str(appName) + "." + str(actorName)
        if key in self.launchMap:
            proc = self.launchMap[key]
            self.logger.info("halting %s" % key)
            if self.RM:
                self.resm.stopActor(appName, actorName, proc)
            
            proc.terminate()                             # Should check for errors
            while True:
                try:
                    proc.wait(3.0)
                    break
                except psutil.TimeoutExpired:
                    self.logger.info("%s did not terminate" % key)
            self.logger.info("halted %s" % key)
            del self.launchMap[key]


        
    def setup(self):
        '''
        Set up the discovery and device management services
        '''
        self.setupIfaces()
        self.login()
        if self.dbaseHost != None and self.dbasePort != None:
            self.startDisco()
        self.startDevm()
    
    def run(self):
        '''
        Main loop of the Deployment Service 
        '''
        self.poller = zmq.Poller()
        ok = True
        while True:     # Placeholder code
            time.sleep(1.0)
            # Poll controlled actors for messages
#             sockets = dict(self.poller.poll(1000.0))
#             if len(sockets) == 0:
#                 pass
#             else:
#                 pass
            # If background server 
            if self.bgsrv == None and self.conn == None: 
                if ok: 
                    self.logger.info("Connection to controller lost - retrying")
                ok = self.login(retry=False)

    def handleBgServingThreadException(self):
        '''
        Background thread exception server. Called when the thread is about to terminate due 
        to, e.g. loss of connection to the controller. The setting of the bgsrv/conn to None 
        indicates to the main thread that connectivity is lost and should be re-built. 
        '''
        self.bgsrv = None
        self.conn = None
        
    def callback(self,msg):
        '''
        Callback from server - runs in the the background server thread
        NOTE: This will likely change as the startActor/haltActor has to create/manage ZMQ
        sockets to connect to the actor (and that should happen in the main thread). Possible
        solution: push the command into a message queue that is read by the main thread.   
        '''
        assert type(msg) == tuple
        try: 
            cmd = msg[0]
            if cmd == 'launch':             # Launch an actor
                appName = msg[1]
                appModelName = msg[2]
                actorName = msg[3]
                actorArgs = msg[4]
                self.startActor(appName,appModelName,actorName,actorArgs)
            elif cmd == "halt":
                appName = msg[1]
                actorName = msg[2]
                self.haltActor(appName,actorName)                   
                    
            elif cmd == "setupApp":
                appName = msg[1]
                appModelName = msg[2]
                self.setupApp(appName,appModelName)
            elif cmd == "cleanupApp":
                appName = msg[1]
                self.cleanupApp(appName)
            elif cmd == "cleanupApps":
                self.cleanupApps()
            else:
                pass                # Should flag an error
        except BuildError as buildError:
            self.logger.error(str(buildError.args))
            raise
        except:
            info = sys.exc_info()
            self.logger.error("Error in callback '%s': %s %s" % (cmd, info[0], info[1]))
            traceback.print_exc()
            raise
        
            
    def terminate(self):
        self.logger.info("terminating")
        # Clean up everything
        # Logout from service
        # Kill actors
        for key in self.launchMap.keys():
            appName,actorName = key.split('.')
            self.haltActor(appName, actorName)
        time.sleep(1.0) # Allow actors terminate cleanly
        # Cleanup resm 
        if self.RM:
            self.resm.cleanupApps()
        # Kill devm
        if self.devm != None:
            self.devm.terminate()
            self.devm.join()
            self.devm = None
        # Kill disco
        if self.disco != None:
            self.disco.terminate()
            self.disco = None
        self.context.destroy()
        time.sleep(1.0)
        self.logger.info("terminated")
        os._exit(0)
        