#!/usr/bin/python3
'''Top-level script of the deployment language processor

Example:
    ``riaps_depll model [-v | --verbose] [-g|--generate]``

Arguments:
    - ``model``: name of model file to be processed
    - ``-v|--verbose``: print the resulting JSON file on the console
    - ``-g``: generate a JSON file  

'''

from riaps.lang.depl import main

if __name__ == '__main__':
    main(True)
    
