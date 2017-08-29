'''
Discovery server database interface
Created on Oct 19, 2016

@author: riaps
'''

import redis
from riaps.consts.defs import *
from riaps.run.exc import *
import re
import logging

class DiscoDbase(object):
    '''
    Discovery service database implemented using redis
    '''

    def __init__(self,context_,dbase):
        '''
        Construct the database object, set up singleton.
        '''
        self.logger = logging.getLogger(__name__)
        # Singleton DiscoDbase object
        global theDiscoBase
        theDiscoBase = self
        self.context = context_ 
        self.r = None               # The redis connection
        self.rHostPort = dbase      # Redis access string: 'host:port' (if any) 
    
    def start(self):
        '''
        Start the database: connect to the database process
        '''
        # Optional redis access string points to the database
        # Redis-specific syntax: database_host ":" database_port
        if self.rHostPort != None:
            pair = re.split(":",self.rHostPort)
            host = str(pair[0])
            port = int(pair[1])
        else:
            host = const.discoRedisHost
            port = const.discoRedisPort
        
        try:    
            self.logger.info("connecting to redis")
            self.r = redis.StrictRedis(host,port, db=0) # Connect
            self.notesPubSub = self.r.pubsub()          # Set up pubsub channel to receive notifications
        except redis.exceptions.ConnectionError:
            raise DatabaseError("db connection lost")
        except OSError:
            raise DatabaseError("OS error")    
        self.subKeys = [ ]                          # List of all keys subscribed to by this disco instance
        

    def updateSubs(self,newKey):
        '''
         Update the list of subscribed keys with the new key
        '''
        self.logger.info("updateSubs: %s" % newKey)
        if newKey in self.subKeys:
            return
        self.subKeys.append(newKey)
        fullKey = '__keyspace@0__:' + newKey        # Redis-specific: reference to a key in the 'keyspace'  
        self.notesPubSub.subscribe(fullKey)

    # 
    def fetchUpdates(self):
        '''
        Check and fetch the updated values of the subscribed keys if any
        '''
        if len(self.subKeys) == 0:
            return []
        keys = []
        try:
            while True:
                msg = self.notesPubSub.get_message(True)    # Use redis pubsub feature to check for a notification
                if not msg:
                    break
                else:
                    channel = msg['channel'].decode('utf-8')
                    data = msg['data'].decode('utf-8')
                    keySplit = re.split('__keyspace@0__:', channel)
                    keys.append(keySplit[1])
            res = [] 
            for key in keys:
                values = self.r.smembers(key)
                clientsKey = key + "_clients"
                clientsToNotify = self.r.smembers(clientsKey)
                for value in values:
                    valueString = value.decode('utf-8')
                    res.append((key, valueString, clientsToNotify))
            return res
        except redis.exceptions.ConnectionError:
            raise DatabaseError("db connection lost")
        except OSError:
            raise DatabaseError("OS error")
                      
    def insert(self,key,value):
        '''
        Insert value under key and return list of clients of value (if any). 
        A key may have multiple values associated with it, hence the new value 
        is added to the set of values that belong to the key
        '''
        self.logger.info("insert %s -> %s" % (repr(key),repr(value)))
        try:
            clientsToNotify = []
            self.r.sadd(key,value)
#            self.updateSubs(key)
            clientsKey = key + "_clients"
            clientsToNotify = self.r.smembers(clientsKey)
            return clientsToNotify
        except redis.exceptions.ConnectionError:
            raise DatabaseError("db connection lost")
        except OSError:
            raise DatabaseError("OS error")

    def fetch(self,key,client):
        '''
        Fetch value(s) under key. Add client to list of clients interested in the value
        '''
        self.logger.info("fetch %s for %s" % (repr(key),repr(client)))
        self.updateSubs(key)
        try:
            if self.r.exists(key):          
                values = self.r.smembers(key)
            else:
                values = []
            clientsKey = key + "_clients"
            self.r.sadd(clientsKey,client)
            return values
        except redis.exceptions.ConnectionError:
            raise DatabaseError("db connection lost")
        except OSError:
            raise DatabaseError("OS error")
        
    def remove(self,key,value):
        '''
        Remove value from values under key.
        '''
        self.logger.info("remove %s from %s" % (repr(value),repr(key)))
        try:
            self.r.srem(key,value)
            return self.r.smembers(key)
        except redis.exceptions.ConnectionError:
            raise DatabaseError("db connection lost")
        except OSError:
            raise DatabaseError("OS error")
        
    def delete(self,key):
        '''
        Completely delete key and list of clients for that key.
        '''
        self.logger.info("delete %s" % (repr(key)))
        try:
            self.rLocal.delete(key)
            clientsKey = key + "_client"
            self.r.delete(clientsKey)
        except redis.exceptions.ConnectionError:
            raise DatabaseError("db connection lost")
        except OSError:
            raise DatabaseError("OS error")

