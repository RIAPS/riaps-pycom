#!/usr/bin/python3
'''Top-level script to start the discovery service (disco)

Example:
    ``riaps_disco [-d|--database location] [-t|--trace host:port]``

The discovery service is started by the deployment manager. 

Arguments:
    - ``-d|--database location`` : location of the discovery service database. Fore the redis-based implementation this is of the form ``host:port``. 
    - ``-t|--trace host:port`` : starts the service in trace mode; it connects to a debug server running on the host and listening on the port.
'''

import riaps.discd.main

if __name__ == '__main__':
    riaps.discd.main.main()
    
