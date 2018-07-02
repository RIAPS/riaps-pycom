"""
.. module:: logging
   :synopsis: Useful logging component implementations for RIAPS
"""
import logging
import time
import pickle
import threading
import signal
import rpyc
from rpyc.utils.server import ThreadedServer
from riaps.consts.defs import *

class NetLogConnection(threading.Thread):
    """"Thread which creates a connection to the Log Server

    This class acts asynchronously to establish a connection
    to therefore prevent blocking anywhere else due to a
    failed connection
    """

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
        """Checks whether or not there's a connection to the Log Server

        This will be false both before we have established a connection
        and after the connection has been lost/stopped.

        Returns:
            A bool indiciating the state of the connection to the Log
            Server
        """
        return self._connected.is_set()

    def stopped(self):
        """Checks whether or not the Thread has been stopped

        This will be true when the connection has been lost or if
        stop() has been called.

        Returns:
            A bool indicating whether the thread has been stopped
        """
        return self._stopped.is_set()

    def stop(self):
        """Terminate any connection or connection attempt

        This will both stop pending connection attempt or any
        current connection.
        """
        self._stopped.set()
        self._connected.clear()
        self._conn.close()        

    def run(self):
        """Creates a connection to the Log Server

        This method should not be called manually. This will be
        automically called in a separate Thread when start() has
        been called.
        """
        while not self.stopped() and not self.connected():
            try:
                self._conn = rpyc.connect_by_service(const.logServiceName, config=const.logServiceConfig)
                self._connected.set()
                self.logger.info("Connected to Log Server")
            except:
                self.logger.info("Failed to find the Log Server: Retrying in 5 seconds")
                time.sleep(5)

    def handleLog(self, record):
        """Pass a LogRecord over the RPyC connection

        If there's currently a connection, this will attempt to
        pass the LogRecord over the connection. If the connection
        has been lost, the LogRecord will be ignored.

        Args:
            record (LogRecord): A LogRecord to be passed to the Log Server

        Raises:
            Any exception that may have been caused by trying to pass the LogRecord
        """
        if self.lock.acquire():
            try:
                if not self.stopped() and self.connected():
                    data = pickle.dumps(record)
                    self._conn.root.handle(data)
            finally:
                self.lock.release()

class NetLogHandler(logging.Handler):
    """Logging handler which sends LogRecords to a Log Server via RPyC

    This handler can be attached to any logger and will attempt to send
    any LogRecords passed to that logger to a remote Log Server
    """

    def __init__(self):
        logging.Handler.__init__(self)

        # Spawn a new thread which connects to server
        self.conn = NetLogConnection()
        self.conn.daemon = True
        self.conn.start()
        self.connLock = threading.Lock()

    def emit(self, record):
        """Catch a LogRecord and pass it to the connection thread

        This method shouldn't be called manually. It is called automatically
        whenever the handler is given a LogRecord

        Args:
            record (LogRecord): The record to be handled
        """
        try:
            self.conn.handleLog(record)
        except:
            # Acquire lock to prevent simultaneous modification of self.conn
            if self.connLock.acquire():
                if not self.conn.stopped():
                    self.conn.stop()
                    self.conn.logger.info("Lost connection to Log Server")
                    self.conn = NetLogConnection() # Spawn a new thread which will reconnect
                    self.conn.daemon = True
                    self.conn.start()
                    self.connLock.release()

class LogService(rpyc.Service):
    """RPyC service for collecting remote logs

    This acts as a server which remote clients can connect to. The
    Clients can then call exposed_handle with any LogRecords which
    should be logged. Those LogRecords are then passed to the local
    Python logger.
    """
    ALIASES = [const.logServiceName] # Registry name for the service
    
    STOPPING = False

    def exposed_handle(self, data):
        """Exposed method for remote clients to pass log records to

        Args:
            data (bytes): Pickled LogRecord
        """
        if not LogService.STOPPING:
            record = pickle.loads(data)
            log = logging.getLogger(record.name)
            log.handle(record)

class LogServer(ThreadedServer):
    """ThreadedServer which executes the LogService"""

    def __init__(self):
        ThreadedServer.__init__(self, LogService, auto_register=True, protocol_config=const.logServiceConfig)

        # Create catch for kill signals
        def exit_gracefully(signal, frame):
            LogService.STOPPING = True
            self.close()
        signal.signal(signal.SIGINT, exit_gracefully)
        signal.signal(signal.SIGTERM, exit_gracefully)