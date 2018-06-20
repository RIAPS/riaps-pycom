'''
Server for collecting remote server logs from RIAPS components
Created on Jun 5, 2018

@author: jeholliday
'''
import logging
import logging.handlers
import signal
import time
import threading
import sys
import copy
import pickle
import rpyc
from rpyc.utils.server import ThreadedServer
from riaps.consts.defs import *

logFile = 'riaps-logserver.log'

class LogService(rpyc.Service):
    '''
    rpyc service for collecting remote logs
    '''
    ALIASES = [const.logServiceName] # Registry name for the service
    
    STOPPING = False

    def exposed_handle(self, data):
        '''
        Exposed method for remote clients to pass log records to
        '''
        if not LogService.STOPPING:
            record = pickle.loads(data)
            log = logging.getLogger(record.name)
            log.handle(record)

if __name__ == "__main__":
    # Setup root logger for displaying all messages
    rootLogger = logging.getLogger('')
    format = logging.Formatter("%(levelname)s:%(asctime)s:[%(process)d]:%(name)s:%(message)s")
    # Construct console handler for displaying logs in the console
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(format)
    rootLogger.addHandler(ch)
    # Construct file handler for saving logs to a file
    fh = logging.FileHandler(logFile)
    fh.setFormatter(format)
    rootLogger.addHandler(fh)

    # Setup local logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Create and configure rpyc service
    server = ThreadedServer(LogService, auto_register=True, protocol_config=const.logServiceConfig)

    # Create catch for kill signals
    def exit_gracefully(signal, frame):
        LogService.STOPPING = True
        server.close()
    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGTERM, exit_gracefully)

    logger.info("\nStarting RIAPS Log Server on port " + str(server.port) + " and saving files to " + logFile)

    server.start()