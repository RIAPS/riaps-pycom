'''
RIAPS run-time system main program for an actor
Created on Oct 9, 2016

@author: riaps
'''
import sys
import os, signal
from os.path import join
import argparse
import json
import logging
from riaps.utils.config import Config

from .actor import Actor

# Singleton Actor object
theActor = None

# Config object
theConfig = None 

# Interactive console for debugging (not used)
def interact():
    import code
    code.InteractiveConsole(locals=globals()).interact()

def termHandler(signal,frame):
    global theActor
    theActor.terminate()

def sigXCPUHandler(signal,frame):
    global theActor
    theActor.handleCPULimit()
    
def main(debug=True):
    parser = argparse.ArgumentParser()
    parser.add_argument("app", help="app name")             # App name
    parser.add_argument("model", help="model file name")    # Model file argument
    parser.add_argument("actor", help="actor name")         # Actor name argument
    (args,rest) = parser.parse_known_args()
    appFolder = os.getenv('RIAPSAPPS', './')
    appFolder = join(appFolder,args.app)
    modelFileName = join(appFolder,args.model) 
    try:
        fp = open(modelFileName,'r')           # Load model file
        model = json.load(fp)
        aName = args.actor
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

    # Read configuration    
    global theConfig
    theConfig = Config()
    
    global theActor
    theActor = Actor(model,args.model,aName,rest)   # Construct the Actor
    signal.signal(signal.SIGTERM,termHandler)       # Termination signal handler
    signal.signal(signal.SIGXCPU,sigXCPUHandler)    # CPU limit exceeded handler    
    try:
        theActor.setup()                        # Setup the objects contained in the actor
        theActor.activate()                     # Activate the components 
        theActor.start()                        # Start the actor main loop
    except:
        info = sys.exc_info()
        print ("riaps_actor: Fatal error: %s" % (info[1],))
        os._exit(1)
#     if debug:
#         interact()

if __name__ == '__main__':
    main()
    os._exit(0)