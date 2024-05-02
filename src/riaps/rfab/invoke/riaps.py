from invoke import task, Collection, Context
from invoke.tasks import call
from fabric import Group, GroupResult, Result
from fabric.exceptions import GroupException
import socket
from riaps.rfab import api
from riaps.rfab.invoke.helpers import assert_role_in, assert_role_not_in
from riaps.rfab.api.riaps import *
from riaps.rfab.api.task import TaskRunner
from riaps.rfab.api.utils import make_log_folder
from pathlib import Path

@task(pre=[call(assert_role_not_in,'hostlist','nodes')])
def update(c: Context):
    """Update RIAPS packages from stable release"""
    kwargs = {'dry':c.config.run.dry,'verbose':c.config.verbose}
    if c.config.role in ('control','all'):
        print("Updating the control node...")
        runner = TaskRunner(c.config.hosts,UpdateControl,**kwargs)
        runner.set_log_folder(make_log_folder("riaps-update-control"))
        runner.run()
    if c.config.role in ('remote','all'):
        print("Updating the remote node(s)...")
        runner = TaskRunner(c.config.hosts,UpdateRemote,**kwargs)
        runner.set_log_folder(make_log_folder("riaps-update-remote"))
        runner.run()

@task(pre=[call(assert_role_in,'remote')],
      auto_shortflags=False,
      help={'keep-password':'prevents removal of password-authenticated login'})
def updateNodeKey(c: Context, keep_password=False):
    """Rekey the remote nodes with newly generated keys"""
    kwargs = {'dry':c.config.run.dry,'verbose':c.config.verbose}
    UpdateNodeKey.configure(keep_password)
    runner = TaskRunner(c.config.hosts,UpdateNodeKey,**kwargs)
    runner.set_log_folder(make_log_folder("riaps-update-node-key"))
    runner.run()
        
@task
def updateAptKey(c: Context):
    """Update RIAPS apt repo key"""
    kwargs = {'dry':c.config.run.dry,'verbose':c.config.verbose}
    runner = TaskRunner(c.config.hosts,UpdateAptKey,**kwargs)
    runner.set_log_folder(make_log_folder("riaps-update-apt-key"))
    runner.run()

@task(help={'package':"One of: timesync, pycom",
            'clean': 'Overwrite RIAPS config files'},
      auto_shortflags=False)
def install(c: Context, package, clean=False):
    """Install a package from the current directory"""
    kwargs = {'dry':c.config.run.dry,'verbose':c.config.verbose,'pty':True}
    if not package in ('timesync','pycom'):
        print(f"ERROR: cannot install {package}, choose from: timesync, pycom")
        exit(-1)
    logs_folder = Path(c.cwd,"logs")
    if not logs_folder.is_dir():
        logs_folder.mkdir()
    if package == 'pycom':
        PycomInstallTask.configure(c.cwd,logs_folder,clean)
        runner = TaskRunner(c.config.hosts,PycomInstallTask,**kwargs)
        runner.set_log_folder(make_log_folder("riaps-install-pycom"))
        runner.run()
    else:
        TimesyncInstallTask.configure(c.cwd,logs_folder,clean)
        runner = TaskRunner(c.config.hosts,TimesyncInstallTask,**kwargs)
        runner.set_log_folder(make_log_folder("riaps-install-timesync"))
        runner.run()

@task(pre=[call(assert_role_in,'remote')],
      help={'purge': "Purge RIAPS config files"},
      auto_shortflags=False)
def uninstall(c: Context, purge=False):
    """Uninstall all RIAPS packages from nodes"""
    kwargs = {'dry':c.config.run.dry,'verbose':c.config.verbose,'pty':True}
    PycomUninstallTask.configure(purge)
    runner = TaskRunner(c.config.hosts,PycomUninstallTask,**kwargs)
    runner.set_log_folder(make_log_folder("riaps-uninstall-pycom"))
    runner.run()

@task(pre=[call(assert_role_in,'nodes','remote')])
def reset(c: Context):
    """Stop all RIAPS procs & remove all apps, restart from clean state"""
    kwargs = {'dry':c.config.run.dry,'verbose':c.config.verbose}
    runner = TaskRunner(c.config.hosts,ResetTask,**kwargs)
    runner.set_log_folder(make_log_folder("riaps-reset"))
    runner.run()

    


ns = Collection('riaps')
ns.add_task(update)
ns.add_task(updateNodeKey)
ns.add_task(updateAptKey)
ns.add_task(install)
ns.add_task(uninstall)
ns.add_task(reset)