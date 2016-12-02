'''
RIAPS run-time system main program for an actor
Created on Oct 9, 2016

@author: riaps
'''
import sys
import os
from os.path import join
import argparse
import json
import logging

from .actor import Actor

# Singleton Actor object
theActor = None

# Interactive console for debugging (not used)
def interact():
    import code
    code.InteractiveConsole(locals=globals()).interact()

  
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
        raise
    except: 
        print ("Unexpected error:", sys.exc_info()[0])
        raise
    sys.path.append(appFolder)   # Ensure load_module works from current directory
    
    # Setup the logger formatter 
    logging.Formatter.default_time_format = '%H:%M:%S'
    logging.Formatter.default_msec_format = '%s,%03d'
    
    global theActor
    theActor = Actor(model,aName,rest)      # Construct the Actor
    theActor.setup()                        # Setup the objects contained in the actor
    theActor.activate()                     # Activate the components 
    theActor.start()                        # Start the actor main loop
#     if debug:
#         interact()

if __name__ == '__main__':
    main()