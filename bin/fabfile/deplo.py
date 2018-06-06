# Fabric taks for controlling riaps-deplo
import time
from .util import sudo
from fabric.api import env, serial, task

@task
def start():
    """start deplo background service on hosts"""
    sudo('systemctl start riaps-deplo.service')

@serial
@task
def startSlow(delay=1):
    """start deplo background service on hosts"""
    time.sleep(delay)
    sudo('systemctl start riaps-deplo.service')

@task
def restart():
    """restart the deplo background service on hosts"""
    sudo('systemctl restart riaps-deplo.service')

@task
def stop():
    """stop deplo background service on hosts"""
    sudo('systemctl stop riaps-deplo.service')

@task
def enable():
    """enable deplo background service on hosts"""
    sudo('systemctl enable riaps-deplo.service')

@task
def disable():
    """disable deplo background service on hosts"""
    sudo('systemctl disable riaps-deplo.service')

@task
def status(n='10', grep=''):
    """Get deplo service status"""
    if grep != '':
        grep=" | grep " + grep
    sudo("systemctl status riaps-deplo --no-pager -n " + n + grep)

@task
def journal(n='10', grep=''):
    """Grep deplo service status"""
    if grep != '':
        grep=" | grep " + grep
    sudo("journalctl -u riaps-deplo.service --no-pager -n " + n + grep)