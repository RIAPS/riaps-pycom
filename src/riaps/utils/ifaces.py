'''
Various network interface utility functions
Created on Nov 4, 2016

@author: riaps
'''

import netifaces
from riaps.utils.config import Config

def getNetworkInterfaces(nicName=None):
    '''
     Determine the IP address of  the network interfaces
     Return a tuple of list of global IP addresses, list of MAC addresses, and local IP address
     ''' 
    if nicName is None:
        nicName = Config.NIC_NAME
    local = None
    ipAddressList = []
    macAddressList = []
    ifNameList = []
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
                ifNameList.append(ifName)
                linkAddrs = netifaces.ifaddresses(ifName)[netifaces.AF_LINK]
                linkAddr = linkAddrs[0]['addr'].replace(':','')
                macAddressList.append(linkAddr)
                if(nicName == ifName):
                    ipAddressList = [ipAddressList[-1]]
                    macAddressList = [macAddressList[-1]] 
                    break
    return (ipAddressList,macAddressList,ifNameList,local)

