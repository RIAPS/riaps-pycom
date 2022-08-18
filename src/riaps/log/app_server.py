import logging
import socketserver
import riaps.log.visualizers.tmux as visualizer

theViewer = None

class MyTCPHandler(socketserver.StreamRequestHandler):
    """
    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def setup(self) -> None:
        global theViewer
        super(MyTCPHandler, self).setup()

    def handle(self):
        while True:
            data_bytes = self.rfile.readline().strip()
            if not data_bytes:
                break
            data_string = data_bytes.decode("utf-8")
            data = f"{data_string}: client_address: {self.client_address}"
            node_name = self.client_address[0]
            if self.client_address[0] not in theViewer.nodes:
                theViewer.add_node_display(node_name=node_name)
            theViewer.write_display(node_name=node_name, msg=data)


class AppLogServer:

    def __init__(self, host, port):
        self.logger = logging.getLogger(__name__)
        self.host = host
        self.port = port

    def serve_until_stopped(self):
        self.logger.info('About to start App Log server...')
        with socketserver.ThreadingTCPServer((self.host, self.port), MyTCPHandler) as server:
            # Activate the server; this will keep running until you
            # interrupt the program with Ctrl-C
            server.serve_forever()

    def terminate(self):
        self.logger.info("terminating")
        theViewer.close_session()


import argparse
import os
import signal
import sys
import traceback
from riaps.consts.defs import *
from riaps.utils.config import Config
from riaps.utils.trace import riaps_trace


# : Singleton Log Server object
theLogServer = None

# : Singleton Config object, holds the configuration information.
theConfig = None


def termHandler(signal, frame):
    global theLogServer
    if theLogServer != None:
        try:
            theLogServer.terminate()
        except:
            pass
    os._exit(0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--host", type=str,
        default=const.applogServerHost,
        help="server port number"
    )
    parser.add_argument(
        "-p", "--port", type=int,
        default=const.applogServerPort,
        help="server port number")
    parser.add_argument(
        "-v", "--visualizer", type=str,
        default=const.applogVisualizer,
        help="choose how to view logs"
    )

    parser.add_argument("-t", "--trace", help="debug server on host:port")
    parser.add_argument('script', nargs='?', help='script name, or - for stdin')
    args = parser.parse_args()
    sys.path.append(os.getcwd())   # Ensure load_module works from current directory

    # Read configuration
    global theConfig
    theConfig = Config()

    traced = riaps_trace(args.trace, 'LOG_SERVER_DEBUG_SERVER')
    global theLogServer
    theLogServer = None
    signal.signal(signal.SIGTERM, termHandler)
    signal.signal(signal.SIGINT, termHandler)

    logger = logging.getLogger(__name__)
    global theViewer
    theViewer = visualizer.View(session_name=args.visualizer)

    try:
        theLogServer = AppLogServer(args.host,
                                    args.port)
        theLogServer.serve_until_stopped()
    except:
        traceback.print_exc()
        info = sys.exc_info()
        print(f"log server error: {info[1]}")
        traceback.print_exc()
        os._exit(0)

if __name__ == '__main__':
    main()
    os._exit(0)
