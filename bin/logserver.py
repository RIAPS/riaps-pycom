"""
.. module:: logserver
   :synopsis: Server for collecting logs from remote RIAPS components
"""
import logging
import logging.handlers
import signal
import time
import threading
import sys
import copy
import pickle
import rpyc
from riaps.utils.logging import LogServer
from riaps.consts.defs import *

logFile = 'riaps-logserver.log'

def main():
    """Start a Log Server

    This creates an instance of the LogService to accept remote logs.
    This then configures the local root logger to automatically output
    and LogRecords to both the console and a file.
    """
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

    # Create instance of the LogServer
    server = LogServer()

    logger.info("\nStarting RIAPS Log Server on port " + str(server.port) + " and saving files to " + logFile)

    server.start()

if __name__ == "__main__":
    main()