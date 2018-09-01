'''
Created on Nov 6, 2016

@author: riaps
'''


import time
import sys
import os
import logging
import zmq
import rpyc
rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True

from riaps.consts.defs import *
from riaps.utils.config import Config
from riaps.run.exc import *
from riaps.utils.ifaces import getNetworkInterfaces
# from riaps.deplo.devm import DeviceManager
from riaps.deplo.depm import DeploymentManager
from riaps.deplo.resm import ResourceManager
from riaps.deplo.fm import FaultManager
from riaps.utils.singleton import singleton
from czmq import Zsys

import traceback

class DeploService(object):
    '''
    Deployment service main class. Each RIAPS mode runs a copy of the Deployment Service, which is
    responsible for starting and managing all RIAPS processes. 
    '''
    def __init__(self,host,port):
        self.logger = logging.getLogger(__name__)
        '''
        Initialize the service with the host:port of the controller node (if provided)
        Note: if the Python implementation of the discovery service and/or actor is used, the corresponding
        script must be in the path. One way to achieve this is to run this script in the same folder 
        '''
        self.riapsApps = os.getenv('RIAPSAPPS', './')
        self.logger.info("Starting with apps in %s" % self.riapsApps)
        if os.getuid() != 0:
            self.logger.warning("running in unprivileged mode, some functions may fail")

        self.ctrlrHost = host 
        self.ctrlrPort = port
        self.conn = None
        self.bgsrv = None
        # self.context = zmq.Context() - Use czmq's context (see fm / zyre socket)
        czmq_ctx = Zsys.init()
        self.context = zmq.Context.shadow(czmq_ctx.value)
        self.setupIfaces()
        self.suffix = self.macAddress
        singleton('riaps_deplo',self.suffix)
        self.depmCommandEndpoint = 'inproc://depm-command'
        # self.devmCommandEndpoint = 'inproc://devm-command'
        self.procMonEndpoint = 'inproc://procmon'
        self.resm = ResourceManager(self.context)
        self.fm = FaultManager(self,self.context)
        # self.devm = DeviceManager(self)
        self.depm = DeploymentManager(self,self.resm,self.fm)   

    def setupIfaces(self):
        '''
        Find the IP addresses of the (host-)local and network(-global) interfaces
        '''
        (globalIPs,globalMACs,globalNames,_localIP) = getNetworkInterfaces()
        try:
            assert len(globalIPs) > 0 and len(globalMACs) > 0
        except:
            self.logger.error("Error: no active network interface")
            raise
        globalIP = globalIPs[0]
        globalMAC = globalMACs[0]
        if Config.NIC_NAME == None:
            Config.NIC_NAME = globalNames[0]
        self.hostAddress = globalIP
        self.macAddress = globalMAC
        self.nodeName = str(self.hostAddress)
           
    def login(self,retry = True):
        '''
        Log in to the controller. First try to reach the controller via the standard service registry, 
        if that fails try to access it via the supplied hostname/port arguments. If that fails, sleep a
        little and try again. 
        '''
        while True:
            try:
                self.conn = rpyc.connect_by_service(const.ctrlServiceName,config = {"allow_public_attrs" : True})
                break
            except:
                try:  
                    self.conn = rpyc.connect(self.ctrlrHost,self.ctrlrPort,config = {"allow_public_attrs" : True})
                    break
                except:
                    if retry == False:
                        return False
                    time.sleep(5)
                    continue
        self.bgsrv = rpyc.BgServingThread(self.conn,self.handleBgServingThreadException)       
        resp = self.conn.root.login(self.hostAddress,self.callback,self.riapsApps)
        if type(resp) == tuple and resp[0] == 'dbase':   # Expected response: (redis) database host:port pair
            if self.depm != None:
                self.depm.doCommand(('setDisco',) + resp[1:])
            return True
        else:
            pass    # Ignore any other response
            return False
        
    def setup(self):
        '''
        Start device and deployment managers
        '''
#         try:
#             self.devm.start()
#         except:
#             self.logger.error("Error while starting devm: %s" % sys.exc_info()[0])
#             raise    
        try:
            self.depm.start()
        except:
            self.logger.error("Error while starting depm: %s" % sys.exc_info()[0])
            raise
        self.login()
    
    def run(self):
        '''
        Main loop of the Deployment Service 
        '''
        self.poller = zmq.Poller()
        self.killed = False
        ok = True
        while True:     # Placeholder code
            time.sleep(1.0)
            # Poll controlled actors for messages
            #             sockets = dict(self.poller.poll(1000.0))
            #             if len(sockets) == 0:
            #                 pass
            #             else:
            #                 pass
            if self.killed:
                time.sleep(0.1)
                break
            # If background server 
            if self.bgsrv == None and self.conn == None: 
                if ok: 
                    self.logger.info("Connection to controller lost - retrying")
                ok = self.login(retry=False)
        self.terminate()

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
        '''
        assert type(msg) == tuple
        reply = None
        try: 
            cmd = msg[0]
            if cmd in ('launch','halt','setupApp','cleanupApp','cleanupApps'):
                self.depm.doCommand(msg)
            elif cmd in ('query','reclaim'):
                reply = self.depm.callCommand(msg)
            elif cmd == "kill":
                self.killed = True
            else:
                self.logger.error("unknown callback from control: %s" % str(msg))
                pass                # Should flag an error
        except BuildError as buildError:
            self.logger.error(str(buildError.args))
            raise
        except:
            info = sys.exc_info()
            self.logger.error("Error in callback '%s': %s %s" % (cmd, info[0], info[1]))
            traceback.print_exc()
            raise
        return reply

    def terminate(self):
        self.logger.info("terminating")
        self.resm.terminate()   # Terminate resource manager
        self.fm.terminate()     # Terminate fault manager
        self.depm.terminate()   # Terminate deployment manager
        self.depm.join() 
        # self.context.destroy()
        time.sleep(0.1)
        self.logger.info("terminated")
        os._exit(0)
        
        