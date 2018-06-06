# Fabric commands for managing RIAPS installs and applications
from . import deplo
from .util import run, sudo, putFile, getFile
from fabric.api import env, task

# RIAPS packages
packages = [ 
            'riaps-externals-armhf', 
            'riaps-core-armhf', 
            'riaps-pycom-armhf', 
            'riaps-systemd-armhf',
            'riaps-timesync-armhf',  
            ]

# RIAPS update (from release)
@task
def update():
    """ Update RIAPS packages on target from official release"""
    sudo('apt-get update')
    global packages
    for pack in packages:
        sudo('apt-get install ' + pack + ' -y')
        run('echo "updated %s"' % (pack))

# RIAPS install (from local host) 
@task
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
    
@task
def uninstall():
    global packages
    for pack in packages:
        package = pack + '.deb'
        sudo("apt-get remove " + pack)
        sudo("dpkg -r " + package)

def killApp(app_name, hostname):
    if hostname[0:3] == 'bbb':
        host_last_4 = hostname[-4:]
    # If it doesn't start with bbb, assume it is a development VM
    else:
        vm_mac = run('ip link show enp0s8 | awk \'/ether/ {print $2}\'')
        host_last_4 = vm_mac[-5:-3] + vm_mac[-2:]
 
    sudo('rm -R /home/riaps/riaps_apps/riaps-apps.lmdb/ || true')
    sudo('rm -R /home/riaps/riaps_apps/'+app_name+'/')
    sudo('userdel ' + app_name.lower() + host_last_4)

# Stop anything related to riaps on the hosts - app_name
@task
def kill(app_name):
    """kill RIAPS functions and application on hosts"""
    deplo.stop()
    hostname = run('hostname')
    killApp(app_name, hostname)

@task
def killAll():
    """kill RIAPS functions and all application on hosts"""
    deplo.stop()
    lsResult = run('\ls ' + env.riapsApps) # \ls bypasses alias to ls with color formatting
    hostname = run('hostname')
    apps = lsResult.split()
    for app in apps:
        if app != 'riaps-apps.lmdb':
            killApp(app, hostname)

# If using riaps-deplo.service, the log data is being recorded in a system journal.
# This function pulls that data from the system journal and places them in a log file
@task
def getLogs():
    """create deployment log"""
    hostname = env.host_string
    sudo('journalctl -u riaps-deplo.service --since today > riaps-deplo-' + hostname + '.log')
    getFile('riaps-deplo-' + hostname + '.log','logs/riaps-deplo-' + hostname + '.log')