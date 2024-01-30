from invoke import task, Collection, Context
from invoke.tasks import call
from fabric import Group, GroupResult
from fabric.exceptions import GroupException
from riaps.rfab import api
from .helpers import assert_role_in

@task
def check(c: Context):
    '''
    Confims a connection can be made
    '''
    res = api.sys.check(c.config.hosts,hide=c.config.hide)
    res.pretty_print()

@task(optional=['when','why'],pre=[call(assert_role_in,"remote")],
      help={'when':'time passed to \'shutdown\', default "now"',
            'why':'message logged for shutdown reason'})
def shutdown(c: Context, when='now', why=''):
    """Shutdown the hosts"""
    res = api.sys.shutdown(c.config.hosts,when,why,hide=c.config.hide)
    res.pretty_print()

@task(pre=[call(assert_role_in,"remote")])
def reboot(c: Context):
    """Reboot the hosts"""
    res = api.sys.reboot(c.config.hosts,hide=c.config.hide)
    res.pretty_print()

@task(pre=[call(assert_role_in,"remote","nodes")])
def clearJournal(c: Context):
    """Clear system journal"""
    res = api.sys.sudo('journalctl --rotate && journalctl --vacuum-time=1s', c.config.hosts,hide = c.config.hide)
    res.pretty_print()

@task(positional=["local_file"],
      help={'local_file':'path to local file',
            'remote_dir':'remote directory to copy into'})
def put(c: Context, local_file, remote_dir=''):
    '''
    Copies a local file to the target(s)
    '''
    api.sys.put(c.config.hosts, local_file, remote_dir)

@task(positional=["remote_file"],pre=[call(assert_role_in,'remote','nodes')],
      help={'remote_file':'remote filename to copy locally',
            'local_dir':'local directory to save files in'})
def get(c: Context, remote_file, local_dir=''):
    '''
    Copies a remote file from the target(s)
    '''
    api.sys.get(c.config.hosts,remote_file,local_dir)

@task(positional=['command'],
      help={'command':'shell command to run, in quotes'})
def run(c: Context, command):
    """Execute command as user:<command>"""
    res = api.sys.run(command,c.config.hosts,hide=c.config.hide)
    res.pretty_print()

@task(positional=['command'],
      help={'command':'shell command to run, in quotes'})
def sudo(c: Context, command):
    """Sudo execute command as user:<command>"""
    res = api.sys.sudo(command,c.config.hosts,hide=c.config.hide)
    res.pretty_print()

@task
def arch(c: Context):
    '''
    Get architecture of host(s)
    '''
    res = api.sys.run("dpkg --print-architecture",c.config.hosts,hide=c.config.hide)
    res.pretty_print()

@task(pre=[call(assert_role_in,'nodes','remote')])
def flushIPTables(c: Context):
    '''
    Flush the iptables
    '''
    res = api.sys.sudo('iptables --flush',c.config.hosts,hide=c.config.hide)
    res.pretty_print()

@task(pre=[call(assert_role_in,'nodes','remote')])
def setJournalLogSize(c: Context, size):
    """Adjust journalctl log file size"""
    newSize = f'SystemMaxUse={size}M'
    res = api.sys.sudo(f'sed -i "/SystemMaxUse/c\{newSize}" /etc/systemd/journald.conf',c.config.hosts,hide=c.config.hide)
    res.pretty_print()

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
ns.add_task(sudo)
ns.add_task(arch)
ns.add_task(flushIPTables)
ns.add_task(setJournalLogSize)

