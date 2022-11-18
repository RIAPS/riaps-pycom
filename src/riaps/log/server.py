import abc
import logging
import logging.handlers
import pickle
import queue
import signal
import socketserver
import struct

import riaps.log.handlers.factory as handler_factory


class BaseLogHandler(socketserver.StreamRequestHandler):

    def __init__(self, request, client_address, server):
        self.logger = logging.getLogger(__name__)
        super(BaseLogHandler, self).__init__(request, client_address, server)

    def setup(self) -> None:
        super(BaseLogHandler, self).setup()

    @abc.abstractmethod
    def handle(self) -> None:
        pass

    def handle_log_record(self, data):
        self.logger.debug(f"client address: {self.client_address}")
        node_name = self.client_address[0]

        msg = {"node_name": node_name,
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


class AppLogHandler(BaseLogHandler):

    def handle(self) -> None:
        while True:
            data_bytes = self.rfile.readline().strip()
            if not data_bytes:
                break
            data_string = data_bytes.decode("utf-8")
            data = f"{data_string}"
            self.handle_log_record(data)


class PlatformLogHandler(BaseLogHandler):

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

            logger = logging.getLogger(record.name)
            handlers = self.getHandlers(logger)
            handler = handlers[0]

            assert type(handler) is logging.StreamHandler, \
                "Handler type is not StreamHandler and may not support calling format"

            msg = handler.format(record)

            self.handle_log_record(data=msg)

    def getHandlers(self, logger):
        handlers = []
        while logger:
            if logger.handlers:
                rv = True
                handlers += logger.handlers
                break
            if not logger.propagate:
                break
            else:
                logger = logger.parent
        return handlers


class BaseLogServer(socketserver.ThreadingTCPServer):

    def __init__(self, server_address, RequestHandlerClass, server_log_handler, q):
        self.logname = "riaps.log"
        self.allow_reuse_address = True
        self.logger = logging.getLogger(__name__)
        self.RequestHandlerClass = RequestHandlerClass
        self.server_log_handler = server_log_handler
        self.q = q
        super(BaseLogServer, self).__init__(server_address,
                                            RequestHandlerClass)

    def service_actions(self):
        """
        service actions is a method of the socketserver class that may be overridden
        https://github.com/python/cpython/blob/3.11/Lib/socketserver.py#L255
        """
        while True:
            try:
                msg = self.q.get(block=False)
                self.server_log_handler.handle(msg)
            except queue.Empty as e:
                break

    def serve_until_stopped(self):
        self.logger.info(f'About to start Log server...')
        try:
            self.serve_forever()
        except KeyboardInterrupt:
            pass


class AppLogServer(BaseLogServer):

    def __init__(self, server_address, RequestHandlerClass, server_log_handler, q):
        super(AppLogServer, self).__init__(server_address, RequestHandlerClass, server_log_handler, q)


class PlatformLogServer(BaseLogServer):
    def __init__(self, server_address, RequestHandlerClass, server_log_handler, q):
        super(PlatformLogServer, self).__init__(server_address, RequestHandlerClass, server_log_handler, q)

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
    server_log_handler = handler_factory.get_handler(handler_type="tmux", session_name="platform")
    q = queue.Queue()
    theLogServer = PlatformLogServer(server_address=("172.21.20.70",
                                                     logging.handlers.DEFAULT_TCP_LOGGING_PORT),
                                     RequestHandlerClass=PlatformLogHandler,
                                     server_log_handler=server_log_handler,
                                     q=q)

    logger = logging.getLogger(__name__)
    server = multiprocessing.Process(target=theLogServer.serve_until_stopped)
    server.start()

    def term_handler(signal, frame):
        print("Call term_handler")
        server.terminate()
        server_log_handler.close()

    signal.signal(signal.SIGTERM, term_handler)
    signal.signal(signal.SIGINT, term_handler)



