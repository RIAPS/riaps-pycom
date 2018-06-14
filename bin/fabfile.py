#
# fabfile for RIAPS tasks
#

from fabric.api import *
from fabric.contrib.files import exists, append

# List of bbb hosts -- EDIT HERE --
import riaps_hosts      # This file must set env.hosts to a list of host names

# Standard riaps setup
env.password = 'riaps'
env.user = 'riaps'
env.sudo_password = 'riaps'
# Shell
env.shell = "/bin/bash -l -i -c"

# Transfer directories 
env.localPath = '/home/riaps/riaps/'    # Path local host
env.nodePath = '/home/riaps/'           # Path on target

env.riapsHome = '/usr/local/riaps'
env.riapsApps = '/home/riaps/riaps_apps'
env.riapsLib = '/opt/riaps/armhf/lib:/usr/local/lib'


# System Utilities
#--------------------
def getFile(fileName,localPrefix=''):
    """Transfer file from hosts (BBBs) to control host"""
    get(env.nodePath + fileName, env.localPath+localPrefix)

# If transferring to a RIAPS account directory, use_sudo=False. 
# If transferring to a system location, use_sudo=True
def putFile(fileName, localPrefix='', use_sudo=False):
    """Transfer file to hosts (BBBs) from control host"""
    put(env.localPath + localPrefix + fileName, env.nodePath + fileName, use_sudo)
    
# RIAPS packages
packages = [ 
            'riaps-externals-armhf', 
            'riaps-core-armhf', 
            'riaps-pycom-armhf', 
            'riaps-systemd-armhf',
            'riaps-timesync-armhf',  
            ]

# RIAPS update (from release)
@parallel
def update():
    """ Update RIAPS packages on target from official release"""
    sudo('apt-get update')
    global packages
    for pack in packages:
        sudo('apt-get install ' + pack + ' -y')
        run('echo "updated %s"' % (pack))

# RIAPS install (from local host) 
@parallel
def install():
    """Install RIAPS packages on target from development host"""
    global packages
    hostname = env.host_string
    for pack in packages:
        package = pack + '.deb'
        putFile(package)
        sudo('apt install ./'+ package + ' > riaps-install-' + hostname + '.log')
        run('echo "installed %s"' % (package))
        sudo('rm -f %s' %(package))
        getFile('riaps-install-' + hostname + '.log', 'logs/')
    

# Control RIAPS operation (manual control)
#------------------------------------------

# Check that all BBBs are communicating
# @parallel
def check():
    """test that hosts are communicating"""
    run('hostname && uname -a')

# Start the deplo on all hosts
@parallel
def start_deplo():
    """start deplo on hosts"""
    hostname = env.host_string
    command = ('sudo -E riaps_deplo >~/riaps-' + hostname + '.log 2>&1 &')
    run(command)

# Stop anything related to riaps on the hosts
@parallel
def stop():
    """stop RIAPS functions on hosts"""
    sudo('pkill -SIGKILL riaps')
    
    
# Stop anything related to riaps on the hosts - app_name
# EXTREMELY HEAVY HANDED: If run, you must restart riaps-deplo.service
@parallel
def kill(app_name):
    """kill RIAPS functions and application on hosts"""
    pgrepResult = run('pgrep \'riaps_\' -l')
    pgrepEntries = pgrepResult.rsplit('\n')
    processList = []
 
    for process in pgrepEntries:
        processList.append(process.split()[1])
 
    for process in processList:
        sudo('pkill -SIGKILL '+process,combine_stderr=True,warn_only=True)
 
    hostname = run('hostname')
    if hostname[0:3] == 'bbb':
        host_last_4 = hostname[-4:]
    # If it doesn't start with bbb, assume it is a development VM
    else:
        vm_mac = run('ip link show enp0s8 | awk \'/ether/ {print $2}\'')
        host_last_4 = vm_mac[-5:-3] + vm_mac[-2:]
 
    sudo('rm -R /home/riaps/riaps_apps/riaps-apps.lmdb/')
    sudo('rm -R /home/riaps/riaps_apps/'+app_name+'/')
    sudo('userdel ' + app_name.lower() + host_last_4)

# Halt the hosts
# Note: must be used prior to powering down the hosts
@parallel
def halt():
    """halt the hosts"""
    sudo('halt &')

# Reboot the hosts
@parallel
def reboot():
    """reboot the hosts"""
    sudo('reboot &')

# Launch the RIAPS controller on the control host
# Note: (1) RIAPS must be installed, (2) starts and stops the rpyc registry as well
@hosts('localhost')
def riaps():
    """launch RIAPS controller"""
    sudo ('systemctl stop riaps-rpyc-registry.service')
    local('(rpyc_registry.py &) && riaps_ctrl && pkill rpyc')

# Note on rpyc_registry: If the control host (dev vm) has a 2 or more network interfaces,
# the riaps_ctrl may bind itself to the wrong one -- this is an rpyc_registry issue.
# Workaround: disable all unused network interfaces on the control host.

@parallel
def getLogs():
    """ Get the main RIAPS log """
    hostname = env.host_string
    getFile('riaps-' + hostname + '.log','logs/')
    
# Time Synchronization
#----------------------
def getTime():
    """Compare clocks on hosts"""
    hostname = env.host_string
    run('date +%H.%M.%S.%N > riaps-time-' + hostname + '.log')
    getFile('riaps-time-' + hostname + '.log','logs/')

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
    """start deplo background service on hosts"""
    sudo('systemctl enable riaps-deplo.service')
    sudo('systemctl start riaps-deplo.service')
    
@parallel
def restartDeplo():
    """restart the deplo background service on hosts"""
    sudo('systemctl restart riaps-deplo.service')

@parallel
def stopDeplo():
    """stop deplo background service on hosts"""
    pgrepResult = run('pgrep \'riaps_\' -l')
    pgrepEntries = pgrepResult.rsplit('\n')
    processList = []
 
    for process in pgrepEntries:
        processList.append(process.split()[1])
 
    for process in processList:
        sudo('pkill -SIGKILL '+process,combine_stderr=True,warn_only=True)

    sudo('systemctl stop riaps-deplo.service')
    sudo('systemctl disable riaps-deplo.service')

# If using riaps-deplo.service, the log data is being recorded in a system journal.
# This function pulls that data from the system journal and places them in a log file
@parallel
def getDeploLogs():
    """create deployment log"""
    hostname = env.host_string
    sudo('journalctl -u riaps-deplo.service --since today > riaps-deplo-' + hostname + '.log')
    getFile('riaps-deplo-' + hostname + '.log','logs/')

# The system journal run continuously with no regard to login session. So to isolate testing data, the system journal can be cleared.
@parallel
def clearJournalLog():
    """clear system journal"""
    sudo('rm -rf  /run/log/journal/*')
    sudo('systemctl restart systemd-journald')

# Find IP address of primary network interface
import socket
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

# Setup hosts routing, if needed.  Configure to your system's setup
def configRouting():
    """Configure routing"""
    env.warn_only = True
    # ---- EDIT HERE ----
    hostIP = get_ip()
    # Provide appropriate IP address
    sudo('route add default gw ' + hostIP + 'dev eth0')




