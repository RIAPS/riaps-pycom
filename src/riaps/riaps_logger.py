#!/usr/bin/python3
'''
Top level script to start the framework log server

Created on Sep 6, 2022

Arguments
-p (or --platform) PLATFORM : The ip address and port for the platform log server. e.g., -p 10.0.0.1 9020
-a (or --app) APP : The ip address and port for the app log server. e.g., -a 10.0.0.1 12345
@author: riaps
'''

import riaps.logger.main

if __name__ == '__main__':
    riaps.logger.main.main()

    