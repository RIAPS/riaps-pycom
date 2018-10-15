'''
Controller node service implementation
Created on Nov 6, 2016

@author: riaps
'''
import rpyc
import time
from rpyc import async
from rpyc.utils.server import ThreadedServer
rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True

from riaps.consts.defs import *
import threading
import logging

theController = None
guiClient = None

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
        self.log("+ %s" %(self.name,))

    def exposed_logout(self):
        '''
        Logs out a node from service. Called when connection to the deployment service is lost. 
        '''
        if self.stale:
            return
        self.stale = True
        self.callback = None
        if self.name != "*gui*":
            self.log("- %s " % (self.name,))
                
    def log(self, text):
        '''
        Adds a log message to the GUI
        '''
        global guiClient
        if guiClient != None:
            guiClient.callback(text)
    
    def setupApp(self,appName,appNameJSON):
        '''
        Sets up an app on the client: it calls the Deployment service's callback running on the
        node. 
        ''' 
        if self.callback != None:
            res = self.callback(('setupApp',appName,appNameJSON))
            return res
            
    def cleanupApp(self,appName):
        '''
        Removes an app from the client: it calls the Deployment service's callback running on the
        node. 
        ''' 
        if self.callback != None:
            res = self.callback(('cleanupApp',appName))
            return res
    
    def cleanupApps(self):
        '''
        Removes all apps from the client: it calls the Deployment service's callback running on the
        node. 
        ''' 
        if self.callback != None:
            res = self.callback(('cleanupApps',))
            return res
            
    def launch(self,appName,appNameJSON,actorName,actuals):
        '''
        Launches an app actor on the client: it calls the Deployment service's callback running on the
        node. 
        ''' 
        if self.callback != None:
            res = self.callback(('launch',appName,appNameJSON,actorName,actuals))
            return res
    
    def halt(self,appName,actorName):
        '''
        Halts an app actor on the client: it calls the Deployment service's callback running on the
        node. 
        ''' 
        if self.callback != None:
            res = self.callback(('halt',appName,actorName))
            return res
        
    def clean(self):
        '''
        Clean the riaps_deplo app folder
        '''
        if self.callback != None:
            res = self.callback(('clean',))
            return res
        
    def kill(self):
        '''
        Kill the riaps_deplo 
        '''
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
        global theController,ctrlLock,guiClient
        if clientName == "*gui*":       # NOTE: the GUI is client of the service
            assert self.client == None and guiClient == None
            guiClient = ServiceClient(clientName,async(callback),self,None)
            return ()
        else:                           # RIAPS node client
            assert (appFolder != None)
            if (self.client and not self.client.stale) or theController.isClient(clientName):
                # raise ValueError("already logged in")
                oldClient = theController.getClient(clientName)
                oldClient.exposed_logout()
                theController.delClient(clientName)
            self.client = ServiceClient(clientName, async(callback),self,appFolder)   # Register client's callback
            theController.addClient(clientName,self.client)
            dbaseNode = theController.nodeName      # The (redis) database is running on this same node
            dbasePort = const.discoRedisPort        
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
        self.server = ThreadedServer(ControllerService,hostname=host, port=self.port,
                                     auto_register=True,
                                     protocol_config = {"allow_public_attrs" : True})
        self.server.start()
        time.sleep(0.010)
        
    def stop(self):
        '''
        Terminates the service. Called when the program exits. 
        '''
        ControllerService.STOPPING = True
        self.server.close()


