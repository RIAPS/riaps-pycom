'''
Discovery service - main program
Created on Oct 19, 2016
@author: riaps
'''
import sys
import os,signal
import argparse
from .discs import DiscoService
from riaps.utils.config import Config
from riaps.utils.trace import riaps_trace

# Singleton DiscoService object 
theDisco = None

# Config object
conf = None 

def termHandler(signal,frame):
    global theDisco
    theDisco.terminate()

# Interactive console for debugging (not used)
def interact():
    import code
    code.InteractiveConsole(locals=globals()).interact()

  
def main(debug=True):
    parser = argparse.ArgumentParser()
    parser.add_argument("-d","--database", help="database location")
    parser.add_argument("-t","--trace",help="debug server on host:port")
    args = parser.parse_args()
    try:
        pass
    except: 
        print ("Unexpected error:", sys.exc_info()[0])
        raise
    sys.path.append(os.getcwd())   # Ensure load_module works from current directory
    
    # Read configuration
    global conf
    conf = Config()
    traced = riaps_trace(args.trace,'DISCO_DEBUG_SERVER')
    # Create singleton 
    global theDisco
    theDisco = DiscoService(args.database)  # Assign the service to the singleton
    signal.signal(signal.SIGTERM,termHandler)
    signal.signal(signal.SIGINT,termHandler)
    theDisco.start()
    theDisco.run()
#    if debug:
#        interact()

if __name__ == '__main__':
    main()
    