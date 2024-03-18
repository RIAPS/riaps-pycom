import toml
import os
from fabric import ThreadingGroup, Group, GroupResult, Result
from fabric.transfer import Result as TransferResult
from fabric.exceptions import GroupException
from riaps.rfab.api.exceptions import RFabException
import socket

def isIPaddress(addr):
    try:
        socket.inet_aton(addr)
        return True
    except socket.error:
        return False

def load_hostfile(hosts_file,validate=False):
    '''
    Load a hosts file, construct role definitions
    '''

    def catch(func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            raise Exception("%r" % args)
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

    if control and type(control) != str:
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

def load_role(role, validate=False) -> ThreadingGroup:
    riapsHome = os.getenv('RIAPSHOME')
    if riapsHome is None:
        riapsHome = os.getcwd()
        print(f"RIAPS Configuration - RIAPSHOME is not set, using {riapsHome}")
    hostfile = riapsHome+'/etc/riaps-hosts.conf'
    roledefs = load_hostfile(hostfile,validate)
    if roledefs is None:
        exit(-1)
    hosts = roledefs.get(role,None)
    if hosts is None:
        raise RFabException(f"No role \"{role}\" in {hostfile}, choose one of {list(roledefs)}")
    if len(hosts) == 0:
        raise RFabException(f"Zero hosts for role \"{role}\" in {hostfile}")
    return ThreadingGroup(*hosts)
