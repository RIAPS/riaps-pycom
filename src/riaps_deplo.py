#!/usr/bin/python3
'''Top level script to start the deployment manager (deplo)

Example:

    ``riaps_deplo [-p|--port port] [-n|--node node] [-t|--trace host:port]``

The deployment manager runs on each target nodes and it manages all actors and services.
Unless the ``port`` and ``node`` are specified, the rpyc_registry service must 
be running somewhere on the subnet accessible to both the controller and 
the target nodes.

Arguments:
    - ``-p|--port port``: Port number for the controller node (if no registry)
    - ``-n|--node node``: Host name for the controller node (if no registry)
    - ``-t|--trace host:port`` : starts the manager in trace mode; it connects to a debug server running on the host and listening on the port. 

'''

import riaps.deplo.main

if __name__ == '__main__':
    riaps.deplo.main.main()
    