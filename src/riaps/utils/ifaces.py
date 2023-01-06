'''
Various network interface utility functions
Created on Nov 4, 2016

@author: riaps
'''

import netifaces
import socket
from random import randint
from contextlib import closing
from riaps.utils.config import Config


def getNetworkInterfaces(nicName=None):
    '''
     Determine the IP address of  the network interfaces
     Return a tuple of list of global IP addresses, list of MAC addresses, and local IP address
     If the requested interface is found the list will contain the information for that interface only. 
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
                linkAddr = linkAddrs[0]['addr'].replace(':', '')
                macAddressList.append(linkAddr)
                if(nicName == ifName):
                    ipAddressList = [ipAddressList[-1]]
                    ifNameList = [ifName]
                    macAddressList = [macAddressList[-1]] 
                    break
    return (ipAddressList, macAddressList, ifNameList, local)

def is_valid_ipv4_address(address):
    ''' Determine if the argument is a valid IP address
    '''
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False
    return True


def get_unix_dns_ips():
    ''' Retrieve the IP address(es) of dns servers used by this host
    '''
    dns_ips = []

    with open('/etc/resolv.conf') as fp:
        for _cnt, line in enumerate(fp):
            columns = line.split()
            if len(columns) > 0 and columns[0] == 'nameserver':
                ip = columns[1:][0]
                if is_valid_ipv4_address(ip):
                    dns_ips.append(ip)
    return dns_ips


RANDOM_PORT_MIN = 49152
RANDOM_PORT_MAX = 65535


def get_random_port():
    '''
    Get a random open port
    '''
    while True:
        port = randint(RANDOM_PORT_MIN , RANDOM_PORT_MAX)
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            s.bind(('', port))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return s.getsockname()[1]

