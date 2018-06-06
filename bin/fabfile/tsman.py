# Fabric commands for using the tsman utility
from .util import run, sudo, getFile
from fabric.api import local, task, hosts, env

@task
def getTime():
    """Compare clocks on hosts"""
    hostname = env.host_string
    run('date +%H.%M.%S.%N > riaps-time-' + hostname + '.log')
    getFile('riaps-time-' + hostname + '.log','logs/')

@task
@hosts('localhost')
def checkPTP():
    """ check to see if ptp is running on control host"""
    local('ps -ef | grep ptp')

@task
def config(mode=''):
    sudo("/opt/riaps/armhf/bin/tsman config " + mode)

@task
def status():
    sudo("/opt/riaps/armhf/bin/tsman status")

@task
def restart():
    sudo("/opt/riaps/armhf/bin/tsman restart")

@task
def date():
    run("date")

@task
def rdate():
    sudo("rdate -s -n -4 time.nist.gov")