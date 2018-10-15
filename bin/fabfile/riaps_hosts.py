# riaps_hosts.py - Configuration for RIAPS hosts which is imported into __init__.py
from fabric.api import env

# If a no commandline roles or hosts are passed (i.e. -R or -H), only then use listed hosts
# Allows for passing of individual hosts or roles on which to run tasks
if not env.roles and not env.hosts:
    
    # ---- START OF EDIT HERE ----
    # List of bbb hosts
    # BBBs can be addressed by their IP address or the hostname.local (found at the command prompt on the BBB)
    env.hosts = ['192.168.1.2','192.168.1.3','ubuntu.local','bbb-ef9e.local']
    # ----  END OF EDIT HERE  ----
