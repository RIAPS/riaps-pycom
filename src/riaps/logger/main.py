"""
Log Server - main program
Created on Oct 10, 2022

@author: riaps
"""

import argparse
import multiprocessing
import os
import queue
import signal
import sys
import traceback
import logging

# from riaps.consts.defs import *
from riaps.utils.config import Config
from riaps.utils.ifaces import getNetworkInterfaces
from riaps.logger.server import AppLogServer, PlatformLogServer
import riaps.logger.drivers.factory as driver_factory

RIAPS_LOGGER_DEFAULT_TCP_PORT = logging.handlers.DEFAULT_TCP_LOGGING_PORT

# global Config object, holds the configuration information.
theConfig = None

# global dictionary for all servers 
theServers = {}

# global logger ('riaps.logger')
theLogger = None

def term_handler(_signal, _frame):
    theLogger.info("term_handler called")
    for _, obj in theServers.items():
        proc = obj.get("process",None)
        if proc:
            try:
                proc.terminate()
                proc.join()
                obj["driver"].close()
            except:
                pass
    os._exit(0)

def setup(pserver, aserver, driver_type):
    global theLogger
    if pserver:
        q = queue.Queue()
        driver = driver_factory.get_driver(driver_type=driver_type, session_name="platform")
        platform_log_server = PlatformLogServer(server_address=pserver,
                                                driver=driver,
                                                q=q)
        p = multiprocessing.Process(target=platform_log_server.serve_until_stopped,
                                    name="riaps.logger.platform", daemon=False)
        theServers["platform"] = {"server": platform_log_server,
                                  "process": p,
                                  "driver": driver}
        p.start()

    if aserver:
        q = queue.Queue()
        driver = driver_factory.get_driver(driver_type=driver_type, session_name="app")
        app_log_server = AppLogServer(server_address=aserver,
                                      driver=driver,
                                      q=q)
        p = multiprocessing.Process(target=app_log_server.serve_until_stopped,
                                    name="riaps.logger.app",
                                    daemon=False)
        theServers["app"] = {"server": app_log_server,
                             "process": p,
                             "driver": driver}
        p.start()
        
    signal.signal(signal.SIGTERM, term_handler)
    signal.signal(signal.SIGINT, term_handler)


def parse_args(arg,default_host,default_port):
    try:
        host,port = arg.split(':')
        if host == '*':
            host = default_host
        if port == None:
            port = default_port
        else:
            port = int(port)
    except ValueError as e:
        theLogger.error(f"Invalid host:port argument: {e}")
        return None
    return host, port

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--platform", nargs='?', metavar='HOST:PORT',  \
                        const="*:%d" % RIAPS_LOGGER_DEFAULT_TCP_PORT, \
                        help="platform logging [via HOST:PORT]")
    parser.add_argument("-a", "--app", nargs='?', metavar='HOST:PORT', \
                        const="*:%d" % (RIAPS_LOGGER_DEFAULT_TCP_PORT+1), \
                        help="app logging [via HOST:PORT]")
    parser.add_argument("-d", "--driver_type", default="console")

    parser.add_argument('script', nargs='?', help='script name, or - for stdin')
    args = parser.parse_args()
    
    global theConfig
    theConfig = Config()
    
    global theLogger
    theLogger = logging.getLogger("riaps.logger")
    theLogger.propagate = False
    
    (globalIPs,_globalMACs,_globalNames,_localIP) = getNetworkInterfaces()
    assert len(globalIPs) > 0 and len(_globalMACs) > 0, "Error: no active network interface"
    default_host = globalIPs[0]
    default_port = RIAPS_LOGGER_DEFAULT_TCP_PORT

    pserver_host_port = None
    aserver_host_port = None

    if args.platform == None and args.app == None:
        print("riaps_logger: nothing to log")
        os._exit(0)
    try:
        if args.platform:
            theLogger.info("platform arg: %r" % args.platform)
            pserver_host_port = parse_args(args.platform,default_host,default_port)
        if args.app:
            theLogger.info("app arg: %r" % args.app)
            aserver_host_port = parse_args(args.app,default_host,default_port+1)
        if pserver_host_port is None and aserver_host_port is None:
            os._exit(0)
        setup(pserver_host_port,aserver_host_port,args.driver_type)
    except:
            traceback.print_exc()
            info = sys.exc_info()
            theLogger.error(f"log server error: {info[1]}")
            traceback.print_exc()
    for _, obj in theServers.items():
        proc = obj.get("process",None)
        try:
            proc.join()
            obj["driver"].close()
        except:
            pass
    theLogger.info('exiting')
    os._exit(0)

if __name__ == '__main__':
    main()

