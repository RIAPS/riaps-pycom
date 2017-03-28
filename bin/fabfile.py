#
# fabfile for RIAPS tasks
#

from fabric.api import *

# List of bbb hosts -- EDIT HERE --
env.hosts = ['bbb-ff98.local' , 'bbb-53b9.local' , 'bbb-1f82.local' , 'bbb-d5b5.local' ]
# ['192.168.0.101' , '192.168.0.103' , '192.168.0.105' , '192.168.0.106' ]
# ['bbb-2839.local','bbb-164c.local','bbb-e835.local','bbb-ef9f.local',
#             'bbb-d521.local','bbb-cdee.local','bbb-1180.local','bbb-e22d.local',
#             'bbb-feb5.local','bbb-4797.local','bbb-eb18.local','bbb-fea3.local',
#             'bbb-a0a6.local','bbb-923a.local','bbb-be53.local','bbb-da04.local',
#             'bbb-f913.local','bbb-1d35.local','bbb-e528.local','bbb-93bb.local',
#             'bbb-e7b8.local','bbb-23c6.local','bbb-f365.local','bbb-8be2.local',
#             'bbb-e7b9.local','bbb-da61.local','bbb-20fb.local','bbb-4930.local',
#             'bbb-7030.local','bbb-5df2.local','bbb-1610.local','bbb-da2e.local']    

# Standard riaps setup
env.password = 'riapspwd'
env.user = 'riaps'
# Shell
env.shell = "/bin/bash -l -i -c"

# Update pycom
# Note: localFilePath and filename should be configurable
def update_pycom():

    localFilePath = '~/Downloads/'                      # '~/RIAPS_updates/update_files/'
    nodePutPath = '/home/riaps/'
    filename = 'riaps-pycom_v0.3.3.tar.gz'              # 'riaps-pycom_v0.3.2.tar.gz'

    put(localFilePath + filename, nodePutPath + filename)
    run('tar xvzf ' + nodePutPath + filename)
    run('pip3 install ' + nodePutPath + 'riaps-pycom/src --user --process-dependency-links')
    run('rm ' + nodePutPath + filename)
    run('rm -R ' + nodePutPath + 'riaps-pycom')

# Update discovery
def update_discovery():    

    localFilePath = '~/RIAPS_updates/update_files/'
    nodePutPath = '/opt/riaps/armhf/'
    libPath = 'lib/'
    binPath = 'bin/'
    libname = 'libriaps.so'
    disconame = 'rdiscoveryd'

    put(localFilePath + libname, nodePutPath + libPath + libname)
    put(localFilePath + disconame, nodePutPath + binPath + disconame) 
    
# Start the deplo on all hosts
# Note: this will block the host's terminal (unless started in the background)
@parallel
def deplo():
    run('riaps_deplo >~/riaps.log')

# Stop anything related to riaps on the hosts
@parallel
def stop():
    run('pkill -SIGKILL riaps')

# Halt the hosts
# Note: must be used prior to powering down the hosts
@parallel
def halt():
    run('sudo halt')

# Reboot the hosts
@parallel
def reboot():
    run('sudo reboot')

# Launch the Gridlabd runner on the control host
@hosts('localhost')
def grunner():
    local('cd ~/grunner; python3 riaps_grunner.py')

# Launch the riaps controller on the control host
# Note: starts and stops the rpyc registry as well
@hosts('localhost')
def riaps():
    local('(rpyc_registry.py &) && riaps_ctrl && pkill rpyc')


# Note on rpyc_registry: If the control host (dev vm) has a 2 or more network interfaces,
# the riaps_ctrl may bind itself to the wrong one -- this is an rpyc_registry issue.
# Workaround: disable all unused network interfaces on the control host.  
