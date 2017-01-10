'''
RIAPS run-time system main program for an device
Created on Jan 7, 2017

@author: riaps
'''
import sys
import os, signal
from os.path import join
import argparse
import json
import logging
from riaps.utils.config import Config

from .device import Device

# Singleton Device object
theDevice = None

# Config object
theConfig = None 

# Interactive console for debugging (not used)
def interact():
    import code
    code.InteractiveConsole(locals=globals()).interact()

def termHandler(signal,frame):
    global theDevice
    theDevice.terminate()
      
def main(debug=True):
    parser = argparse.ArgumentParser()
    parser.add_argument("app", help="app name")             # App name
    parser.add_argument("model", help="model file name")    # Model file argument
    parser.add_argument("device", help="device name")         # Device name argument
    (args,rest) = parser.parse_known_args()
    appFolder = os.getenv('RIAPSAPPS', './')
    appFolder = join(appFolder,args.app)
    modelFileName = join(appFolder,args.model) 
    try:
        fp = open(modelFileName,'r')           # Load model file
        model = json.load(fp)
        aName = args.device
    except IOError as e:
        print ("I/O error({0}): {1}".format(e.errno, e.strerror))
        raise
    except: 
        print ("Unexpected error:", sys.exc_info()[0])
        raise
    sys.path.append(appFolder)   # Ensure load_module works from current directory
    
    # Setup the logger formatter 
    logging.Formatter.default_time_format = '%H:%M:%S'
    logging.Formatter.default_msec_format = '%s,%03d'

    # Read configuration    
    global theConfig
    theConfig = Config()
    
    global theDevice
    theDevice = Device(model,args.model,aName,rest)      # Construct the Device
    signal.signal(signal.SIGTERM,termHandler)
    theDevice.setup()                        # Setup the objects contained in the device
    theDevice.activate()                     # Activate the components 
    theDevice.start()                        # Start the device main loop
#     if debug:
#         interact()

if __name__ == '__main__':
    main()