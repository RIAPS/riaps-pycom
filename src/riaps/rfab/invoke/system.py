from invoke import task, Collection, Context
from invoke.tasks import call
from fabric import Group, GroupResult
from fabric.exceptions import GroupException
import socket
from riaps.rfab import api
from .helpers import assert_role_in

@task
def check(c: Context):
    '''
    Confims a connection can be made
    '''
    res = api.sys.check(c.config.hosts,hide=c.config.hide)
    res.pretty_print(exception_hints=[(socket.gaierror,"No known address for host")])

@task(optional=['when','why'],pre=[call(assert_role_in,"remote")])
def shutdown(c: Context, when='now', why=''):
    api.sys.shutdown(c.config.hosts,when,why,hide=c.config.hide).pretty_print()

@task(pre=[call(assert_role_in,"remote")])
def reboot(c: Context):
    api.sys.reboot(c.config.hosts,hide=c.config.hide).pretty_print()

@task(pre=[call(assert_role_in,"remote","nodes")])
def clearJournal(c: Context):
    res = api.sys.sudo('journalctl --rotate && journalctl --vacuum-time=1s', c.config.hosts,hide = c.config.hide)
    res.pretty_print()

@task(positional=["local_file"])
def put(c: Context, local_file, remote_dir=''):
    '''
    Copies a local file to the target(s)
    '''
    api.sys.put( c.config.hosts, local_file, remote_dir)

@task(positional=["remote_file"],pre=[call(assert_role_in,'remote','nodes')])
def get(c: Context, remote_file, local_dir=''):
    '''
    Copies a remote file from the target(s)
    '''
    res = api.sys.get(remote_file,local_dir,c.config.hosts)

@task(positional=['command'])
def run(c: Context, command):
    res = api.sys.run(command,c.config.hosts,hide=c.config.hide)
    res.pretty_print()

@task
def arch(c: Context):
    '''
    Get architecture of host(s)
    '''
    res = api.sys.run("dpkg --print-architecture",c.config.hosts,hide=c.config.hide)

@task(pre=[call(assert_role_in,'nodes','remote')])
def flushIPTables(c: Context):
    '''
    Flush the iptables
    '''
    api.sys.sudo('iptables --flush',c.config.hosts,hide=c.config.hide).pretty_print()

@task(pre=[call(assert_role_in,'nodes','remote')])
def setJournalLogSize(c: Context, size):
    """Adjust journalctl log file size"""
    newSize = f'SystemMaxUse={size}M'
    res = api.sys.sudo(f'sed -i "/SystemMaxUse/c\{newSize}" /etc/systemd/journald.conf',c.config.hosts,hide=c.config.hide)

@task(pre=[call(assert_role_in,'nodes','remote')])
def getConfig(c: Context):
    '''
    Get configuration information from target nodes
    '''
    pass
    
ns = Collection('sys')
ns.add_task(check)
ns.add_task(shutdown)
ns.add_task(reboot)
ns.add_task(clearJournal)
ns.add_task(put)
ns.add_task(get)
ns.add_task(run)
ns.add_task(arch)
ns.add_task(flushIPTables)
ns.add_task(setJournalLogSize)

