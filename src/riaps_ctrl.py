#!/usr/bin/python3
'''Top level script to start the controller

Example:

    ``riaps_ctrl [-p|--port port] [-t|--trace host:port] [script|-]``

The controller runs on the control node and it manages all target nodes.
Unless the ``port`` argument is specified, the rpyc_registry service must 
be running somewhere on the subnet accessible to both the controller and 
the target nodes.


Arguments
    - ``-p|--port port`` : port number to access the controller from the target nodes (if no registry)
    - ``-t|--trace host:port`` : starts the controller in trace mode; it connects to a debug server running on the host and listening on the port. 
    - ``script|-`` : executes the script file via the built-in command line interpreter. - reads from standard input.  

'''

import riaps.ctrl.main

if __name__ == '__main__':
    riaps.ctrl.main.main()
    