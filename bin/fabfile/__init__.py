#
# fabfile for RIAPS tasks
#
from fabric.api import env
from os import getcwd

# Import user hosts file
from . import riaps_hosts

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
env.localPath = getcwd()       # Path on localhost
env.nodePath = '/home/riaps/'  # Path on target

# RIAPS directories
env.riapsHome = '/usr/local/riaps'
env.riapsApps = '/home/riaps/riaps_apps'
env.riapsLib = '/opt/riaps/armhf/lib:/usr/local/lib'
