#!/usr/bin/python3
'''Top level script to start a device actor

Example:

    ``riaps_device app model actor args [-t|--trace host:port]``
    
The device actor is started and terminated by the deployment manager. 
    
Arguments:
    - ``app``:    Name of application
    - ``model``:  Name of .json model file
    - ``actor``:  Name of actor
    - ``args``:   List of arguments of the form: -keyword value
    - ``-t|--trace host:port`` : starts the device actor in trace mode; it connects to a debug server running on the host and listening on the port. 

'''

import riaps.run.dmain

if __name__ == '__main__':
    riaps.run.dmain.main()
    
