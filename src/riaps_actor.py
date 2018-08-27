#!/usr/bin/python3
'''Top level wrapper script for a RIAPS actor.

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

import riaps.run.main

if __name__ == '__main__':
    riaps.run.main.main()
    
