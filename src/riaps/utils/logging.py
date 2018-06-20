'''
Useful logging component implementations
Created on Jun 19, 2018

@author: jeholliday
'''
import logging
import time
import pickle
import threading
import signal
import rpyc
from riaps.consts.defs import *

class NetLogConnection(threading.Thread):
    '''
    Thread which creates a connection to the Log Server
    '''
    def __init__(self):
        threading.Thread.__init__(self)

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.propagate=True
        self.lock = threading.Lock()

        self._connected = threading.Event()
        self._stopped = threading.Event()
        self._conn = None

    def connected(self):
        return self._connected.is_set()

    def stopped(self):
        return self._stopped.is_set()

    def _stop(self):
        self._stopped.set()
        self._connected.clear()
        self._conn.close()  

    def stop(self):
        if self.lock.acquire():
            self._stop()
            self.lock.release()           

    def run(self):
        '''
        Creates a connection to the Log Server
        '''
        while not self.stopped() and not self.connected():
            try:
                self._conn = rpyc.connect_by_service(const.logServiceName, config=const.logServiceConfig)
                self._connected.set()
                self.logger.info("Connected to Log Server")
            except:
                self.logger.info("Failed to find the Log Server: Retrying in 5 seconds")
                time.sleep(5)

    def handleLog(self, record):
        '''
        Pass a LogRecord over the rpyc connection
        Will throw an exception if sending the message fails
        '''
        if self.lock.acquire():
            if not self.stopped() and self.connected():
                try:
                    data = pickle.dumps(record)
                    self._conn.root.handle(data)
                except:
                    self._stop()
                    raise
            self.lock.release()

class NetLogHandler(logging.Handler):
    '''
    Logging handler which sends LogRecords to a Log Server via rpyc
    '''
    def __init__(self):
        logging.Handler.__init__(self)

        self.lock = threading.Lock()

        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

        # Spawn a new thread which connects to server
        self.conn = NetLogConnection()
        self.conn.start()

    def exit_gracefully(self, signal, frame):
        '''
        Stop any spawned threads
        '''
        self.conn.stop()

    def emit(self, record):
        '''
        Catch a LogRecord and pass it to the connection thread
        '''
         # Acquire lock to prevent simultaneous modification of self.conn
        if self.lock.acquire():
            try:
                self.conn.handleLog(record)
            except:
                self.conn.logger.info("Lost connection to Log Server")
                self.conn = NetLogConnection() # Spawn a new thread which will reconnect
                self.conn.start()
            self.lock.release()

