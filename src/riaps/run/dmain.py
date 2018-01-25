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
from riaps.utils.trace import riaps_trace

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

def sigXCPUHandler(signal,frame):
    global theActor
    theActor.handleCPULimit()
    
def sigXMEMHandler(signal,frame):
    global theActor
    theActor.handleMemLimit()

def sigXSPCHandler(signal,frame):
    global theActor
    theActor.handleSpcLimit()
    
def main(debug=True):
    parser = argparse.ArgumentParser()
    parser.add_argument("app", help="app name")             # App name
    parser.add_argument("model", help="model file name")    # Model file argument
    parser.add_argument("device", help="device name")         # Device name argument
    parser.add_argument("-t","--trace",help="debug server on host:port")
    (args,rest) = parser.parse_known_args()

    # Read configuration    
    global theConfig
    theConfig = Config()
    traced = riaps_trace(args.trace,'DEVICE_DEBUG_SERVER')
       
    appFolder = os.getenv('RIAPSAPPS', './')
    appFolder = join(appFolder,args.app)
    modelFileName = join(appFolder,args.model) 
    try:
        fp = open(modelFileName,'r')           # Load model file
        model = json.load(fp)
        aName = args.device
    except IOError as e:
        print ("I/O error({0}): {1}".format(e.errno, e.strerror))
        os._exit(1)
    except: 
        print ("Unexpected error:", sys.exc_info()[0])
        os._exit(1)
    sys.path.append(appFolder)   # Ensure load_module works from current directory
    
    # Setup the logger formatter 
    logging.Formatter.default_time_format = '%H:%M:%S'
    logging.Formatter.default_msec_format = '%s,%03d'

    global theDevice
    theDevice = Device(model,args.model,aName,rest) # Construct the Device
    signal.signal(signal.SIGTERM,termHandler)       # Termination signal handler
    signal.signal(signal.SIGXCPU,sigXCPUHandler)    # CPU limit exceeded handler
    signal.signal(signal.SIGUSR1,sigXMEMHandler)    # Mem limit exceeded handler
    signal.signal(signal.SIGUSR2,sigXSPCHandler)    # Spc limit exceeded handler     
    try:
        theDevice.setup()                        # Setup the objects contained in the device
        theDevice.activate()                     # Activate the components 
        theDevice.start()                        # Start the device main loop
    except:
        info = sys.exc_info()
        print ("riaps_device: Fatal error: %s" % (info[1],))
        os._exit(1)
#     if debug:
#         interact()

if __name__ == '__main__':
    main()
    os._exit(0)