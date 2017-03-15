'''
Various network interface utility functions
Created on Nov 4, 2016

@author: riaps
'''

import netifaces

def getNetworkInterfaces():
    '''
     Determine the IP address of  the network interfaces
     Return a tuple of list of global IP addresses, list of MAC addresses, and local IP address
     ''' 
    local = None
    ipAddressList = []
    macAddressList = []
    ifNames = netifaces.interfaces()      
    for ifName in ifNames:
        ifInfo = netifaces.ifaddresses(ifName)
        if netifaces.AF_INET in ifInfo:
            ifAddrs = ifInfo[netifaces.AF_INET]
            ifAddr = ifAddrs[0]['addr']
            if ifAddr == '127.0.0.1':
                local = ifAddr
            else:
                ipAddressList.append(ifAddr)
                linkAddrs = netifaces.ifaddresses(ifName)[netifaces.AF_LINK]
                linkAddr = linkAddrs[0]['addr'].replace(':','')
                macAddressList.append(linkAddr)
    return (ipAddressList,macAddressList,local)
