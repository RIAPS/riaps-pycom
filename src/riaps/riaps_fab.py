#!/usr/bin/python3
'''
Top level script to start fabric file for handling multiple BBB setup

Created on March 6, 2019

Arguments:
    - ``fabcmd``:    fabric command desired

    optional arguments:
    - ``-H | --hosts hostnames``:  list of hostnames (comma separated)
    - ``-f hostfilename``       :  absolute path to local host file
    - ``-i ssh private key``    :  relative or absolute path to specific private key

If specific hostnames are not given, the command will be called for all hosts
listed in /usr/local/riaps/etc/riaps_hosts.conf

@author: riaps
'''

import os
import sys
import shlex
import argparse
import subprocess

def bash(cmd):
    print("=== "+cmd)
    subprocess.run(shlex.split(cmd))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("fabcmd", help="fabric command")             # Desired fabric command
    parser.add_argument("-H", "--hosts", default="", help="list of hostnames, comma separated")    # List of hostnames to used instead of system configured file
    parser.add_argument("-f", dest='hostsFile', help="absolute path to user defined host file")
    parser.add_argument("-i", dest='privateKeyPath', help="relative or absolute path to specific private key")
    args = parser.parse_args()

    fcmd = "fab"
    fflag = "-f"
    fpaths = ["/usr/local/lib/python3.6/dist-packages/riaps/fabfile/",os.getenv('RIAPSHOME')+"/fabfile/"]
    fhost = "-H"
    fident = ""
    fset = "--set"
    if args.hostsFile is not None:
        fenvVar = "hostsFile="+args.hostsFile

    if args.privateKeyPath:
        if os.path.isfile(args.privateKeyPath):
            fident = "-i "+args.privateKeyPath
        else:
            print("Given private key does not exist, exiting...")
            sys.exit(-1)

    #    sys.path.append(os.getcwd())   # Ensure load_module works from current directory
    fpath = None
    for p in fpaths:
        if os.path.isdir(p):
            fpath = p; break
    if fpath is not None:
        if args.hosts:
            cmd = str.join(' ',(fcmd, fflag, fpath, args.fabcmd, fhost, args.hosts, fident))
        elif args.hostsFile:
            cmd = str.join(' ',(fcmd, fset, fenvVar, fflag, fpath, args.fabcmd, fident))
        else:
            cmd = str.join(' ',(fcmd, fflag, fpath, args.fabcmd, fident))
        bash(cmd)
    else:
        print('RIAPS fabfile is not installed, please update the riaps-pycom installation.')
