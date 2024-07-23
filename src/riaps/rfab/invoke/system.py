from invoke import task, Collection, Context
from invoke.tasks import call
from fabric import Group, GroupResult
from fabric.exceptions import GroupException
from riaps.rfab import api
from riaps.rfab.api.task import TaskRunner
from riaps.rfab.api.sys import *
from riaps.rfab.api.utils import make_log_folder
from .helpers import assert_role_in
from os.path import isfile
from pathlib import Path

@task
def check(c: Context):
    '''
    Confims a connection can be made
    '''
    kwargs = {'dry':c.config.run.dry,'verbose':c.config.verbose}
    runner = TaskRunner(c.config.hosts,SysCheck,**kwargs)
    runner.set_log_folder(make_log_folder("sys.check"))
    runner.run()


@task(optional=['when','why'],pre=[call(assert_role_in,"remote")],
      help={'when':'time passed to \'shutdown\', default "1"',
            'why':'message logged for shutdown reason'})
def shutdown(c: Context, when='1', why=''):
    """Shutdown the hosts"""
    kwargs = {'dry':c.config.run.dry,'verbose':c.config.verbose}
    SysShutdown.configure(when,why)
    runner = TaskRunner(c.config.hosts,SysShutdown,**kwargs)
    runner.set_log_folder(make_log_folder("sys.shutdown"))
    runner.run()

@task(pre=[call(assert_role_in,"remote")])
def reboot(c: Context):
    """Reboot the hosts"""
    kwargs = {'dry':c.config.run.dry,'verbose':c.config.verbose}
    runner = TaskRunner(c.config.hosts,SysReboot,**kwargs)
    runner.set_log_folder(make_log_folder("sys.reboot"))
    runner.run()

@task(pre=[call(assert_role_in,"remote","nodes")])
def clearJournal(c: Context):
    """Clear system journal"""
    kwargs = {'dry':c.config.run.dry,'verbose':c.config.verbose}
    runner = TaskRunner(c.config.hosts,SysClearJournal,**kwargs)
    runner.set_log_folder(make_log_folder("sys.clearJournal"))
    runner.run()

@task(positional=["local_file"],
      help={'local_file':'path to local file',
            'remote_dir':'remote directory to copy into'})
def put(c: Context, local_file, remote_dir=''):
    '''
    Copies a local file to the target(s)
    '''

    kwargs = {'dry':c.config.run.dry,'verbose':c.config.verbose}
    SysPut.configure(local_file,remote_dir)
    runner = TaskRunner(c.config.hosts,SysPut,**kwargs)
    runner.set_log_folder(make_log_folder("sys.put"))
    runner.run()


@task(pre=[call(assert_role_in,'remote','nodes')],
      help={'remote_file':'remote filename to copy locally',
            'local_dir':'local directory to save files in',
            'name':'local name to use for file(s)'},)
def get(c: Context, remote_file, local_dir='', name=''):
    '''
    Copies a remote file from the host(s) to local folder(s)
    '''
    kwargs = {'dry':c.config.run.dry,'verbose':c.config.verbose}
    SysGet.configure(remote_file,local_dir,name)
    runner = TaskRunner(c.config.hosts,SysGet,**kwargs)
    runner.set_log_folder(make_log_folder("sys.get"))
    runner.run()


@task(positional=['command'],
      help={'command':'shell command to run, in quotes'})
def run(c: Context, command):
    """Execute command as user:<command>"""
    kwargs = {'dry':c.config.run.dry,'verbose':c.config.verbose}
    SysRun.configure(command)
    runner = TaskRunner(c.config.hosts,SysRun,**kwargs)
    runner.set_log_folder(make_log_folder("sys.run"))
    runner.run()

@task(positional=['command'],
      help={'command':'shell command to run, in quotes'})
def sudo(c: Context, command):
    """Sudo execute command as root:<command>"""
    kwargs = {'dry':c.config.run.dry,'verbose':c.config.verbose}
    SysSudo.configure(command)
    runner = TaskRunner(c.config.hosts,SysSudo,**kwargs)
    runner.set_log_folder(make_log_folder("sys.sudo"))
    runner.run()

@task
def arch(c: Context):
    '''
    Get architecture of host(s)
    '''
    kwargs = {'dry':c.config.run.dry,'verbose':True}
    runner = TaskRunner(c.config.hosts,SysArch,**kwargs)
    runner.set_log_folder(make_log_folder("sys.arch"))
    runner.run()

@task(pre=[call(assert_role_in,'nodes','remote')])
def flushIPTables(c: Context):
    '''
    Flush the iptables
    '''
    kwargs = {'dry':c.config.run.dry,'verbose':c.config.verbose}
    runner = TaskRunner(c.config.hosts,SysFlushIPTables,**kwargs)
    runner.set_log_folder(make_log_folder("sys.flushIPTables"))
    runner.run()

@task(pre=[call(assert_role_in,'nodes','remote')],
      help={'size':"(int) number of MB"})
def setJournalLogSize(c: Context, size=64):
    """Adjust journalctl log file size"""
    newSize = f'SystemMaxUse={size}M'
    kwargs = {'dry':c.config.run.dry,'verbose':c.config.verbose}
    SysSudo.configure(f'sed -i "/SystemMaxUse/c\{newSize}" /etc/systemd/journald.conf')
    runner = TaskRunner(c.config.hosts,SysSudo,**kwargs)
    runner.set_log_folder(make_log_folder("sys.setJournalLogSize"))
    runner.run()

@task(pre=[call(assert_role_in,'nodes','remote','all')])
def getConfig(c: Context):
    '''Collect system state date to local folder ./logs/
    '''
    kwargs = {'dry':c.config.run.dry,'verbose':c.config.verbose}
    #Make log folder
    logfolder = Path(c.cwd,"logs")
    if logfolder.exists() and logfolder.is_dir():
        if len(list(logfolder.iterdir())):
            print(f"ERROR: {c.cwd}/logs is not empty! No commands run. Exiting...")
            exit(1)
    logfolder.mkdir(exist_ok=True)
    runner = TaskRunner(c.config.hosts,SysGetConfig.configure(logfolder),**kwargs)
    runner.set_log_folder(make_log_folder("sys.getConfig"))
    runner.run()


    
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
ns.add_task(getConfig)

