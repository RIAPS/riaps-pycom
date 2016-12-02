'''
Discovery service - main program
Created on Oct 19, 2016
@author: riaps
'''
import sys
import os
import argparse
from .discs import DiscoService

# Singleton DiscoService object 
theDisco = None

# Interactive console for debugging (not used)
def interact():
    import code
    code.InteractiveConsole(locals=globals()).interact()

  
def main(debug=True):
    parser = argparse.ArgumentParser()
    parser.add_argument("-d","--database", help="database location")
    args = parser.parse_args()
    try:
        pass
    except: 
        print ("Unexpected error:", sys.exc_info()[0])
        raise
    sys.path.append(os.getcwd())   # Ensure load_module works from current directory
    global theDisco
    theDisco = DiscoService(args.database)  # Assign the service to the singleton
    theDisco.start()
    theDisco.run()
#    if debug:
#        interact()

if __name__ == '__main__':
    main()
    