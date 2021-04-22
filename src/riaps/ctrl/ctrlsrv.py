'''
Controller node service implementation
Created on Nov 6, 2016

@author: riaps
'''
import os
import time
import threading
import logging
import zmq
import rpyc
from rpyc import async_
from rpyc.utils.server import ThreadedServer
from rpyc.utils.authenticators import SSLAuthenticator
from riaps.utils.config import Config
import ssl
import traceback

rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True

from riaps.consts.defs import *

theController = None
# guiClient = None

class ServiceClient(object):
    '''
    Service Client object represents a RIAPS node that runs a Deployment Service
    '''
    def __init__(self, name, callback,parent,appFolder):
        self.name = name
        self.stale = False
        self.callback = callback
        self.parent = parent
        self.appFolder = appFolder
        self.socket = theController.context.socket(zmq.PUSH)
        self.socket.connect(theController.endpoint)
        self.log("+ %s" %(self.name,))

    def exposed_logout(self):
        '''
        Logs out a node from service. Called when connection to the deployment service is lost. 
        '''
        if self.stale:
            return
        self.stale = True
        self.callback = None
        self.log("- %s " % (self.name,))    
        self.socket.close()
                
    def log(self, text):
        '''
        Adds a log message to the GUI
        '''
        self.socket.send_pyobj(text)
#         global guiClient
#         if guiClient != None:
#             guiClient.callback(text)
    
    def setupApp(self,appName,appNameJSON):
        '''
        Sets up an app on the client: it calls the Deployment service's callback running on the
        node. 
        ''' 
        res = None
        if self.callback != None:
            res = self.callback(('setupApp',appName,appNameJSON))
        return res
            
    def cleanupApp(self,appName):
        '''
        Removes an app from the client: it calls the Deployment service's callback running on the
        node. 
        ''' 
        res = None
        if self.callback != None:
            res = self.callback(('cleanupApp',appName))
        return res
    
    def cleanupApps(self):
        '''
        Removes all apps from the client: it calls the Deployment service's callback running on the
        node. 
        ''' 
        res = None 
        if self.callback != None:
            res = self.callback(('cleanupApps',))
        return res
            
    def launch(self,appName,appNameJSON,actorName,actuals):
        '''
        Launches an app actor on the client: it calls the Deployment service's callback running on the
        node. 
        ''' 
        res = None
        if self.callback != None:
            res = self.callback(('launch',appName,appNameJSON,actorName,actuals))
        return res
    
    def install(self,appName):
        '''
        Installs the downloaded package on the client.
        '''
        res = None
        if self.callback != None:
            res = self.callback(('install',appName))
        return res
    
    def halt(self,appName,actorName):
        '''
        Halts an app actor on the client: it calls the Deployment service's callback running on the
        node. 
        ''' 
        res = None 
        if self.callback != None:
            res = self.callback(('halt',appName,actorName))
        return res
        
    def clean(self):
        '''
        Clean the riaps_deplo app folder
        '''
        res = None 
        if self.callback != None:
            res = self.callback(('clean',))
        return res
        
    def kill(self):
        '''
        Kill the riaps_deplo 
        '''
        res = None
        if self.callback != None:
            res = self.callback(('kill',))
        return res
    
    def query(self):
        '''
        Query client for running apps
        '''
        res = None
        if self.callback != None:
            res = self.callback(('query',))
        return res
    
    def reclaim(self,appName):
        '''
        Reclaim app files 
        '''
        res = None
        if self.callback != None:
            res = self.callback(('reclaim',appName))
        return res
            
class ControllerService(rpyc.Service):
    '''
    Controller Service implementation (rpyc service)
    '''
    
    ALIASES = ["RIAPSCONTROL"]              # Registry name for the service
    
    STOPPING = None
    
    def on_connect(self,_conn = None):
        '''
        Called when a client connects. Subsequently the client must login. 
        '''
        if ControllerService.STOPPING: return
        self.client = None
        self.logger = logging.getLogger('riapsCtrl')
        self.socket = None

    def on_disconnect(self,_conn = None):
        '''
        Called when a client disconnects
        '''
        if ControllerService.STOPPING: return
        if self.client:
            self.client.exposed_logout()
            theController.delClient(self.client.name)

    def exposed_login(self,clientName,callback,appFolder=None):
        '''
        Log into the service. 
        '''
        if ControllerService.STOPPING: return
        global theController,ctrlLock # ,guiClient
        #         if clientName == "*gui*":       # NOTE: the GUI is client of the service
        #             assert self.client == None and guiClient == None
        #             guiClient = ServiceClient(clientName,async_(callback),self,None)
        #             return ()
        #         else:                           # RIAPS node client
        assert (appFolder != None)
        if (self.client and not self.client.stale) or theController.isClient(clientName):
            # raise ValueError("already logged in")
            oldClient = theController.getClient(clientName)
            oldClient.exposed_logout()
            theController.delClient(clientName)
        self.client = ServiceClient(clientName, async_(callback),self,appFolder)   # Register client's callback
        theController.addClient(clientName,self.client)
        dbaseNode = theController.nodeName      # The (redis) database is running on this same node
        if theController.discoType == 'redis':
            dbasePort = const.discoRedisPort
        elif theController.discoType == 'opendht':
            dbasePort = theController.dhtPort
        else:
            dbasePort = -1        
        return ('dbase',str(dbaseNode),str(dbasePort))  # Reply to the client

class ServiceThread(threading.Thread):
    '''
    Control server main execution thread.
    Note: ThreadedServer launches a new thread for every connection.  
    '''
    def __init__(self,port):
        threading.Thread.__init__(self)
        self.port = port
    
    def setController(self,ctrl):
        '''
        Set the controller object for the service thread. 
        '''
        global theController
        theController = ctrl
        
    def run(self):
        '''
        Runs the rpyc ThreadedServer with the service implementation.
        NOTE: it expects a rpyc service registry running 
        '''
        global theController
        host = theController.hostAddress
        self.auth = SSLAuthenticator(theController.keyFile, theController.certFile,
                                     cert_reqs=ssl.CERT_REQUIRED, ca_certs=theController.certFile,
                                     ) if Config.SECURITY else None
        try:
            self.server = ThreadedServer(ControllerService,hostname=host, port=self.port,
                                         authenticator = self.auth,
                                         auto_register=True,
                                         protocol_config = {"allow_public_attrs" : True})
        except:
            print ("Failed to create server")
            traceback.print_exc()
            os._exit(0)
        self.server.start()
        time.sleep(0.010)
        
    def stop(self):
        '''
        Terminates the service. Called when the program exits. 
        '''
        ControllerService.STOPPING = True
        self.server.close()


