'''
Top-level script to start the discovery service (disco)
Created on Oct 20, 2016

Arguments:
 --database DatabaseLocation
 DatabaseLocation is a string used to contact the shared database used to store and lookup port registrations.
 For redis, it is hostName:portNumber pair
s
@author: riaps
'''
import riaps.discd.main

if __name__ == '__main__':
    riaps.discd.main.main()
    
