'''
Discovery service - main program
Created on Oct 19, 2016
@author: riaps
'''
import sys
import os,signal
import argparse
from .devm import DevmService
from riaps.utils.config import Config

# Singleton DiscoService object 
theDevm = None

# Config object
conf = None 

# Interactive console for debugging (not used)
def interact():
    import code
    code.InteractiveConsole(locals=globals()).interact()

def termHandler(signal,frame):
    global theDevm
    theDevm.terminate()
  
def main(debug=True):
    parser = argparse.ArgumentParser()
    # parser.add_argument("-d","--database", help="database location")
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
    
    # Create singleton 
    global theDevm
    signal.signal(signal.SIGTERM,termHandler)
    signal.signal(signal.SIGINT,termHandler)
    theDevm = DevmService() # Assign the service to the singleton
    theDevm.start()
    theDevm.run()
#    if debug:
#        interact()

if __name__ == '__main__':
    main()
    