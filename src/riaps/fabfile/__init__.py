#
# fabfile for RIAPS tasks
#
from fabric.api import env
from fabric.utils import abort
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
env.parallel = True             # Changes default behavior to parallel
env.use_ssh_config = False      # Tells fabric to use the user's ssh config
env.disable_known_hosts = True  # Ignore warnings about known_hosts
env.skip_bad_hosts = True       # Skip bad hosts
env.abort_on_prompts = True     # Abort on prompts

# Standard riaps setup
env.user = 'riaps'

# File transfer directories
env.localPath = os.getcwd() + '/'   # Path on localhost
env.nodePath = '/home/riaps/'       # Path on target

# RIAPS directories
env.riapsHome = os.getenv('RIAPSHOME')
if env.riapsHome  == None:
        print("RIAPS Configuration - RIAPSHOME is not set, using ./")
        env.riapsHome = './'

if 'riapsApps' not in env:
    env.riapsApps = os.getenv('RIAPSAPPS')
    if env.riapsApps  == None:
        print("RIAPS Configuration - RIAPSAPPS  is not set, using /home/riaps/riaps_apps")
        env.riapsApps = '/home/riaps/riaps_apps'

env.riapsLib = '/usr/local/lib'

# Use RIAPS SSH key
#env.key_filename = os.path.join(env.riapsHome,"keys/" + str(const.ctrlPrivateKey))
validate = True if 'validate' in env else False

# If no command line roles or hosts are passed (i.e. -R or -H), only then use listed hosts
# Allows for passing of individual hosts or roles on which to run tasks
env.roledefs = None
if 'hostsFile' in env:
    if os.path.isfile(env.hostsFile):
        sys.hosts(env.hostsFile,validate)
    else:
        print("Given hosts file \"%s\" does not exist, exiting..." % env.hostsFile)
# elif not env.roles and not env.hosts and not [s for s in env.tasks if 'sys.hosts' in s]:
else:
    # Task is not sys.hosts
    riaps_conf = os.path.join(env.riapsHome,'etc/riaps-hosts.conf')
    sys.hosts(riaps_conf,validate)

if env.roledefs is None:
    abort('Bad configuration/hosts/roles')
#
