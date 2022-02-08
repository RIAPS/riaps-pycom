'''RIAPS run-time system main program for an actor. 
It is called by the wrapper script ``riaps_actor``.

Example:

    ``riaps_actor app model actor args [-t|--trace host:port]``
    
The actor is started and terminated by the deployment manager. 
    
Arguments:
    - ``app``:    Name of application
    - ``model``:  Name of .json model file
    - ``actor``:  Name of actor
    - ``args``:   List of arguments of the form: -keyword value
    - ``-t|--trace host:port`` : starts the actor in trace mode; it connects to a debug server running on the host and listening on the port. 

'''

import sys
import os, signal
from os.path import join
import argparse
import json
import logging
import traceback 

from apparmor_monkeys import patch_modules
patch_modules()

from riaps.utils.config import Config
from riaps.utils.trace import riaps_trace

from .actor import Actor

# : Singleton Actor object
theActor = None

# : Singleton Config object, holds the configuration information. 
theConfig = None 


def interact():
    ''' Interactive console for debugging (not used)
    '''
    import code
    code.InteractiveConsole(locals=globals()).interact()


def termHandler(signal, frame):
    '''Actor termination handler, attached to SIGTERM.
    
    Simply calls the Actor.terminate() method.
    '''
    global theActor
    theActor.terminate()

# def sigXCPUHandler(signal,frame):
#     global theActor
#     theActor.handleCPULimit()
#     
# def sigXMEMHandler(signal,frame):
#     global theActor
#     theActor.handleMemLimit()
#     
# def sigXSPCHandler(signal,frame):
#     global theActor
#     theActor.handleSpcLimit()

    
def main(debug=True):
    ''' main() entry point for riaps_actor. 
    
    Parses its arguments, reads the configuration file, if started in 
    debug mode it waits for connecting to the debug server, then it
    reads the model file creates the singleton Actor object.
      
    '''
    
    parser = argparse.ArgumentParser()
    parser.add_argument("app", help="app name")  # App name
    parser.add_argument("model", help="model file name")  # Model file argument
    parser.add_argument("actor", help="actor name")  # Actor name argument
    parser.add_argument("-t", "--trace", help="debug server on host:port")
    (args, rest) = parser.parse_known_args()
    
    # Read configuration    
    global theConfig
    theConfig = Config()
    traced = riaps_trace(args.trace, 'ACTOR_DEBUG_SERVER')
    
    appFolder = os.getenv('RIAPSAPPS', './')
    appFolder = join(appFolder, args.app)
    modelFileName = join(appFolder, args.model) 
    try:
        fp = open(modelFileName, 'r')  # Load model file
        model = json.load(fp)
        aName = args.actor
    except IOError as e:
        print ("I/O error({0}): {1} {2}".format(e.errno, e.strerror, e.filename))
        os._exit(1)
    except: 
        print ("Unexpected error:", sys.exc_info()[0])
        os._exit(1)
    sys.path.append(appFolder)  # Ensure load_module works from current directory
    
    # Setup the logger formatter 
    logging.Formatter.default_time_format = '%H:%M:%S'
    logging.Formatter.default_msec_format = '%s,%03d'

    global theActor
    theActor = Actor(model, args.model, aName, rest)  # Construct the Actor
    signal.signal(signal.SIGTERM, termHandler)  # Termination signal handler
#     signal.signal(signal.SIGXCPU,sigXCPUHandler)    # CPU limit exceeded handler 
#     signal.signal(signal.SIGUSR1,sigXMEMHandler)    # Mem limit exceeded handler 
#     signal.signal(signal.SIGUSR2,sigXSPCHandler)    # Spc limit exceeded handler     
    try:
        theActor.setup()  # Setup the objects contained in the actor
        theActor.activate()  # Activate the components 
        theActor.start()  # Start the actor main loop
    except:
        traceback.print_exc()
        info = sys.exc_info()
        print ("riaps_actor: Fatal error: %s" % (info[1],))
        os._exit(1)
#     if debug:
#         interact()


if __name__ == '__main__':
    main()
    os._exit(0)
