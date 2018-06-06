#
# fabfile for RIAPS tasks
#
from fabric.api import env

# Import user configuration file
from . import fab_config

# Universal utilities
from . import sys
from . import fs

# Riaps utilities
from . import riaps
from . import deplo
from . import tsman

# Standard fabric configuration
env.shell = "/bin/bash -l -i -c"
env.parallel = True            # Changes default behavior to parallel
env.use_ssh_config = True      # Tells fabric to use the user's ssh config
env.disable_known_hosts = True # Ignore warnings about known_hosts