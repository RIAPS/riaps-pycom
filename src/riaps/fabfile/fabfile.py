#!/usr/bin/python3
'''
Top level script to start fabric file for handling multiple RIAPS nodes setup

Created on March 6, 2019

Arguments:
    - ``fabcmd``:    fabric command desired

    optional arguments:
    - ``-H | --hosts hostnames``:  list of hostnames (comma separated)
    - ``-R | --roles rolenames``:  list of roles (comma separated)
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
import site
import subprocess

def bash(cmd):
    print("=== "+cmd)
    subprocess.run(shlex.split(cmd))

def main():
    parser = argparse.ArgumentParser()
    # Fabric command
    parser.add_argument("fabcmd", help="fabric command")
    # List of hosts to use (instead of system configured file)
    parser.add_argument("-H", "--hosts", default="", help="list of hosts, comma separated")   
    # List of roles to use 
    parser.add_argument("-R", "--roles", default="", help="list of roles, comma separated")   
    parser.add_argument("-f", dest='hostsFile', help="absolute path customs hosts file")
    parser.add_argument("-i", dest='privateKeyPath', help="relative or absolute path to specific private key")
    parser.add_argument("-v", "--validate", action='store_const', const=True, help="validate host names")
    args = parser.parse_args()
    
    fcmd = "fab"
    fflag = "-f"
    fpaths = [p + "/riaps/" for p in site.getsitepackages()] + [os.getenv('RIAPSHOME')]
    fhosts = ("--hosts=" + args.hosts) if args.hosts else ""
    froles = ("--roles=" + args.roles) if args.roles else ""
    fhostsFile = ("--set hostsFile=" + args.hostsFile) if args.hostsFile else ""
    fident = "-i "+ args.privateKeyPath \
                        if args.privateKeyPath and os.path.isfile(args.privateKeyPath) else ""
                                                                            
    #    sys.path.append(os.getcwd())   # Ensure load_module works from current directory
    fvalidate = "--set validate" if args.validate else ""
    fpath = None
    for p in fpaths:
        if p is None: continue
        fp = os.path.join(p,"fabfile","")
        if os.path.isdir(fp):
            fpath = fp; break  
    if fpath is not None:
        # if args.hosts:
        #     # fab -f FABFILE FABCMD --hosts=HOSTS --roles=ROLES -i IDENT 
        #     cmd = str.join(' ',(fcmd, fflag, fpath, args.fabcmd, fhosts, fident))
        # elif args.hostsFile:
        #     # fab --set hostsFile=HOSTS -f FABFILE FABCMD -i IDENT
        #     cmd = str.join(' ',(fcmd, fset, fenvVar, fflag, fpath, args.fabcmd, fident))
        # else:
        #     # fab -f FABFILE FABCMD -i IDENT 
        #     cmd = str.join(' ',(fcmd, fflag, fpath, args.fabcmd, fident))
        
        # fab -f FABFILE FABCMD [--set hostsFile=HOSTSFILE] [--hosts=HOSTS] [--roles==ROLES] [-i
        cmd = str.join(' ',(fcmd,fflag,fpath,args.fabcmd, fhostsFile, fhosts, froles, fvalidate, fident))
        bash(cmd)
    else:
        print('RIAPS fabfile is missing')


if __name__ == '__main__':
    main()