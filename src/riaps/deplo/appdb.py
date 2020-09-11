'''
Application database
Created on Apr 2, 2018

@author: riaps
'''

import os
from os.path import join
import lmdb
import logging

try:
    import cPickle
    pickle = cPickle
except:
    cPickle = None
    import pickle

from riaps.consts.defs import *
from riaps.utils.config import Config
from riaps.run.exc import BuildError

#from riaps.deplo.depm import DeploActorCommand

# obj <- pickle.loads(bytes)
# bytes <- pickle.dumps(obj)

class AppDbase(object):
    '''
    Application database. The database is a collection of key -> value pairs, where values are
    pickled Python objects (i.e. bytearrays). 
    Structure: 
    RIAPSAPPS -> [ appNames* ]
    appName -> [ actorRecords* ]
    '''

    RIAPSAPPS = 'RIAPSAPPS'
    RIAPSDISCO = 'RIAPSDISCO'
    RIAPSDISCOCMD = 'RIAPSDISCOCMD'
    
    def __init__(self):
        '''
        Constructor
        '''
        # Open database
        self.logger = logging.getLogger(__name__)
        self.create = False
        self.dbase = None
        appFolder = os.getenv('RIAPSAPPS', './')
        dbPath = join(appFolder,const.appDb) 
        mapSize = const.appDbSize * 1024 * 1024
        if os.path.exists(dbPath) and not os.access(dbPath,os.W_OK):
            raise BuildError("app database is not writeable")
        while True:
            try:
                self.dbase = lmdb.open(dbPath,
                                       map_size = mapSize,
                                       metasync=True, 
                                       sync=True, 
                                       map_async=False,
                                       mode=0o700, 
                                       readahead=True, 
                                       create = self.create,
                                       writemap=False)
                self.logger.info('appDb opened (create = %s)' % str(self.create))
                break
            except lmdb.Error:
                self.create = True
            except:
                raise 
            
    def closeDbase(self):
        apps = self.getApps()
        for appName in apps:
            self.delKey(appName)
        self.delKey(self.RIAPSDISCO)
        self.delKey(self.RIAPSAPPS)
        self.dbase.close()
        self.logger.info('appDb closed')
    
    def getKeyValue(self,key,default = None):
        assert self.dbase != None
        value = default
        if type(key) == str: key = key.encode('utf-8')
        with self.dbase.begin() as txn:
            valuePickle = txn.get(key)
            if valuePickle != None:
                value = pickle.loads(valuePickle)
        return value
    
    def putKeyValue(self,key,value):
        assert self.dbase != None
        res = False
        if type(key) == str: key = key.encode('utf-8')
        with self.dbase.begin(write=True) as txn:
            valuePickle = pickle.dumps(value)
            res = txn.put(key,valuePickle)
        return res
    
    def replaceKeyValue(self,key,value):
        assert self.dbase != None
        res = False
        if type(key) == str: key = key.encode('utf-8')
        with self.dbase.begin(write=True) as txn:
            valuePickle = pickle.dumps(value)
            res = txn.replace(key,valuePickle)
        return res
    
    def delKey(self,key):
        assert self.dbase != None
        res = False
        if type(key) == str: key = key.encode('utf-8')
        with self.dbase.begin(write=True) as txn:
            res = txn.delete(key)
        return res
    
    def getDisco(self):
        return self.getKeyValue(self.RIAPSDISCO)
    
    def setDisco(self,disco):
        return self.putKeyValue(self.RIAPSDISCO,disco)
            
    def getDiscoCommand(self):
        return self.getKeyValue(self.RIAPSDISCOCMD)
    
    def setDiscoCommand(self,discoCmd):
        return self.putKeyValue(self.RIAPSDISCOCMD,discoCmd)
    
    def delDiscoCommand(self):
        return self.delKey(self.RIAPSDISCOCMD)
            
    def getApps(self):
        if self.create:
            return []
        appList = self.getKeyValue(self.RIAPSAPPS,[])
        assert type(appList) == list
        return appList
    
    def addApp(self,appName):
        '''
        Add a new app to the database
        '''
        ok, repl = False, False
        try:
            appList = self.getKeyValue(self.RIAPSAPPS)
            if appList == None: 
                appList = []
            else: 
                repl = True
            if appName not in appList:
                appList += [appName]
            if repl:
                self.replaceKeyValue(self.RIAPSAPPS, appList)
            else:
                self.putKeyValue(self.RIAPSAPPS, appList)
            ok = True
        except:
            pass
        return ok
    
    def delApp(self,appName):
        ok = False
        try:
            appList = self.getKeyValue(self.RIAPSAPPS,[])
            if appName in appList:
                self.delKey(appName)
                appList.remove(appName)
                self.replaceKeyValue(self.RIAPSAPPS,appList)
                ok = True
        except:
            pass
        return ok
        

    def addAppActor(self,appName,actorRecord):
        ok = False
        try:
            actList = self.getKeyValue(appName,[])
            actList += [actorRecord]
            self.replaceKeyValue(appName, actList)
            ok = True
        except:
            pass
        return ok
        
    def getAppActors(self,appName):
        actList = False
        try:
            actList = self.getKeyValue(appName,[])
        except:
            pass
        return actList

    def getAppActor(self,appName,actorName):
        res = None
        try:
            actList = self.getKeyValue(appName,[])
            actList = [ a for a in actList if a.actor == actorName ]
            res = actList[0]
        except:
            pass
        return res
    
    def delAppActor(self,appName,actorName):
        ok = False
        try:
            actList = self.getKeyValue(appName,[])
            actList = [ a for a in actList if a.actor != actorName ]
            self.replaceKeyValue(appName, actList)
            ok = True
        except:
            pass
        return ok
    
