'''
Deployment manager main program
Created on Nov 1, 2016

@author: riaps
'''
import sys
import os,signal
import argparse
import traceback
import logging

import faulthandler
faulthandler.enable()

from .deplo import DeploService
from riaps.consts.defs import *
from riaps.utils.config import Config 
from riaps.utils.trace import riaps_trace

# Singleton Deployment Service object 
theDepl = None

# Config object
conf = None 

# Interactive console for debugging (not used)
def interact():
    import code
    code.InteractiveConsole(locals=globals()).interact()

def termHandler(signal,frame):
    global theDepl
    theDepl.terminate()
      
def main(debug=True):
    parser = argparse.ArgumentParser()
    parser.add_argument("-p","--port", type=int,  default=const.ctrlPort, help="controller port number")
    parser.add_argument("-n","--node", default=const.ctrlNode, help="controller node")
    parser.add_argument("-t","--trace",help="debug server on host:port")
    args = parser.parse_args()
    try:
        pass
    except: 
        print ("Unexpected error:", sys.exc_info()[0])
        raise

    sys.path.append(os.getcwd())   # Ensure load_module works from current directory
    global conf
    conf = Config()
    # Setup the logger formatter 
    logging.Formatter.default_time_format = '%H:%M:%S'
    logging.Formatter.default_msec_format = '%s,%03d'
    
    signal.signal(signal.SIGTERM,termHandler)
    signal.signal(signal.SIGINT,termHandler)
    _traced = riaps_trace(args.trace,'DEPLO_DEBUG_SERVER')
    try:
        global theDepl
        theDepl = DeploService(args.node,args.port)  # Assign the service to the singleton
        theDepl.setup()
        theDepl.run()
    except:
        traceback.print_exc()
        info = sys.exc_info()
        print ("riaps_deplo: Fatal error: %s" % (info[1],))
        os._exit(1)
#     if debug:
#         interact()

if __name__ == '__main__':
    pass
