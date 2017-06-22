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
    """update RIAPS platform"""
    localFilePath = '/home/riaps/Downloads/'
    nodePutPath = '/home/riaps/'
    filename = 'riaps-release.tar.gz'

    put(localFilePath + filename, nodePutPath + filename)
    run('tar xvzf ' + nodePutPath + filename)
    run('sudo dpkg -i riaps-release/riaps-externals-armhf.deb')
    run('echo "installed externals"')
    run('sudo dpkg -i riaps-release/riaps-core-armhf.deb')
    run('echo "installed core"')
    run('sudo dpkg -i riaps-release/riaps-pycom-armhf.deb')
    run('echo "installed pycom"')
    run('sudo dpkg -i riaps-release/riaps-systemd-armhf.deb') 
    run('echo "installed services"')
    run('sudo dpkg -i riaps-release/riaps-timesync-armhf.deb') 
    run('echo "installed timesync"')
    run('rm ' + nodePutPath + filename)

    run('rm -R ' + nodePutPath + 'riaps-release')


# Control RIAPS operation (manual control)
#------------------------------------------
# Start the deplo on all hosts
# Note: this will block the host's terminal (unless started in the background)
# Indicate the host IP address where 'riaps_ctrl' is running
@parallel
def deplo():
    """start deplo on hosts"""
    # ---- START OF EDIT HERE ----
    run('riaps_deplo -n 192.168.1.103 >~/riaps.log')
    # ----  END OF EDIT HERE  ----

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
    run('sudo halt')

# Reboot the hosts
@parallel
def reboot():
    """reboot the hosts"""
    run('sudo reboot')

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
    sudo('systemctl enable disco.service')
    sudo('systemctl start disco.service')
    sudo('systemctl enable deplo.service')
    sudo('systemctl start deplo.service')

@parallel
def stopDeplo():
    """stop deplo.service"""
    sudo('systemctl stop disco.service')
    sudo('systemctl disable disco.service')
    sudo('systemctl stop deplo.service')
    sudo('systemctl disable deplo.service')

# If using deplo.service, the log data is being recorded in a system journal.
# This function pulls that data from the system journal and places them in a log file
@parallel
def createDeployLogs():
    """create deployment log"""
    host_ID = env.host_string
    run('sudo journalctl -u deplo.service --since today > /home/riaps/deploy_' + host_ID + '.log')

# The system journal run continuously with no regard to login session. So to isolate testing data, the system journal can be cleared.
@parallel
def clear_journal_log():
    """clear system journal"""
    run('sudo rm -rf  /run/log/journal/*')
    run('sudo systemctl restart systemd-journald')


# System Utilities
#--------------------
def fileTransferFrom():
    """Transfer files from hosts (BBBs) to control host"""
    localFilePath = '/home/riaps/Download/'
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
    run('sudo route add default gw 10.1.1.249 dev eth0')

def noPass():
    """Create riaps file in sudoers directory and allow riaps to sudo with no password"""
    sudo('cd /etc/sudoers.d && echo \'%riaps ALL=NOPASSWD: ALL\' >riaps')

