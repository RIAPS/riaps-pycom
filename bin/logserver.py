'''
Created on Jun 5, 2018

@author: jeholliday
'''
import cPickle
import logging
import logging.handlers
import SocketServer
import struct
import signal
import os

logFile = 'riaps-logserver.log'
tcpserver = None

class LogRecordStreamHandler(SocketServer.StreamRequestHandler):
    """Handler for logging remote logs"""

    def handle(self):
        """
        Handle multiple requests - each expected to be a 4-byte length,
        followed by the LogRecord in pickle format.
        """
        while 1:
            chunk = self.connection.recv(4)
            if len(chunk) < 4:
                break
            slen = struct.unpack(">L", chunk)[0]
            chunk = self.connection.recv(slen)
            while len(chunk) < slen:
                chunk = chunk + self.connection.recv(slen - len(chunk))
            obj = self.unPickle(chunk)
            record = logging.makeLogRecord(obj)
            self.handleLogRecord(record)

    def unPickle(self, data):
        return cPickle.loads(data)

    def handleLogRecord(self, record):
        logger = logging.getLogger(record.name)
        logger.handle(record)

class LogRecordSocketReceiver(SocketServer.ThreadingTCPServer):
    allow_reuse_address = 1

    def __init__(self, host, port, handler=LogRecordStreamHandler):
        self.handler = handler
        self.abort = 0
        self.timeout = 1
        SocketServer.ThreadingTCPServer.__init__(self, (host, port), self.handler)

    def serve_until_stopped(self):
        import select
        abort = 0
        while not abort:
            rd, wr, ex = select.select([self.socket.fileno()],[], [],self.timeout)
            if rd:
                self.handle_request()
            abort = self.abort

    def halt(self):
        self.abort = 1

def findLocalIP():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

if __name__ == "__main__":
    host = findLocalIP()
    port = logging.handlers.DEFAULT_TCP_LOGGING_PORT

    # fetch root logger
    logger = logging.getLogger('')
    # create file handler
    fh = logging.FileHandler(logFile)
    fh.setLevel(logging.INFO)
    # create console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    tcpserver = LogRecordSocketReceiver(host, port)

    # Create catch for CTRL+C
    def signal_handler(signal, frame):
        print('SIGNAL: Exitting gracefully!')
        tcpserver.halt()
        os._exit(0)
    signal.signal(signal.SIGINT, signal_handler)

    print("\nStarting RIAPS Log Server")
    print("-------------------------")
    print("Listening on: " + host + ":" + str(port))
    print("Saving logs to: " + logFile)
    print("-------------------------\n")
    tcpserver.serve_until_stopped()