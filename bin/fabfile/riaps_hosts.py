# riaps_hosts.py - Configuration for RIAPS hosts
# imported into the fab file
# Edit this file to match your configuration
from fabric.api import env

# If a no commandline roles or hosts are passed (i.e. -R or -H), only then use listed hosts
# Allows for passing of individual hosts or roles on which to run tasks
if not env.roles and not env.hosts:
    # List of roles and hosts -- EDIT HERE --
    env.hosts = ['bbb-2839.local','bbb-164c.local','bbb-e835.local','bbb-ef9f.local',
                  'bbb-d521.local','bbb-cdee.local','bbb-1180.local','bbb-e22d.local',
                  'bbb-feb5.local','bbb-4797.local','bbb-eb18.local','bbb-fea3.local',
                  'bbb-a0a6.local','bbb-923a.local','bbb-be53.local','bbb-da04.local',
                  'bbb-f913.local','bbb-1d35.local','bbb-e528.local','bbb-93bb.local',
                  'bbb-e7b8.local','bbb-23c6.local','bbb-f365.local','bbb-8be2.local',
                  'bbb-e7b9.local','bbb-da61.local','bbb-20fb.local','bbb-4930.local',
                  'bbb-7030.local','bbb-5df2.local','bbb-1610.local','bbb-da2e.local']