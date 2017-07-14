#
# fabfile for RIAPS tasks
#

from fabric.api import *
from fabric.contrib.files import exists, append


# ---- START OF EDIT HERE ----
# List of bbb hosts
# BBBs can be addressed by their IP address or the hostname.local (found at the command prompt on the BBB)
env.hosts = ['192.168.0.101', 'bbb-ff98.local']
# ----  END OF EDIT HERE  ----


# Standard riaps setup
env.password = 'riaps'
env.user = 'riaps'
env.sudo_password = 'riaps'
# Shell
env.shell = "/bin/bash -l -i -c"


# Functions
# Note: localFilePath, nodeGetPath, nodePutPath, localFilename, nodeFilename, and filename should be configurable

# Setup Utilities
#-----------------
# Good utility to make sure all BBBs are communicating
def hello_hosts():
    """test that hosts are communicating"""
    run('echo HELLO')

# RIAPS Platform Update
# First download the latest riaps-release.tar.gz from https://github.com/RIAPS/riaps-integration/releases
def update_riaps():
    """update RIAPS platform on hosts"""
    
    sudo('apt-get update')
    sudo('apt-get install riaps-externals-armhf -y')
    run('echo "installed externals"')
    sudo('apt-get install riaps-core-armhf -y')
    run('echo "installed core"')
    sudo('apt-get install riaps-pycom-armhf -y')
    run('echo "installed pycom"')
    sudo('apt-get install riaps-systemd-armhf -y') 
    run('echo "installed services"')
    sudo('apt-get install riaps-timesync-armhf -y') 
    run('echo "installed timesync"')
    

# Control RIAPS operation (manual control)
#------------------------------------------
# Start the deplo on all hosts
# Note: this will block the host's terminal (unless started in the background)
# Indicate the host IP address where 'riaps_ctrl' is running
@parallel
def deplo():
    """start deplo on hosts"""
    run('riaps_deplo >~/riaps.log')

# Stop anything related to riaps on the hosts
@parallel
def stop():
    """stop RIAPS functions on hosts"""
    run('pkill -SIGKILL riaps')

# Halt the hosts
# Note: must be used prior to powering down the hosts
@parallel
def halt():
    """halt the hosts"""
    sudo('halt')

# Reboot the hosts
@parallel
def reboot():
    """reboot the hosts"""
    sudo('reboot')

# Launch the riaps controller on the control host
# Note: starts and stops the rpyc registry as well
@hosts('localhost')
def riaps():
    """launch RIAPS controller"""
    local('(rpyc_registry.py &) && riaps_ctrl && pkill rpyc')

# Note on rpyc_registry: If the control host (dev vm) has a 2 or more network interfaces,
# the riaps_ctrl may bind itself to the wrong one -- this is an rpyc_registry issue.
# Workaround: disable all unused network interfaces on the control host.


# Time Synchronization
#----------------------
def timeStamp():
    """Compare clocks on hosts"""
    run('date +%H.%M.%S.%N > timestamp.txt')

@hosts('localhost')
def checkPTP():
    """ check to see if ptp is running on control host"""
    local('ps -ef | grep ptp')


# Working with RIAPS Services (automation control)
#-------------------------------------------------
# RIAPS services could be started and stopped when configuring a more automated approach
# At this time, these services are experimental (06/2017)

# The deployment service requires the discovery service to be running
# Each of these services are configured to restart if they fail. So to truly stop them, the
# service must be disabled
@parallel
def startDeplo():
    """start deplo.service"""
    sudo('systemctl enable riaps-disco.service')
    sudo('systemctl start riaps-disco.service')
    sudo('systemctl enable riaps-deplo.service')
    sudo('systemctl start riaps-deplo.service')

@parallel
def stopDeplo():
    """stop deplo.service"""
    sudo('systemctl stop riaps-disco.service')
    sudo('systemctl disable riaps-disco.service')
    sudo('systemctl stop riaps-deplo.service')
    sudo('systemctl disable riaps-deplo.service')

# If using riaps-deplo.service, the log data is being recorded in a system journal.
# This function pulls that data from the system journal and places them in a log file
@parallel
def createDeployLogs():
    """create deployment log"""
    host_ID = env.host_string
    sudo('journalctl -u riaps-deplo.service --since today > /home/riaps/deploy_' + host_ID + '.log')

# The system journal run continuously with no regard to login session. So to isolate testing data, the system journal can be cleared.
@parallel
def clear_journal_log():
    """clear system journal"""
    sudo('rm -rf  /run/log/journal/*')
    sudo('systemctl restart systemd-journald')


# System Utilities
#--------------------
def fileTransferFrom():
    """Transfer files from hosts (BBBs) to control host"""
    localFilePath = '/home/riaps/Downloads/'
    nodeGetPath = '/home/riaps/'
    filename = 'hostfile'

    get(nodeGetPath + filename, localFilePath)

# If transferring to a riaps account directory, use_sudo=False. If transferring to a system location, use_sudo=True
def fileTransferTo():
    """Transfer files to hosts (BBBs) from control host"""
    localFilePath = '/home/riaps/Downloads/'
    nodePutPath = '/home/riaps/'
    localFilename = 'controlhost_filename'
    nodeFilename = 'host_filename'

    put(localFilePath + localFilename, nodePutPath + nodeFilename, use_sudo=False)

# Setup hosts routing, if needed.  Configure to your system's setup
def config_routing():
    """Configure routing"""
    env.warn_only = True
    # ---- EDIT HERE ----
    # Provide appropriate IP address
    sudo('route add default gw 10.1.1.249 dev eth0')



