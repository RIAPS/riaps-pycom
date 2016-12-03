'''
Top level script to start the deployment manager
It connects to the RIAPSCONTROL service, either through the service registry or through the specified 
node and port

Created on Nov 4, 2016

Arguments
-p (or --port) Port number for the RIAPSCONTROL service
-n (or --node) Host IP address of the controller node

@author: riaps
'''

import riaps.deplo.main

if __name__ == '__main__':
    riaps.deplo.main.main()
    