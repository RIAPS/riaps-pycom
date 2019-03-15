#
# fabfile for RIAPS tasks
#
from fabric.api import env
from riaps.consts.defs import *
import os

# Universal utilities
from . import sys

# Riaps utilities
from . import riaps
from . import deplo
from . import time


# Standard fabric configuration
env.shell = "/bin/bash -l -i -c"
env.parallel = True            # Changes default behavior to parallel
env.use_ssh_config = False     # Tells fabric to use the user's ssh config
env.disable_known_hosts = True # Ignore warnings about known_hosts

# Standard riaps setup
env.user = 'riaps'

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
#env.key_filename = os.path.join(env.riapsHome,"keys/" + str(const.ctrlPrivateKey))

# If a no commandline roles or hosts are passed (i.e. -R or -H), only then use listed hosts
# Allows for passing of individual hosts or roles on which to run tasks
if 'hostsFile' in env:
    if os.path.isfile(env.hostsFile):
        sys.hosts(env.hostsFile)
    else:
        print("Given hosts file \"%s\" does not exist, exiting..." % env.hostsFile)
elif not env.roles and not env.hosts and not [s for s in env.tasks if 'sys.hosts' in s]:
    riaps_conf = os.path.join(env.riapsHome,'etc/riaps-hosts.conf')
    sys.hosts(riaps_conf)
