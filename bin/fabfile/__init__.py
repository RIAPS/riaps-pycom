#
# fabfile for RIAPS tasks
#
from fabric.api import env
from riaps.consts.defs import *
import os,csv,itertools,configparser

# Universal utilities
from . import sys

# Riaps utilities
from . import riaps
from . import deplo
from . import time

# Standard fabric configuration
env.shell = "/bin/bash -l -i -c"
env.parallel = True            # Changes default behavior to parallel
env.use_ssh_config = True      # Tells fabric to use the user's ssh config
env.disable_known_hosts = True # Ignore warnings about known_hosts

# Standard riaps setup
env.password = 'riaps'
env.user = 'riaps'
env.sudo_password = 'riaps'

# File transfer directories 
env.localPath = os.getcwd() + '/' # Path on localhost
env.nodePath = '/home/riaps/'  # Path on target

# RIAPS directories
env.riapsHome = riaps_folder = os.getenv('RIAPSHOME')
if riaps_folder == None:
        print("RIAPS Configuration - RIAPSHOME is not set, using ./")
        env.riapsHome = './'
env.riapsApps = '/home/riaps/riaps_apps'
env.riapsLib = '/opt/riaps/armhf/lib:/usr/local/lib'

# Use RIAPS SSH key
env.key_filename = os.path.join(env.riapsHome,"keys/" + str(const.ctrlPrivateKey))

# If a no commandline roles or hosts are passed (i.e. -R or -H), only then use listed hosts
# Allows for passing of individual hosts or roles on which to run tasks
if not env.roles and not env.hosts:
    riaps_conf = os.path.join(env.riapsHome,'etc/riaps-hosts.conf')
    try:
        config = configparser.ConfigParser()
        settings = config.read(riaps_conf)
    except Exception as e:
        print(' Hosts configuration file %s has a problem: %s.' % (riaps_conf, str(e)))
        pass

    riaps_section = 'RIAPS'
    if settings == [] or not config.has_section(riaps_section):
        print('System configuration file %s not found or invalid file.' % (riaps_conf))

    found = False
    for item in config.items(riaps_section):
        key,arg = item
        if key == 'hosts':
            found = True
            # Parse hosts config as multi line csv
            lines = arg.replace('\'','"').split('\n')
            print("lines=%s"%lines)
            parser = csv.reader(lines) # Parse commas and quotations
            hosts = list(itertools.chain.from_iterable(parser)) # Combine lines
            env.hosts = list(filter(None, hosts)) # Filter out any empty strings
        else:
            print("Unrecognized key in %s: %s" % (riaps_conf,key))  
        if not found:
            print('Failed to find "hosts" key in hosts file %s' % riaps_conf)