'''
Discovery server database interface
Created on Oct 19, 2016

@author: riaps
'''

from riaps.consts.defs import *
from riaps.run.exc import *
import typing
import re
import logging


class DiscoDbase(object):
    '''
    Discovery service database base class
    '''
        
    def __init__(self,context_,dbaseLoc):
        '''
        Construct the database object, set up singleton.
        '''
        self.logger = logging.getLogger(__name__)
        # Singleton DiscoDbase object
        self.context = context_ 
        self.dbaseLoc = dbaseLoc

    def start(self):
        '''
        Start the database: connect to the database process
        '''
        pass

    # 
    def fetchUpdates(self) -> [str]:
        '''
        Check and fetch the updated values of the subscribed keys if any
        '''
        return []
    
                      
    def insert(self,key:str,value:str) -> [str]:
        '''
        Insert value under key and return list of clients of value (if any). 
        A key may have multiple values associated with it, hence the new value 
        is added to the set of values that belong to the key
        '''
        clientsToNotify = []
        return clientsToNotify
    
    def fetch(self,key:str,client:str) -> [str]:
        '''
        Fetch value(s) under key. Add client to list of clients interested in the value
        '''
        values = []
        return values
        
    def remove(self,key:str,value:str) -> [str]:
        '''
        Remove value from value under key.
        '''
        pass
        
    def detach(self, key:str, target:str):
        '''
        Detach client (for updates) from keys
        '''
        pass

    def terminate(self):
        pass
    
    
