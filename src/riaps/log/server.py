import pickle
import logging
import logging.config
import logging.handlers
import socketserver
import struct

import riaps.log.visualizers.tmux as visualizer

theViewer = visualizer.View(session_name="platformLogger")


class LogRecordStreamHandler(socketserver.StreamRequestHandler):
    """Handler for a streaming logging request.
    This basically logs the record using whatever logging policy is
    configured locally.
    """

    def setup(self) -> None:
        global theViewer
        super(LogRecordStreamHandler, self).setup()
        self.logger = logging.getLogger(__name__)

    def handle(self):
        """
        Handle multiple requests - each expected to be a 4-byte length,
        followed by the LogRecord in pickle format. Logs the record
        according to whatever policy is configured locally.
        """
        while True:
            chunk = self.connection.recv(4)
            if len(chunk) < 4:
                break
            slen = struct.unpack('>L', chunk)[0]
            chunk = self.connection.recv(slen)
            while len(chunk) < slen:
                chunk += self.connection.recv(slen - len(chunk))
            obj = self.unpickle(chunk)
            obj["msg"] = f"{obj['msg']}: {self.client_address}"
            record = logging.makeLogRecord(obj)

            node_name = self.client_address[0]

            if node_name not in theViewer.nodes:
                theViewer.add_node_display(node_name=node_name)

            # self.handle_log_record(record)
            theViewer.write_display(node_name=node_name, msg=record.getMessage())

    def unpickle(self, data):
        return pickle.loads(data)

    def handle_log_record(self, record):
        logger = logging.getLogger(__name__)
        tty_id = theViewer.nodes[self.client_address[0]]["tty"]
        print(f"tty_id: {tty_id}")
        view_handle = logging.FileHandler(filename=tty_id)
        view_handle.setLevel("DEBUG")
        logger.addHandler(view_handle)

        # N.B. EVERY record gets logged. This is because Logger.handle
        # is normally called AFTER logger-level filtering. If you want
        # to do filtering, do it at the client end to save wasting
        # cycles and network bandwidth!
        # print(f"logger: {logger}, handlers: {logger.handlers}, level: {logger.level}")

        logger.handle(record)


class LogRecordSocketReceiver(socketserver.ThreadingTCPServer):
    """
    Simple TCP socket-based logging receiver suitable for testing.
    """

    allow_reuse_address = 1

    def __init__(self, host,
                 port=logging.handlers.DEFAULT_TCP_LOGGING_PORT,
                 handler=LogRecordStreamHandler):

        socketserver.ThreadingTCPServer.__init__(self, (host, port), handler)
        self.abort = 0
        self.timeout = 1
        self.logname = None
        self.logger = logging.getLogger(__name__)

    def serve_until_stopped(self):
        self.logger.info('About to start TCP server...')
        import select
        abort = 0
        while not abort:
            rd, wr, ex = select.select([self.socket.fileno()],
                                       [], [],
                                       self.timeout)

            # This keeps the sever active while there are logs to process.
            if rd:
                # print(f"Call handle_request. What is rd? {rd}")
                self.handle_request()
            abort = self.abort

    def terminate(self):
        self.logger.info("terminating")
        self.abort = True
        theViewer.close_session()

