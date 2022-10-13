'''
Deployment controller - main program
Created on Nov 1, 2016

@author: riaps
'''
import sys
import os
import signal
import argparse
import traceback

from riaps.consts.defs import *
from riaps.utils.config import Config
from riaps.log.server import LogRecordSocketReceiver
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
        default=const.logServerHost,
        help="server port number"
    )
    parser.add_argument(
        "-p", "--port", type=int,
        default=const.logServerPort,
        help="server port number")
    parser.add_argument(
        "-v", "--visualizer", type=str,
        default=const.logVisualizer,
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

    try:
        theLogServer = LogRecordSocketReceiver(args.host,
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
