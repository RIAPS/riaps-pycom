#!/usr/bin/python3
'''
Top level script to start the controller node 
It assumes that an rpyc registry is running

Created on Nov 4, 2016

Arguments
-p (or --port) PORT : Port on which the the RIAPSCONTROL service is started on and registered with.

@author: riaps
'''

import riaps.ctrl.main

if __name__ == '__main__':
    riaps.ctrl.main.main()
    