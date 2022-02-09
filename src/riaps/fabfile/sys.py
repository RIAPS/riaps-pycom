# Fabric commands for performing system tasks
from fabric import api, operations
from fabric.api import task, env, settings, roles, local, hosts
from fabric.context_managers import hide
import os
import toml
import socket


# Prevent namespace errors by explicitly defining which tasks belong to this file
__all__ = ['check', 'shutdown', 'reboot', 'clearJournal', 'run', 'sudo', 'arch',
           'flushIPTables', 'setJournalLogSize', 'getConfig']

def catch(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception:
        raise Exception("%r" % args)

def isIPaddress(addr):
    try:
        socket.inet_aton(addr)
        return True
    except socket.error:
        return False

def load_hosts(hosts_file,validate=False):
    '''
    Load a hosts file, construct role definitions
    '''
    if not os.path.isfile(hosts_file):
        print('Hosts configuration file doesn\'t exist: %s' % hosts_file)
        return None
    try:
        config = toml.load(hosts_file)
    except Exception as e:
        print(' Hosts configuration file %s has a problem: %s.' % (hosts_file, str(e)))
        return None

    spec = config.get('RIAPS',None)

    if spec is None:
        print('Hosts configuration file %s is missing [RIAPS] section.' % (hosts_file))
        return None

    # control is optional
    control = spec.get('control', None)

    if type(control) != str:
        print("String is expected: %r" % control)
        return None

    if control in {'localhost', '127.0.0.1'}:
        print("Control hostname or IP address is expected: %r " % control)
        return None
    else:
        control = socket.gethostname() if control is None else control

    control_ = control if control.endswith('.local') or isIPaddress(control) else control + '.local'

    if validate:
        # Validate control host name
        try:
            _control = catch(socket.gethostbyname,control_)
        except Exception as e:
            print('Control host name %s cannot be resolved.' % str(e))
    #   return None

    # nodes are required
    nodes = spec.get('nodes', None)
    if nodes is None:
        print("No nodes specified in %s." % (hosts_file))
        return None

    if type(nodes) == str: nodes = [nodes]

    if validate:
        # Validate target host names
        for node in nodes:
            try:
                _nodes = catch(socket.gethostbyname,node)
            except Exception as e:
                print('Host name %s cannot be resolved.' % str(e))
                # return None

    nodes = [node if node != control else control_ for node in nodes]

    nodeS,controlS = set(nodes), set([control_])

    roledefs = {"nodes" : nodes,                            # Nodes that run apps
                "control" : [control_],                     # Control host
                "remote" : list(nodeS.difference(controlS)),# Only the remote nodes
                "all" : list(nodeS.union(controlS))         # All nodes
                }
    return roledefs


def hosts(hosts_file,validate=False):
    """
    Load hosts from file, setup hosts, roles, and role definitions
    """
    if env.hosts:                   # Hosts on command line
        if not env.roles:           # No roles set
            control = socket.gethostname()  # Control on the same subnet
            control_ = control if control.endswith('.local') else control + '.local'
            nodes = [node if node != control else control_ for node in env.hosts]
            nodeS,controlS = set(nodes),set([control_])
            roledefs = {"nodes" : nodes,# Only the hosts listed will be 'nodes' 
                        "control" : [], # [control_],
                        "remote" : list(nodeS.difference(controlS)),
                        "all" : nodes   # list(nodeS.union(controlS)) 
                        }
        else:                       # Roles on command line (to be used in tasks)
            roledefs = load_hosts(hosts_file,validate)
            if roledefs is None: return
            for key in [key for key in roledefs if key not in env.roles]:
                roledefs[key] = []          # Clear roles not on command line
            for key in roledefs:            # Remove hosts not on command line
                for host in roledefs[key]:
                    if host not in env.hosts:
                        roledefs[key].remove(host)
    else:                           # Hosts/roles from file
        roledefs = load_hosts(hosts_file,validate)
        if roledefs is None: return
        if env.roles:               # If roles from command line, keep only those roles
            for key in [key for key in roledefs if key not in env.roles]:
                roledefs[key] = []

    env.hosts = []
    env.roles =  [] 
    env.roledefs = roledefs

# Check that all RIAPS nodes are communicating
@task
@roles('nodes','remote','control','all')
def check():
    """Test that hosts are communicating"""
    run('hostname && uname -a')

# Shutdown the hosts
# Note: must be used prior to powering down the hosts
@task
@roles('remote')
def shutdown(when='now', why=''):
    """Shutdown the hosts:[when],[why]"""
    sudo('shutdown ' + when + ' ' + why)

# Reboot the hosts
@task
@roles('remote')
def reboot():
    """Reboot the hosts"""
    sudo('reboot &')

# The system journal run continuously with no regard to login session.
# So to isolate testing data, the system journal can be cleared.
@task
@roles('nodes','remote')
def clearJournal():
    """Clear system journal"""
    sudo('rm -rf  /run/log/journal/*')
    sudo('systemctl restart systemd-journald')

# Wrapper for fabric.api.run to capture and combine and console output
@task
@roles('nodes','control','remote','all')
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
@roles('nodes','control','remote','all')
def sudo(command):
    """Execute a command as root:<command>"""
    with hide('everything'), settings(warn_only=True):
        result = api.sudo(command)
        print("["+env.host+"] sudo " + command)
        if result != '':
            print(result)
        return result

@task
@roles('control')
def get(fileName, local_path='', use_sudo=False):
    """Download file from host:<file name>,[local path],[use sudo]"""
    use_sudo = use_sudo in ['True', 'true', 'Yes', 'yes', 'y']
    operations.get(local_path=local_path, remote_path=fileName, use_sudo=use_sudo)

# If transferring to a RIAPS account directory, use_sudo=False.
# If transferring to a system location, use_sudo=True
@task
@roles('control')
def put(fileName, remote_path='', use_sudo=False):
    """Upload file to hosts:<file name>,[remote path],[use sudo]"""
    use_sudo = use_sudo in ['True', 'true', 'Yes', 'yes', 'y']
    operations.put(local_path=fileName, remote_path=remote_path, use_sudo=use_sudo)

@task
@roles('nodes','control','remote','all')
def arch():
    """Detect architecture of host"""
    return run("dpkg --print-architecture ")

# @task
# @roles('all')
# def setup_cython():
#     """Fix 'Debugger speedups using cython not found' warnings"""
#     sudo('wget https://raw.githubusercontent.com/fabioz/PyDev.Debugger/master/setup_cython.py -P /usr/local/lib/python3.5/dist-packages/')
#     sudo('python3 /usr/local/lib/python3.5/dist-packages/setup_cython.py build_ext --inplace')

@task
@roles('nodes','remote')
def flushIPTables():
    """Flush the iptables"""
    sudo('iptables --flush')

@task
@roles('nodes','remote')
def setJournalLogSize(size):
    """Adjust journalctl log file size:size"""
    newSize = f'SystemMaxUse={size}M'
    sudo(f'sed -i "/SystemMaxUse/c\{newSize}" /etc/systemd/journald.conf')

def runCmd(cmd,log=None,sudo=False):
    cmdLine = cmd + (" >> " + log if log else "") + " 2>&1"
    if sudo:
        sudo(cmdLine)
    else:
        run(cmdLine)

@task
@roles('nodes','remote','all')
def getConfig():
    """Get configuration information from target nodes"""
    hostname = run('hostname')
    confFile = '/home/riaps/sysconfig-' + hostname + '.log'
    run("rm -f %s" % confFile)
    for cmd in ['echo "### system"',
                'echo "hostname: " `hostname` ',
                'uname -a ',
                'lsb_release -a ',
                'python3 --version ',
                'echo "### apt packages" ',
                'dpkg -l | grep zmq ',
                'dpkg -l | grep riaps ',
                'echo "### riaps.conf" ',
                'cat /etc/riaps/riaps.conf ',
                'echo "### pip packages" ',
                'pip3 list ',
                'echo "### local libraries" ',
                'ls -l /usr/local/lib/lib* ',
                'echo "### riaps-log.conf" ',
                'cat /etc/riaps/riaps-log.conf ',
                'echo "### redis version" ',
                'redis-server --version ',
                'echo "### redis.conf" ',
                'echo "`cat /etc/redis/redis.conf`"'
                ]:
        runCmd(cmd,confFile)
    local('mkdir -p logs')
    get(confFile,'logs/')
