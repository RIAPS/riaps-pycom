# Fabric commands for performing system tasks
from fabric import api, operations
from fabric.api import task, env, settings
from fabric.context_managers import hide
import os,csv,itertools,configparser

# Prevent namespace errors by explicitly defining which tasks belong to this file
__all__ = ['check', 'shutdown', 'reboot', 'clearJournal', 'run', 'sudo', 'hosts', 'get', 'put', 'arch', 'setup_cython', 'flushIPTables', 'journalLogSize', 'getDebugInfo']

# Check that all RIAPS nodes are communicating
@task
def check():
    """Test that hosts are communicating"""
    run('hostname && uname -a')

# Shutdown the hosts
# Note: must be used prior to powering down the hosts
@task
def shutdown(when='now', why=''):
    """Shutdown the hosts:[when],[why]"""
    sudo('shutdown ' + when + ' ' + why)

# Reboot the hosts
@task
def reboot():
    """Reboot the hosts"""
    sudo('reboot &')

# The system journal run continuously with no regard to login session. So to isolate testing data, the system journal can be cleared.
@task
def clearJournal():
    """Clear system journal"""
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
@api.hosts('localhost')
def hosts(hosts_file):
    """Load hosts from file:<file name>"""
    if not os.path.isfile(hosts_file):
        print('Hosts configuration file doesn\'t exist: %s' % hosts_file)
        return
    try:
        config = configparser.ConfigParser()
        settings = config.read(hosts_file)
    except Exception as e:
        print(' Hosts configuration file %s has a problem: %s.' % (hosts_file, str(e)))
        return

    riaps_section = 'RIAPS'
    if settings == [] or not config.has_section(riaps_section):
        print('Hosts configuration file %s is missing [RIAPS] section.' % (hosts_file))
        return

    found = False
    for item in config.items(riaps_section):
        key,arg = item
        if key == 'hosts':
            found = True
            # Parse hosts config as multi line csv
            lines = arg.replace('\'','"').split('\n')
            parser = csv.reader(lines) # Parse commas and quotations
            hosts = list(itertools.chain.from_iterable(parser)) # Combine lines
            env.hosts = list(filter(None, hosts)) # Filter out any empty strings
        else:
            print("Unrecognized key in %s: %s" % (hosts_file,key))
        if not found:
            print('Failed to find "hosts" key in hosts file %s' % hosts_file)

@task
def get(fileName, local_path='', use_sudo=False):
    """Download file from host:<file name>,[local path],[use sudo]"""
    use_sudo = use_sudo in ['True', 'true', 'Yes', 'yes', 'y']
    operations.get(local_path=local_path, remote_path=fileName, use_sudo=use_sudo)

# If transferring to a RIAPS account directory, use_sudo=False.
# If transferring to a system location, use_sudo=True
@task
def put(fileName, remote_path='', use_sudo=False):
    """Upload file to hosts:<file name>,[remote path],[use sudo]"""
    use_sudo = use_sudo in ['True', 'true', 'Yes', 'yes', 'y']
    operations.put(local_path=fileName, remote_path=remote_path, use_sudo=use_sudo)

@task
def arch():
    """Detect architecture of host"""
    return run("dpkg --print-architecture ")

@task
def setup_cython():
    """Fix 'Debugger speedups using cython not found' warnings"""
    sudo('wget https://raw.githubusercontent.com/fabioz/PyDev.Debugger/master/setup_cython.py -P /usr/local/lib/python3.5/dist-packages/')
    sudo('python3 /usr/local/lib/python3.5/dist-packages/setup_cython.py build_ext --inplace')

@task
def flushIPTables():
    """Flush the iptables"""
    sudo('iptables --flush')

@task
def journalLogSize(size):
    """Adjust journalctl log file size:<size>"""
    newSize = f'SystemMaxUse={size}M'
    sudo(f'sed -i "/SystemMaxUse/c\{newSize}" /etc/systemd/journald.conf')

@task
def getDebugInfo():
    """Get Debug Info from Connected Nodes"""
    run('echo "#SystemInfo" >> /home/riaps/.riaps/sysdebug.log')
    run('uname -a >> /home/riaps/.riaps/sysdebug.log')
    run('lsb_release -a >> /home/riaps/.riaps/sysdebug.log')
    run('cat /etc/hostname >> /home/riaps/.riaps/sysdebug.log')
    run('echo "\n" >> /home/riaps/.riaps/sysdebug.log')')
    run('echo "#Installed Apt Package Info" >> /home/riaps/.riaps/sysdebug.log')
    run('dpkg -l | grep zmq >> /home/riaps/.riaps/sysdebug.log')
    run('dpkg -l | grep riaps >> /home/riaps/.riaps/sysdebug.log')
    run('echo "\n" >> /home/riaps/.riaps/sysdebug.log')')
    run('echo "#Installed PIP3 Package Info" >> /home/riaps/.riaps/sysdebug.log')
    run('pip3 list >> /home/riaps/.riaps/sysdebug.log')
    run('echo "\n" >> /home/riaps/.riaps/sysdebug.log')')
    run('echo "#RIAPS Compiled Package Info" >> /home/riaps/.riaps/sysdebug.log')
    run('ls /usr/local/lib >> /home/riaps/.riaps/sysdebug.log')
    run('echo "\n" >> /home/riaps/.riaps/sysdebug.log')')
    run('echo "#RIAPS Configuration" >> /home/riaps/.riaps/sysdebug.log')
    sudo('cat /etc/riaps/riaps.conf >> /home/riaps/.riaps/sysdebug.log')
