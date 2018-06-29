# Fabric commands for performing system tasks
from fabric import api
from fabric.api import task, env, settings
from fabric.context_managers import hide

# Prevent namespace errors by explicitly defining which tasks belong to this file
__all__ = ['check', 'shutdown', 'reboot', 'clearJournal', 'run', 'sudo', 'get', 'put', 'arch']

# Check that all BBBs are communicating
@task
def check():
    """test that hosts are communicating"""
    run('hostname && uname -a')

# Shutdown the hosts
# Note: must be used prior to powering down the hosts
@task
def shutdown(when='now', why=''):
    """shutdown the hosts:[when],[why]"""
    sudo('shutdown ' + when + ' ' + why)

# Reboot the hosts
@task
def reboot():
    """reboot the hosts"""
    sudo('reboot &')

# The system journal run continuously with no regard to login session. So to isolate testing data, the system journal can be cleared.
@task
def clearJournal():
    """clear system journal"""
    sudo('rm -rf  /run/log/journal/*')
    sudo('systemctl restart systemd-journald')

# Wrapper for fabric.api.run to capture and combine and console output
@task
def run(command):
    """Execute command as user:<command>"""
    with hide('everything'), settings(warn_only=True):
        result = api.run(command)
        print("["+env.host+"] " + command)
        if result != '':
            print(result)
        return result


# Wrapper for fabric.api.sudo to capture and combine any console output
@task
def sudo(command):
    """Execute a command as root:<command>"""
    with hide('everything'), settings(warn_only=True):
        result = api.sudo(command)
        print("["+env.host+"] sudo " + command)
        if result != '':
            print(result)
        return result

@task
def get(fileName,localPrefix=''):
    """Download file from host:<file name>,[local prefix]"""
    api.get(env.nodePath + fileName, env.localPath+localPrefix)

# If transferring to a RIAPS account directory, use_sudo=False. 
# If transferring to a system location, use_sudo=True
@task
def put(fileName, localPrefix='', use_sudo=False):
    """Upload file to hosts:<file name>,[local prefix],[use sudo]"""
    api.put(env.localPath + localPrefix + fileName, env.nodePath + fileName, use_sudo)

@task
def arch():
    """Detect architecture of host"""
    return run("dpkg --print-architecture ")