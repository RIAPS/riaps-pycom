"""
Log Server - main program
Created on Oct 10, 2022

@author: riaps
"""
import sys
import os
import signal
import argparse
import multiprocessing
import traceback

import riaps.log.server
from riaps.consts.defs import *
from riaps.utils.config import Config
from riaps.log.server import BaseLogServer
import riaps.log.visualizers.tmux as visualizer
from riaps.utils.trace import riaps_trace


# : Singleton Config object, holds the configuration information.
theConfig = None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--platform", nargs=2, metavar=("host", "port"))
    parser.add_argument("-a", "--app", nargs=2, metavar=("host", "port"))

    parser.add_argument("-t", "--trace", help="debug server on host:port")
    parser.add_argument('script', nargs='?', help='script name, or - for stdin')
    args = parser.parse_args()
    print(args)

    sys.path.append(os.getcwd())   # Ensure load_module works from current directory

    traced = riaps_trace(args.trace, 'LOG_SERVER_DEBUG_SERVER')

    p_host = None
    p_port = None
    a_host = None
    a_port = None
    try:
        if args.platform:
            p_host, p_port = parse_args(args.platform)
        if args.app:
            a_host, a_port = parse_args(args.app)
        setup(platform=(p_host, p_port), app=(a_host, a_port))
    except:
        traceback.print_exc()
        info = sys.exc_info()
        print(f"log server error: {info[1]}")
        traceback.print_exc()
        os._exit(0)


def parse_args(server):
    host = server[0]
    try:
        port = int(server[1])
    except ValueError as e:
        print(f"Port must be an int: {e}")
        return
    return host, port


def setup(platform, app):
    # Read configuration
    global theConfig
    theConfig = Config()

    servers = {}

    if platform:
        view = visualizer.View(session_name="platform")
        platform_log_server = BaseLogServer(server_address=platform,
                                            RequestHandlerClass=riaps.log.server.PlatformLogHandler,
                                            view=view)

        p = multiprocessing.Process(target=platform_log_server.serve_until_stopped)
        servers["platform"] = {"server": platform_log_server,
                               "process": p,
                               "view": view}
        p.start()

    if app:
        view = visualizer.View(session_name="app")
        app_log_server = BaseLogServer(server_address=app,
                                       RequestHandlerClass=riaps.log.server.AppLogHandler,
                                       view=view)
        p = multiprocessing.Process(target=app_log_server.serve_until_stopped)
        servers["app"] = {"server": app_log_server,
                          "process": p,
                          "view": view}
        p.start()

    def term_handler(signal, frame):
        print("\nCall term_handler")
        for server_type, obj in servers.items():
            if obj["process"] is not None:
                try:
                    obj["process"].terminate()
                    obj["view"].close_session()
                except:
                    pass
        os._exit(0)

    signal.signal(signal.SIGTERM, term_handler)
    signal.signal(signal.SIGINT, term_handler)


if __name__ == '__main__':
    setup(("172.21.20.70", 9020),
          None)
    # main()
    # os._exit(0)
