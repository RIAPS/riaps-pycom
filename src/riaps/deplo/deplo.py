'''
Created on Nov 6, 2016

@author: riaps
'''
import rpyc
import time
import sys
import os
from os.path import join
import subprocess
import zmq
from riaps.consts.defs import *
from riaps.utils.ifaces import getNetworkInterfaces
from riaps.run.exc import SetupError
import logging
    
class DeploService(object):
    '''
    Deployment service main class. Each RIAPS mode runs a copy of the Deployment Service, which is
    responsible for starting and managing all RIAPS processes. 
    '''
    def __init__(self, host,port):
        self.logger = logging.getLogger(__name__)
        '''
        Initialize the service with the host:port of the controller node (if provided)
        '''
        self.ctrlrHost = host 
        self.ctrlrPort = port
        self.conn = None
        self.bgsrv = None
        self.context = zmq.Context()
        self.launchMap = { }            # Map of launched actors
        self.riapsApps = os.getenv('RIAPSAPPS', './')
        self.logger.info("Starting with apps in %s" % self.riapsApps)

    def setupIfaces(self):
        '''
        Find the IP addresses of the (host-)local and network(-global) interfaces
        '''
        (globalIPs,globalMACs,localIP) = getNetworkInterfaces()
        assert len(globalIPs) > 0 and len(globalMACs) > 0
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
        Log in to the controller. First try to reach the controller via the standard service registry, 
        if that fails try to access it via the supplied hostname/port arguments. If that fails, sleep a
        little and try again. 
        '''
        while True:
            try:
                self.conn = rpyc.connect_by_service(const.ctrlServiceName)
                break
            except:
                try:  
                    self.conn = rpyc.connect(self.ctrlrHost,self.ctrlrPort)
                    break
                except:
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
        riaps_folder = os.getenv('RIAPSHOME', './')
        disco_mod = join(riaps_folder,'disco.py')
        disco_arg1 = '--database'
        disco_arg2 = '%s:%s' % (self.dbaseHost,self.dbasePort)
        try: 
            self.disco = subprocess.Popen(['python3',disco_mod,disco_arg1,disco_arg2])
        except:
            self.logger.error("Error: %s" % sys.exc_info()[0])
            raise
    
    def startActor(self,appName,appModel,actorName,actorArgs):
        '''
        Start an actor of an application 
        '''
        
        riaps_folder = os.getenv('RIAPSHOME', './')
        riaps_mod = join(riaps_folder,'riaps.py')
        
        appFolder = join(self.riapsApps,appName)
        appModelPath = join(appFolder,appModel)
        riaps_arg1 = appName 
        riaps_arg2 = appModelPath
        riaps_arg3 = actorName
        command = ['python3',riaps_mod,riaps_arg1,riaps_arg2,riaps_arg3]
        for arg in actorArgs:
            command.append(arg)
        try: 
            self.logger.info("Launching %s " % str(command[2:]))
            proc = subprocess.Popen(command,cwd=appFolder)
            key = str(appName) + "." + str(actorName)
            # ADD HERE: build comm channel to the actor for control purposes
            self.launchMap[key] = proc
        except:
            self.logger.error("Error: %s" % sys.exc_info()[0])
            raise
    
    def haltActor(self,appName,actorName):
        '''
        Halt (terminate) the actor of an application  
        '''
        key = str(appName) + "." + str(actorName)
        if key in self.launchMap:
            proc = self.launchMap[key]
            self.logger.info("Halting %s" % key)
            proc.terminate()                             # Should check for errors
            del self.launchMap[key]

        
    def setup(self):
        '''
        Set up the discovery service
        '''
        self.setupIfaces()
        self.login()
        if self.dbaseHost != None and self.dbasePort != None:
            self.startDisco()
            
    
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
        else:
            pass                # Should flag an error

