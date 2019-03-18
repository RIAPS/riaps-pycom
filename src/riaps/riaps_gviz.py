#!/usr/bin/python3
''' Top-level script to start the graphic visualization processor ('gviz')

Example:

    ``riaps_gviz model deplo [-v|--verbose]``

The script generates a .dot file shown the allocation of components and actors 
to target nodes based on the model and deployment files. 

Arguments:
    -``model``: name of application model file to be processed
    - ``deplo``: name of deployment model file to be processed
    - ``-v|--verbose``: prints the JSON produced from the deployment model
    
Output:
    - ``appname.dot`` : graphviz-style dot file for the name application (based on the model)  
    
'''
from riaps.lang.gviz import main

if __name__ == '__main__':
    main()
    
