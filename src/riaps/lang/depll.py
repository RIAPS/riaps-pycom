#!/usr/bin/python3
'''
Top-level script to start the deployment language processor ('depl')
Created on Oct 15, 2016

Arguments:
  model        : Name of deployment model file to be processed 

@author: riaps
'''
from riaps.lang.depl import main

if __name__ == '__main__':
    main(True)