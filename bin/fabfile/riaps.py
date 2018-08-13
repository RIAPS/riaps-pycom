# Fabric commands for managing RIAPS installs and applications
from . import deplo
from .sys import run, sudo, put, get, arch
from fabric.api import env, task, hosts, local

# Prevent namespace errors by explicitly defining which tasks belong to this file
__all__ = ['update','updateKey','install','uninstall','kill','getLogs','setup_cython', 'ctrl', 'configRouting']

# RIAPS packages
packages = [ 
            'riaps-externals-',
            'riaps-core-',
            'riaps-pycom-',
            'riaps-systemd-',
            'riaps-timesync-'
            ]

# RIAPS update (from release)
@task
def update():
    """Update RIAPS packages from official release"""
    sudo('apt-get update')
    architecture = arch()
    global packages
    for pack in packages:
        package = pack + architecture
        sudo('apt-get install ' + package + ' -y')

@task
def updateKey():
    """Update RIAPS apt key"""
    sudo('wget -qO - https://riaps.isis.vanderbilt.edu/keys/riapspublic.key | apt-key add -')

# RIAPS install (from local host) 
@task
def install():
    """Install RIAPS packages from development host"""
    global packages
    hostname = env.host_string
    architecture = arch()
    for pack in packages:
        package = pack + architecture + '.deb'
        put(package)
        sudo('dpkg -i '+ package + ' > riaps-install-' + hostname + '-' + package + '.log')
        sudo('rm -f %s' %(package))
        get('riaps-install-' + hostname + '-' + package + '.log', 'logs/')

@task
def uninstall():
    """Uninstall all RIAPS packages"""
    global packages
    architecture = arch()
    for pack in packages:
        package = pack + architecture
        sudo("apt remove " + package)

@task
def kill():
    """Kill all RIAPS functions and application on hosts"""
    deplo.stop()

    pgrepResult = run('pgrep \'riaps_\' -l')
    pgrepEntries = pgrepResult.rsplit('\n')
    processList = []
 
    for process in pgrepEntries:
        if process != "":
            processList.append(process.split()[1])
 
    for process in processList:
        sudo('pkill -SIGKILL '+process)

    hostname = run('hostname')
    if hostname[0:3] == 'bbb':
        host_last_4 = hostname[-4:]
    # If it doesn't start with bbb, assume it is a development VM
    else:
        vm_mac = run('ip link show enp0s8 | awk \'/ether/ {print $2}\'')
        host_last_4 = vm_mac[-5:-3] + vm_mac[-2:]
 
    apps = run('\ls ' + env.riapsApps).split() # \ls bypasses alias to ls with color formatting
    for app in apps:
        sudo('rm -R /home/riaps/riaps_apps/'+app+'/')
        if app != 'riaps-apps.lmdb':
            sudo('userdel ' + app.lower() + host_last_4)

# If using riaps-deplo.service, the log data is being recorded in a system journal.
# This function pulls that data from the system journal and places them in a log file
@task
def getLogs():
    """Get deployment log"""
    hostname = env.host_string
    sudo('journalctl -u riaps-deplo.service --since today > riaps-deplo-' + hostname + '.log')
    get('riaps-deplo-' + hostname + '.log','logs/riaps-deplo-' + hostname + '.log')

@task
def setup_cython():
    """Fix 'Debugger speedups using cython not found' warnings"""
    sudo('wget https://raw.githubusercontent.com/fabioz/PyDev.Debugger/master/setup_cython.py -P /usr/local/lib/python3.5/dist-packages/')
    sudo('python3 /usr/local/lib/python3.5/dist-packages/setup_cython.py build_ext --inplace')

@task
@hosts('localhost')
def ctrl():
    """launch RIAPS controller"""
    local('riaps_ctrl')

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
@task
def configRouting():
    """Configure routing"""
    env.warn_only = True
    # ---- EDIT HERE ----
    hostIP = get_ip()
    # Provide appropriate IP address
    sudo('route add default gw ' + hostIP + 'dev eth0')
