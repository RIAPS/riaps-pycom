'''
Created on Nov 23, 2016

@author: riaps
'''

import configparser
import os
from os.path import join
import logging
import logging.config

class Config(object):
    '''
    Configuration database for RIAPS tools
    Including logging configuration
    '''
    TARGET_USER = 'riaps-user'
    SEND_TIMEOUT = -1
    
    def __init__(self):
        '''
        Constructor
        '''
        riaps_folder = os.getenv('RIAPSHOME', './')
        
        riaps_logconf = join(riaps_folder,'etc/riaps-log.conf')
        
        try:
            logging.config.fileConfig(riaps_logconf)
        except Exception as e:
            logging.warning(' Log configuration file %s not found.' % (riaps_logconf))
            pass

        
        logger = logging.getLogger(__name__)
        
        riaps_conf = join(riaps_folder,'etc/riaps.conf')
        c_parse = configparser.ConfigParser()
    
        try:
            files = c_parse.read(riaps_conf)
        except:
            logger.warning(' Configuration file %s not found.' % (riaps_conf))
            return 
        
        if files == [] or not c_parse.has_section('RIAPS'):
            logger.warning(' Configuration file %s not found or invalid file.' % (riaps_conf))
            return 
        
        try: 
            for item in c_parse.items('RIAPS'):
                arg = item[1]
                opt = item[0].upper()
            
                if hasattr(Config,opt):
                    optType = type(getattr(Config,opt))
                    try:
                        if optType == str:
                            optValue = str(arg)
                        elif optType == int:
                            optValue = int(arg)
                        elif optType == bool:
                            optValue = bool(arg)
                        elif optType == float:
                            optValue = float(arg)
                        else:
                            optValue = opt
                        setattr(Config,opt,optValue)
                    except:
                        logger.warning('Formal and actual type of configuration argument %s differ %s - ignored'
                                       % (str(opt), str(optType)))
        except:
            logger.warning(' Error reading configuration file %s.' % (riaps_conf))
            return 

