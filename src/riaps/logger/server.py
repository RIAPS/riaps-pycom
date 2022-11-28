#
# log server 
# 

import abc
import logging
import logging.handlers
import pickle
import queue
import signal
import socket
import socketserver
import struct
import threading
import time
import os
from functools import partial 

import riaps.logger.drivers.factory as driver_factory

class BaseLogRequestHandler(socketserver.StreamRequestHandler):

    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        
    def setup(self) -> None:
        super().setup()

    @abc.abstractmethod
    def handle(self) -> None:
        pass

    def handle_log_record(self, data):
        self.server.logger.debug(f"request: client: {self.client_address}")
        client = self.client_address[0]

        msg = {"client": client,
               "data": data}

        self.server.q.put(msg)
        # ^^^^^^^^^^^^^^^^^^^^
        # self.server is passed in by the parent of the handler.
        # https://github.com/python/cpython/blob/3.11/Lib/socketserver.py#L752
        # and is set in the BaseRequestHandler of the socketserver class.
        #
        # q is set in the server class
        # a shared q is used to avoid creating multiple tmux panes which could happen if
        # panes were created in this handler
        # This handle is called in a new thread though, so that is why the queue is needed... right?
        # -------------------------------------


class AppLogRequestHandler(BaseLogRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)

    def handle(self) -> None:
        while True:
            data_bytes = self.rfile.readline().strip()
            if not data_bytes:
                break
            data_string = data_bytes.decode("utf-8")
            data = f"{data_string}"
            self.handle_log_record(data)

class PlatformLogRequestHandler(BaseLogRequestHandler):
    
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)

    def handle(self) -> None:
        while True:
            chunk = self.connection.recv(4)
            if len(chunk) < 4:
                break
            slen = struct.unpack('>L', chunk)[0]
            chunk = self.connection.recv(slen)
            while len(chunk) < slen:
                chunk += self.connection.recv(slen - len(chunk))
            obj = pickle.loads(chunk)

            record = logging.makeLogRecord(obj)
            
            handler = self.server.getLogHandler() 
            msg = handler.format(record)
            self.handle_log_record(data=msg)

# thread that waits for items on the queue and forwards them to the driver
# thread stops when receive a special 'stop' message '#'
def handler_thread(owner):
    while True:
        try:
            msg = owner.q.get()
            if msg == '#': 
                break
            else:
                owner.driver.handle(msg)
        except:
            break

class BaseLogServer(socketserver.ThreadingTCPServer):
    
    def __init__(self, server_address, RequestHandlerClass, driver, q):
        super(BaseLogServer, self).__init__(server_address, RequestHandlerClass)
        self.allow_reuse_address = True

        self.RequestHandlerClass = RequestHandlerClass
        self.driver = driver
        self.q = q
    
    @staticmethod
    # stop the server main loop
    def stopper(me):
        me.shutdown()
        
    @staticmethod
    # termination signal handler, launches the stopper on another (timer) thread
    def term_handler(_signal,_frame,me):
        s = threading.Timer(0.1,BaseLogServer.stopper,args=(me,))
        s.start()
    
    def serve_until_stopped(self):
        self.logger = logging.getLogger("riaps.logger")
        self.logger.propagate = False
        self.logger.info(f'server: starting at %s' % str(self.server_address))
        signal.signal(signal.SIGTERM, partial(BaseLogServer.term_handler, me=self))
        signal.signal(signal.SIGINT, partial(BaseLogServer.term_handler, me=self))
        self.socket.setsockopt(socket.SOL_SOCKET,socket.SO_LINGER,struct.pack('ii', 1, 0))
        _thread = threading.Thread(target=handler_thread, args=(self,),daemon=False)
        _thread.start()
        try:
            self.serve_forever()
        except KeyboardInterrupt:
            self.logger.info("server: interrupted")
        self.logger.info('server: shutting down')
        self.q.put('#')
        _thread.join()
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        os._exit(0)

class AppLogServer(BaseLogServer):
    def __init__(self, server_address, driver, q):
        super().__init__(server_address, AppLogRequestHandler, driver, q)

class PlatformLogServer(BaseLogServer):
    def __init__(self, server_address, driver, q):
        super().__init__(server_address, PlatformLogRequestHandler, driver, q)
        self.findHandler()
    
    def findHandler(self):
        # The handler for the 'riaps.rlog' is used to 
        # format messages before sending them to the driver
        logger = logging.getLogger("riaps.rlog")
        handlers = []
        while logger:
            if logger.handlers:
                handlers += logger.handlers
                break
            if not logger.propagate:
                break
            else:
                logger = logger.parent
        self.handler = None
        for h in handlers:
            if type(h) is logging.StreamHandler:
                self.handler = h
                break
        if self.handler is None:                # Default to a StreamHandler
            self.handler = logging.StreamHandler()
            
    def getLogHandler(self):
        '''
         Return the log handler (to be used in formatting the record)
        '''
        return self.handler    

    # -----------------------------------------------------------------------------------
    # Commented code below is left in case using serve_forever() ends up having an as yet
    # undetected problem. It came from the original example.
    # \/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/
    # def serve_until_stopped(self):
    #     self.logger.info(f'Starting Platform Log server...')
    #     self.logger.info(threading.get_ident())
    #     import select
    #     abort = 0
    #     while not abort:
    #         rd, wr, ex = select.select([self.socket.fileno()],
    #                                    [], [],
    #                                    self.timeout)
    #         if rd:
    #             self.handle_request()
    #         abort = self.abort
    #     self.logger.info(f"Terminate Platform Log server")


if __name__ == '__main__':
    import multiprocessing
    driver = driver_factory.get_driver(handler_type="console", session_name="platform")
    q = queue.Queue()
    theLogServer = PlatformLogServer(server_address=("riaps.local",logging.handlers.DEFAULT_TCP_LOGGING_PORT),
                                     driver=driver,
                                     q=q)

    logger = logging.getLogger("riaps.logger")
    logger.propagate = False
    server = multiprocessing.Process(target=theLogServer.serve_until_stopped)
    server.start()

    def term_handler(signal, frame):
        print("Call term_handler")
        server.terminate()
        driver.close()

    signal.signal(signal.SIGTERM, term_handler)
    signal.signal(signal.SIGINT, term_handler)



