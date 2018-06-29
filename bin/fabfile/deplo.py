# Fabric tasks for controlling riaps-deplo
import time
from .sys import sudo
from fabric.api import env, serial, task

# Prevent namespace errors by explicitly defining which tasks belong to this file
__all__ = ['start', 'startSlow', 'restart', 'stop', 'enable', 'disable', 'status', 'journal']

@task
def start():
    """start service"""
    sudo('systemctl start riaps-deplo.service')

@serial
@task
def startSlow(delay=1):
    """start service serially with delay: """
    time.sleep(delay)
    sudo('systemctl start riaps-deplo.service')

@task
def restart():
    """restart service"""
    sudo('systemctl restart riaps-deplo.service')

@task
def stop():
    """stop service"""
    sudo('systemctl stop riaps-deplo.service')

@task
def enable():
    """enable service"""
    sudo('systemctl enable riaps-deplo.service')

@task
def disable():
    """disable service"""
    sudo('systemctl disable riaps-deplo.service')

@task
def status(n='10', grep=''):
    """Get systemctl service status:[# of lines],[grep args]"""
    if grep != '':
        grep=" | grep " + grep
    sudo("systemctl status riaps-deplo --no-pager -n " + n + grep)

@task
def journal(n='10', grep=''):
    """Get journalctl service log:[# of lines],[grep args]"""
    if grep != '':
        grep=" | grep " + grep
    sudo("journalctl -u riaps-deplo.service --no-pager -n " + n + grep)