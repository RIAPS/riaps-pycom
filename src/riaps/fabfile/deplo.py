# Fabric tasks for controlling riaps-deplo
import time
from .sys import sudo, run
from fabric.api import env, serial, task, hosts, roles

# Prevent namespace errors by explicitly defining which tasks belong to this file
__all__ = ['start', 'startSlow', 'startManual', 'restart', 'stop', 'enable', 'disable', 'status', 'journal']

@task
@roles('nodes','remote')
def start():
    """Start service"""
    sudo('systemctl start riaps-deplo.service')

@serial
@task
@roles('nodes','remote')
def startSlow(delay=1):
    """Start service serially with delay:[delay]"""
    time.sleep(delay)
    sudo('systemctl start riaps-deplo.service')

@task
# Start the deplo on all hosts
@roles('nodes','remote')
def startManual():
    """Start deplo on hosts without service"""
    hostname = env.host_string
    command = ('sudo -E riaps_deplo >~/riaps-' + hostname + '.log 2>&1 &')
    run(command)

@task
@roles('nodes','remote')
def restart():
    """Restart service"""
    sudo('systemctl restart riaps-deplo.service')

@task
@roles('nodes','remote')
def stop():
    """Stop service"""
    sudo('systemctl stop riaps-deplo.service')

@task
@roles('nodes','remote')
def enable():
    """Enable service"""
    sudo('systemctl enable riaps-deplo.service')

@task
@roles('nodes','remote')
def disable():
    """Disable service"""
    sudo('systemctl disable riaps-deplo.service')

@task
@roles('nodes','remote')
def status(n='10', grep=''):
    """Get systemctl service status:[# of lines],[grep args]"""
    if grep != '':
        grep=" | grep " + grep
    sudo("systemctl status riaps-deplo --no-pager -n " + n + grep)

@task
@roles('nodes','remote')
def journal(n='10', grep=''):
    """Get journalctl service log:[# of lines],[grep args]"""
    if grep != '':
        grep=" | grep " + grep
    sudo("journalctl -u riaps-deplo.service --no-pager -n " + n + grep)
