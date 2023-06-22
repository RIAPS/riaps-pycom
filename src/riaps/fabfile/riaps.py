# Fabric commands for managing RIAPS installs and applications
from . import deplo
from .sys import run, sudo, put, get, arch
from fabric.api import env, task, hosts, roles, local, execute
from fabric.contrib.files import sed
import os
import os.path
import time
from riaps.consts.defs import *

# Prevent namespace errors by explicitly defining which tasks belong to this file
__all__ = ['update','updateNodeKey','updateAptKey','install','uninstall','reset',
           'updateConfig','updateLogConfig', 'getSystemLogs', 'getAppLogs',
           'ctrl', 'configRouting', 'securityOff', 'securityOn']

# RIAPS packages
packages = [
            'riaps-timesync',
            'riaps-pycom'
            ]

# RIAPS update (from release)
@task
@roles('nodes','control','remote','all')
def update():
    """Update RIAPS packages from official release"""
    sudo('apt-get update')
    architecture = arch()
    hostname = env.host_string
    controlhost = "{}".format(*env.roledefs['control'])
    global packages
    for pack in packages:
        if pack == 'riaps-pycom':
            if controlhost == hostname:
                package = pack + '-dev'
            else:
                package = pack
        else:
            package = pack + '-' + architecture
                
        sudo('apt-get install ' + package + ' -y')

@task
@roles('remote')
def updateNodeKey(keepPasswd=False):
    """Rekey the remote nodes with newly generated keys:[keepPasswd]"""
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

    # Defaults to remove password to remote nodes, user can request to keep the password enabled
    if not keepPasswd:
        sudo('passwd -q -d riaps')

@task
@roles('nodes','control','remote','all')
def updateAptKey():
    """Update RIAPS apt key"""
    sudo('wget -qO - https://riaps.isis.vanderbilt.edu/keys/riapspublic.key | apt-key add -')

# See https://raphaelhertzog.com/2010/09/21/debian-conffile-configuration-file-managed-by-dpkg/

# RIAPS install (from local host)
@task
@roles('nodes','control','remote','all')
def install(keepConfig=False):
    """Install RIAPS packages from host:[keepConfig]"""
    global packages
    hostname = env.host_string
    controlhost = "{}".format(*env.roledefs['control'])
    architecture = arch()
    for pack in packages:
        if pack == 'riaps-pycom':
            if controlhost == hostname:
                package = pack + '-dev' + '.deb'
            else:
                package = pack + '.deb'
        else:
            package = pack + '-' + architecture + '.deb'
        try:
            if not os.path.exists(package): continue
            put(package)
            keep = '--force-confold' if keepConfig else '--force-confnew'
            sudo('dpkg -i '+ keep + ' ' + package + ' > riaps-install-' + hostname + '-' + package + '.log')
            sudo('rm -f %s' %(package))
            local('mkdir -p logs')
            get('riaps-install-' + hostname + '-' + package + '.log', 'logs/')
        except Exception as e:
            print("install exception: %r" % e)

@task
@roles('nodes','control','remote','all')
def uninstall(keepConfig=False):
    """Uninstall all RIAPS packages from nodes:[keepConfig]"""
    global packages
    architecture = arch()
    hostname = env.host_string
    controlhost = "{}".format(*env.roledefs['control'])
    for pack in reversed(packages):
        if pack == 'riaps-pycom':
            if controlhost == hostname:
                package = pack + '-dev'
            else:
                package = pack
        else:
            package = pack + '-' + architecture
        try:
            sudo('apt-get remove -y ' + package)
        except Exception as e:
            print("uninstall exception: %r" % e)
        if keepConfig: continue
        try:
            sudo('dpkg --purge ' + package)
        except Exception as e:
            print("purge exception: %r" % e)
    # run('rm -f riaps*.log')

