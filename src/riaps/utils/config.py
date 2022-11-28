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
    TARGET_USER = 'riaps'
    SEND_TIMEOUT = -1
    RECV_TIMEOUT = -1
    SEND_HWM = 100            # Send water mark
    RECV_HWM = 100            # Receive high water mark
    NIC_NAME = None
    NIC_RATE = '118kbps'    # 90% of 1 gigabits per sec
    NIC_CEIL = '131kbps'    # 1 gigabits per sec
    DISCO_TYPE = 'redis'    # or 'opendht'
    CTRL_DEBUG_SERVER = ''
    DEPLO_DEBUG_SERVER = ''
    DISCO_DEBUG_SERVER = ''
    ACTOR_DEBUG_SERVER = ''
    DEVICE_DEBUG_SERVER = ''
    APP_LOGS = ''
    CTRL_HEARTBEAT = True
    NODE_HEARTBEAT = True
    NETMON = True
    SECURITY = True
    
    def __init__(self):
        '''
        Construct the configuration object that configures the logger and various system parameters. 
        The logger and system configuration are set according to the content of the files $RIAPSHOME/etc/riaps-log.conf
        and $RIAPSHOME/etc/riaps.conf 
        '''
        riaps_folder = os.getenv('RIAPSHOME')
        
        if riaps_folder == None:
            print("RIAPS Configuration - RIAPSHOME is not set, using ./")
            riaps_folder = './'
        
        riaps_logconf = join(riaps_folder, 'etc/riaps-log.conf')
        
        try:
            logging.config.fileConfig(riaps_logconf)
        except Exception as e:
            logging.warning(' Log configuration file %s has a problem: %s.' % (riaps_logconf, str(e)))
            pass
        
        logger = logging.getLogger(__name__)
        
        riaps_conf = join(riaps_folder, 'etc/riaps.conf')
        c_parse = configparser.ConfigParser()
    
        try:
            files = c_parse.read(riaps_conf)
        except Exception as e:
            logger.warning(' System configuration file %s has a problem: %s.' % (riaps_conf, str(e)))
            return 
        
        riaps_section = 'RIAPS'
        if files == [] or not c_parse.has_section(riaps_section):
            logger.warning(' System configuration file %s not found or invalid file.' % (riaps_conf))
            return 
        
        try: 
            for item in c_parse.items(riaps_section):
                key, arg = item
                opt = key.upper()
            
                if hasattr(Config, opt):
                    optType = type(getattr(Config, opt))
                    optValue = getattr(Config, opt)
                    try:
                        if optType == str:
                            optValue = str(arg)
                        elif optType == int:
                            optValue = int(arg)
                        elif optType == bool:
                            try:
                                optValue = c_parse.getboolean(riaps_section, key)
                            except:
                                print (1)
                                pass
                        elif optType == float:
                            optValue = float(arg)
                        else:
                            optValue = arg
                        setattr(Config, opt, optValue)
                    except:
                        print(2)
                        logger.warning('Formal and actual type of configuration argument %s differ %s - ignored'
                                       % (str(opt), str(optType)))
        except:
            logger.warning(' Error reading configuration file %s.' % (riaps_conf))
            return 

