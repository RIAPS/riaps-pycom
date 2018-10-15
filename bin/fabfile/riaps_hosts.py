# riaps_hosts.py - Configuration for RIAPS hosts
# imported into the fab file
# Edit this file to match your configuration
from fabric.api import env

# If a no commandline roles or hosts are passed (i.e. -R or -H), only then use listed hosts
# Allows for passing of individual hosts or roles on which to run tasks
if not env.roles and not env.hosts:
    # List of roles and hosts -- EDIT HERE --
    env.hosts = ['192.168.1.2','192.168.1.3','ubuntu.local','bbb-ef9e.local']
