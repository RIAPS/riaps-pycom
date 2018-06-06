# Fabric commands for performing system tasks
from . import util
from fabric.api import task, env

# Check that all BBBs are communicating
@task
def check():
    """test that hosts are communicating"""
    util.run('hostname && uname -a')

# Shutdown the hosts
# Note: must be used prior to powering down the hosts
@task
def shutdown(when='now', why=''):
    """shutdown the hosts"""
    util.sudo('shutdown ' + when + ' ' + why)

# Reboot the hosts
@task
def reboot():
    """reboot the hosts"""
    util.sudo('reboot &')

# The system journal run continuously with no regard to login session. So to isolate testing data, the system journal can be cleared.
@task
def clearJournal():
    """clear system journal"""
    util.sudo('rm -rf  /run/log/journal/*')
    util.sudo('systemctl restart systemd-journald')

# Task wrapper for util.run to sys.run
@task
def run(command):
    util.run(command)

# Task wrapper for util.sudo to sys.sudo
@task
def sudo(command):
    util.sudo(command)