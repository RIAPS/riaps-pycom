# Fabric commands for using the tsman utility
from .sys import run, sudo, get
from fabric.api import local, task, hosts, env

# Prevent namespace errors by explicitly defining which tasks belong to this file
__all__ = ['compare', 'checkPTP', 'config', 'status', 'restart', 'date', 'rdate']

@task
def compare():
    """Compare clocks on hosts"""
    hostname = env.host_string
    run('date +%H.%M.%S.%N > riaps-time-' + hostname + '.log')
    get('riaps-time-' + hostname + '.log','logs/')

@task
@hosts('localhost')
def checkPTP():
    """Check to see if ptp is running on control host"""
    local('ps -ef | grep ptp')

@task
def config(mode=''):
    """Change timesync configuration:[mode]"""
    sudo("timesyncctl config " + mode)

@task
def status():
    """Get timesync status"""
    sudo("timesyncctl status")

@task
def restart():
    """Restart timesync"""
    sudo("timesyncctl restart")

@task
def date():
    """Get the system time"""
    run("date")

@task
def rdate():
    """Update the system time"""
    sudo("rdate -s -n -4 time.nist.gov")
