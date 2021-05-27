# Fabric commands for managing RIAPS installs and applications
from . import deplo
from .sys import run, sudo, put, get, arch
from fabric.api import env, task, hosts, local, execute
from fabric.contrib.files import sed
import os
from riaps.consts.defs import *

# Prevent namespace errors by explicitly defining which tasks belong to this file
__all__ = ['update','updateRemoteNodeKey','updateAptKey','install','uninstall','kill','updateConfig','updateLogConfig','getLogs','ctrl', 'configRouting', 'securityOff', 'securityOn']

# RIAPS packages
packages = [
            'riaps-externals-',
            'riaps-core-',
            'riaps-pycom-',
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
def updateRemoteNodeKey():
    """Rekey the remote RIAPS nodes with new generated keys"""
    etc_key_path = "/etc/riaps/"
    ssh_key_path = "/home/riaps/.ssh/"
    ssh_pubkey_name = os.path.join(ssh_key_path, str(const.ctrlPublicKey))
    ssh_privatekey_name = os.path.join(ssh_key_path, str(const.ctrlPrivateKey))
    ssh_cert_name = os.path.join(ssh_key_path, str(const.ctrlCertificate))
    ssh_zmqcert_name = os.path.join(ssh_key_path, str(const.zmqCertificate))
    riaps_pubkey_name = os.path.join(etc_key_path, str(const.ctrlPublicKey))
    riaps_privatekey_name = os.path.join(etc_key_path, str(const.ctrlPrivateKey))
    riaps_cert_name = os.path.join(etc_key_path, str(const.ctrlCertificate))
    riaps_zmqcert_name = os.path.join(etc_key_path, str(const.zmqCertificate))

    put(ssh_privatekey_name,'.ssh')
    sudo('cp ' + ssh_privatekey_name + ' ' + riaps_privatekey_name)
    sudo('chown root:riaps ' + riaps_privatekey_name)
    sudo('chmod 440 ' + riaps_privatekey_name)

    #create public key from private key to get openSSH formatting
    run('chmod 400 ' + ssh_privatekey_name)
    sudo('ssh-keygen -y -f ' + ssh_privatekey_name + ' > /home/riaps/.ssh/authorized_keys')
    sudo('cp /home/riaps/.ssh/authorized_keys ' + riaps_pubkey_name)
    sudo('chown root:riaps ' + riaps_pubkey_name)
    sudo('chmod 440 ' + riaps_pubkey_name)
    sudo('rm ' + ssh_privatekey_name)

    put(ssh_cert_name,'.ssh')
    sudo('cp ' + ssh_cert_name + ' ' + riaps_cert_name)
    sudo('chown root:riaps ' + riaps_cert_name)
    sudo('chmod 440 ' + riaps_cert_name)
    run('rm ' + ssh_cert_name)

    put(ssh_zmqcert_name,'.ssh')
    sudo('cp ' + ssh_zmqcert_name + ' ' + riaps_zmqcert_name)
    sudo('chown root:riaps ' + riaps_zmqcert_name)
    sudo('chmod 444 ' + riaps_zmqcert_name)
    run('rm ' + ssh_zmqcert_name)

    sudo('passwd -q -d riaps')

@task
def updateAptKey():
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
    for pack in reversed(packages):
        package = pack + architecture
        sudo('apt-get remove -y ' + package)

@task
def kill():
    """Kills any hanging processes. deplo.stop should be called first"""
    deplo.stop()

    pgrepResult = sudo('pgrep \'riaps_\' -l')
    pgrepEntries = pgrepResult.rsplit('\n')
    processList = []

    for process in pgrepEntries:
        if process != "":
            processList.append(process.split()[1])
    for process in processList:
        sudo('pkill -SIGKILL ' + process)

    cmd = 'python3 -c "from riaps.utils.config import Config; c=Config(); print(c.NIC_NAME)"'
    nic_name = sudo(cmd)
    cmd = 'ip link show %s | awk \'/ether/ {print $2}\'' % nic_name
    mac = sudo(cmd)
    host_last_4 = mac[-5:-3] + mac[-2:]
    # Get last for digits of mac address since that is how apps and users are named.


    apps = sudo('\ls ' + env.riapsApps).split()  # \ls bypasses alias to ls with color formatting
    for app in apps:
        sudo('rm -R /home/riaps/riaps_apps/' + app + '/')
        if app != 'riaps-apps.lmdb':
            sudo('userdel ' + app.lower() + host_last_4)


@task
def updateConfig():
    """"Place local riaps.conf on all remote hosts"""
    if(os.path.isfile(os.path.join(os.getcwd(), "riaps.conf"))):
        put('riaps.conf')
        sudo('cp riaps.conf /etc/riaps/')
        sudo('chown root:root /etc/riaps/riaps.conf')
        sudo('rm riaps.conf')
    else:
        print("Local riaps.conf doesn't exist!")

@task
def updateLogConfig():
    """"Places local riaps-log.conf on all remote hosts"""
    if(os.path.isfile(os.path.join(os.getcwd(), "riaps-log.conf"))):
        put('riaps-log.conf')
        sudo('cp riaps-log.conf /etc/riaps/')
        sudo('chown root:root /etc/riaps/riaps-log.conf')
        sudo('rm riaps-log.conf')
    else:
        print("Local riaps-log.conf doesn't exist!")

# If using riaps-deplo.service, the log data is being recorded in a system journal.
# This function pulls that data from the system journal and places them in a log file
@task
def getLogs():
    """Get deployment logs and save them to logs/"""
    hostname = env.host_string
    sudo('journalctl -u riaps-deplo.service --since today > riaps-deplo-' + hostname + '.log')
    get('riaps-deplo-' + hostname + '.log','logs/')

@task
@hosts('localhost')
def ctrl():
    """Launch RIAPS controller"""
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
    """Configure BBBs to use this host as their default gateway"""
    env.warn_only = True
    # ---- EDIT HERE ----
    hostIP = get_ip()
    # Provide appropriate IP address
    sudo('route add default gw ' + hostIP + 'dev eth0')

# Reset the config files with the install files (include /etc/riaps/ folder)
# MM TODO: consider adding in future release
#@task
#def resetConfig():
#    """Reset the Configuration files installed"""
#    architecture = arch()
#    package = 'riaps-pycom-' + architecture
#    deplo.stop
#    sudo('dpkg --purge ' + package)
#    sudo('apt-get -o DPkg::options::=--force-confmiss --reinstall install ' + package)
#    deplo.start

# Turn off RIAPS security feature
@task
def securityOff():
    """Turn RIAPS security feature off"""
    execute(deplo.stop)
    riaps_conf_name = "/etc/riaps/riaps.conf"
    sed(riaps_conf_name, 'security = on', 'security = off', use_sudo=True)
    execute(deplo.start)

# Turn on RIAPS security feature
@task
def securityOn():
    """Turn RIAPS security feature on"""
    execute(deplo.stop)
    riaps_conf_name = "/etc/riaps/riaps.conf"
    sed(riaps_conf_name, 'security = off', 'security = on', use_sudo=True)
    execute(deplo.start)
