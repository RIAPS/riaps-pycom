'''
Deployment commander - main program
Created on Nov 1, 2016

@author: riaps
'''
import sys
import os
import argparse
import logging

from riaps.ctrl.ctrl import Controller
from riaps.consts.defs import *
from riaps.utils.config import Config 

# Interactive console for debugging (not used)
def interact():
    import code
    code.InteractiveConsole(locals=globals()).interact()

conf = None
  
def main(debug=True):
    parser = argparse.ArgumentParser()
    parser.add_argument("-p","--port", type=int, 
                        default=const.ctrlPort, 
                        help="server port number")
    args = parser.parse_args()
    sys.path.append(os.getcwd())   # Ensure load_module works from current directory
#
    logging.basicConfig(level=logging.INFO)
    global conf
    conf = Config()
    c = None
    try:
        c = Controller(args.port)
        c.start()       # Start concurrent activities
        c.run()         # Run the GUI Loop
        c.stop()        # Stop all concurrent activities
    except:
        if c != None:
            c.stop()
        raise
    #print ("Unexpected error:", sys.exc_info()[0])
    sys.exit()

if __name__ == '__main__':
    pass