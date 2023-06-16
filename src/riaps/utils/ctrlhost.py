#!/usr/bin/python3
'''
Retrieves the IP address(es) of the RIAPS Control host
and prints the out on the standard output, one address per line. 
'''

import rpyc.utils.factory

def main():
    try:
        for pair in rpyc.utils.factory.discover("RIAPSCONTROL"):
            print (pair[0])
    except rpyc.utils.factory.DiscoveryError:
        pass

if __name__ == '__main__':
    pass
        
    
