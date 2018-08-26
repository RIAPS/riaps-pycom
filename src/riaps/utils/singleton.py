'''
Created on Jul 23, 2018

@author: riaps
'''
import socket
import os

def singleton(process_name,suffix=None):
    ''' 
    Enforce the caller process is a singleton
    '''
    # Without holding a reference to our socket somewhere it gets garbage
    # collected when the function exits
    singleton._name = process_name if suffix == None else process_name + '_' + str(suffix)
    singleton._lock_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

    try:
        singleton._lock_socket.bind('\0' + singleton._name)
        #print 'I got the lock'
    except socket.error:
        print ("%s is already running - exiting" % (process_name))
        os._exit(0)