@task
@roles('nodes','remote')
def reset():
    """Kill riaps_, clean, restart riaps_*"""
    deplo.stop()            # stop deplo service
    deplo.disable()
    
    sudo('pkill -SIGKILL "(riaps_deplo|riaps_disco|riaps_actor|riaps_device)"')

    remains = sudo('pgrep -l riaps_')
    if remains:
        print("=== Still alive: " + remains)

    hostname = run('hostname')
    if hostname[0:4] == 'riaps':
        host_last_4 = hostname[-4:]
    else:
        # If it doesn't start with riaps, assume it is a development VM
        # Get last for digits of mac address since that is how apps and users are named.
        cmd = 'python3 -c "from riaps.utils.config import Config; c=Config(); print(c.NIC_NAME)"'
        nic_name = sudo(cmd)
        if nic_name != None:
            cmd = 'ip link show %s | awk \'/ether/ {print $2}\'' % nic_name
            mac = sudo(cmd)
            host_last_4 = mac[-5:-3] + mac[-2:]
        else:                           # Should have set the NIC_NAME ...
            host_last_4 = '0000'

    apps = sudo('\ls ' + env.riapsApps).split()  # \ls bypasses alias to ls with color formatting
    apps = list(set(apps).difference(set(['riaps-apps.lmdb','riaps-disco.lmdb'])))
    for app in apps:
        sudo('rm -R ' + env.riapsApps + '/' + app + '/')
        sudo('userdel ' + app.lower() + host_last_4)    # May fail if dev vm
    sudo('rm -R ' + env.riapsApps + '/riaps*.lmdb')
    
    deplo.enable()
    deplo.start()

@task
@roles('nodes','remote')
def updateConfig():
    """"Place local riaps.conf on all nodes"""
    if(os.path.isfile(os.path.join(os.getcwd(), "riaps.conf"))):
        put('riaps.conf')
        sudo('cp riaps.conf /etc/riaps/')
        sudo('chown root:root /etc/riaps/riaps.conf')
        sudo('rm riaps.conf')
    else:
        print("Local ./riaps.conf doesn't exist!")

@task
@roles('nodes','remote')
def updateLogConfig():
    """"Places local riaps-log.conf on all remote hosts"""
    if(os.path.isfile(os.path.join(os.getcwd(), "riaps-log.conf"))):
        put('riaps-log.conf')
        sudo('cp riaps-log.conf /etc/riaps/')
        sudo('chown root:root /etc/riaps/riaps-log.conf')
        sudo('rm riaps-log.conf')
    else:
        print("Local ./riaps-log.conf doesn't exist!")

# If using riaps-deplo.service, the log data is being recorded in a system journal.
# This function pulls that data from the system journal and places them in a log file
@task
@roles('nodes','control','remote','all')
def getSystemLogs():
    """Get deployment logs and save them to logs/"""
    hostname = env.host_string
    sudo('journalctl -u riaps-deplo.service --since today > riaps-deplo-' + hostname + '.log')
    local('mkdir -p logs')
    get('riaps-deplo-' + hostname + '.log','logs/')

@task
@roles('nodes','control','remote','all')
def getAppLogs(app_name):
    """Get deployment logs and save them to logs/:app_name"""
    hostname = env.host_string
    local('mkdir -p logs/' + hostname)
    get(env.riapsApps + '/' + app_name + '/*.log', 'logs/' + hostname + '/')

@task
# @hosts('localhost')
@roles('control')
def ctrl():
    """Launch RIAPS controller"""
    local('riaps_ctrl')

# Find IP address of primary network interface, typically eth0
import socket
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))    # doesn't even have to be reachable
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

# Setup hosts routing, if needed.  Configure to your system's setup
@task
@roles('remote')
def configRouting():
    """Configure RIAPS nodes (eth0) to use control host as their default gateway"""
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
@roles('nodes','control','remote','all')
def securityOff():
    """Turn RIAPS security feature off"""
    execute(deplo.stop)
    riaps_conf_name = "/etc/riaps/riaps.conf"
    sed(riaps_conf_name, 'security = on', 'security = off', use_sudo=True)
    execute(deplo.start)

# Turn on RIAPS security feature
@task
@roles('nodes','control','remote','all')
def securityOn():
    """Turn RIAPS security feature on"""
    execute(deplo.stop)
    riaps_conf_name = "/etc/riaps/riaps.conf"
    sed(riaps_conf_name, 'security = off', 'security = on', use_sudo=True)
    execute(deplo.start)
