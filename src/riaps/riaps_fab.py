#!/usr/bin/python3
'''
Top level script to start fabric file for handling multiple RIAPS nodes setup

Created on March 6, 2019

Arguments:
    - ``fabcmd``:    fabric command desired
    - ``--list``:    list available commands

    optional arguments:
        Argument(names=('role','r'), help = "RIAPS role name to run command for",default="remote"),
        Argument(names=('v'), kind=bool, help = "Show remote output"),
        Argument(names=('host','H'),help = "Run command on host (repeatable)",kind=list),
        Argument(name='hostfile', help = "Path to riaps-hosts.conf file"),
        Argument(names=('i'),help = "SSH Private Key to use")]

If specific hostnames are not given, the command will be called for all hosts
listed in /usr/local/riaps/etc/riaps-hosts.conf

@author: riaps
'''

import riaps.rfab.main

if __name__ == '__main__':
    riaps.rfab.main.main()
    
