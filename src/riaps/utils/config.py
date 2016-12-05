'''
Created on Nov 23, 2016

@author: riaps
'''

import configparser
import os
from os.path import join
import logging

class Config(object):
    '''
    Configuration database for RIAPS tools
    '''
    USER = 'riaps-user'
    
    def __init__(self):
        '''
        Constructor
        '''
        riaps_folder = os.getenv('RIAPSHOME', './')
        riaps_conf = join(riaps_folder,'etc/riaps.conf')
        
        c_parse = configparser.ConfigParser()
    
        try:
            files = c_parse.read(riaps_conf)
        except:
            logging.info(' Configuration file %s not found.' % (riaps_conf))
            return 
        
        if files == [] or not c_parse.has_section('RIAPS'):
            logging.info(' Configuration file %s not found or invalid file.' % (riaps_conf))
            return 
        
        try: 
            for item in c_parse.items('RIAPS'):
                arg = item[1]
                opt = item[0].upper()
            
                if hasattr(Config,opt):
                    setattr(Config,opt,arg)
        except:
            logging.info(' Error reading configuration file %s.' % (riaps_conf))
            return 

