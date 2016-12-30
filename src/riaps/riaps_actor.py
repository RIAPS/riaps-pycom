#!/usr/bin/python3
'''
Top level script to start the run-time system: an actor
Created on Oct 15, 2016

Arguments
  model    : Name of processed (JSON) model file
  actor    : Name of specific actor from the model this process will run

@author: riaps
'''
import riaps.run.main

if __name__ == '__main__':
    riaps.run.main.main()
    
