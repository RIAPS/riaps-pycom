'''
Deployment controller - main program
Created on Nov 1, 2016

@author: riaps
'''
import sys
import os,signal
import argparse
# import logging

from riaps.ctrl.ctrl import Controller
from riaps.consts.defs import *
from riaps.utils.config import Config 

conf = None
theController = None

# Interactive console for debugging (not used)
def interact():
    import code
    code.InteractiveConsole(locals=globals()).interact()

def termHandler(signal,frame):
    global theController
    if theController != None:
        try:
            theController.stop()
        except:
            pass
    sys.exit()

def main(debug=True):
    parser = argparse.ArgumentParser()
    parser.add_argument("-p","--port", type=int, 
                        default=const.ctrlPort, 
                        help="server port number")
    args = parser.parse_args()
    sys.path.append(os.getcwd())   # Ensure load_module works from current directory
#
#   logging.basicConfig(level=logging.INFO)
    global conf
    conf = Config()
    global theController
    theController = None
    signal.signal(signal.SIGTERM,termHandler)
    signal.signal(signal.SIGINT,termHandler)
    try:
        theController = Controller(args.port)
        theController.start()       # Start concurrent activities
        theController.run()         # Run the GUI Loop
        theController.stop()        # Stop all concurrent activities
    except:
        if theController != None:
            theController.stop()
    #print ("Unexpected error:", sys.exc_info()[0])
    sys.exit()

if __name__ == '__main__':
    pass