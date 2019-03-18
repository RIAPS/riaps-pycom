#!/usr/bin/python3
'''Top-level script to start the language processor ('lang') for app models

Example:
    ``riaps_lang model [-v|--verbose]``

The program analyzes the model file and generates a JSON file. 

Arguments:
    - ``model`` : Name of model file to be processed
    - ``-v|--verbose``: print the resulting JSON file on the console 

'''
from riaps.lang.lang import main

if __name__ == '__main__':
    main()
    
