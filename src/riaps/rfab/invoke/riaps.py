from invoke import task, Collection, Context
from invoke.tasks import call
from fabric import Group, GroupResult, Result
from fabric.exceptions import GroupException
import socket
from riaps.rfab import api
from riaps.rfab.invoke.helpers import assert_role_in
from riaps.rfab.api.riaps import *
from riaps.rfab.api.task import TaskRunner
from riaps.rfab.api.utils import make_log_folder
from pathlib import Path

@task(pre=[call(assert_role_in,'control')])
def update_control(c: Context):
    """Update RIAPS packages from stable release"""
    kwargs = {'dry':c.config.run.dry,'verbose':c.config.verbose}
    runner = TaskRunner(c.config.hosts,UpdateControl,**kwargs)
    runner.set_log_folder(make_log_folder("update-control"))
    runner.run()

@task(pre=[call(assert_role_in,'remote')])
def update_remote(c: Context):
    """Update RIAPS packages from stable release"""
    kwargs = {'dry':c.config.run.dry,'verbose':c.config.verbose}
    runner = TaskRunner(c.config.hosts,UpdateRemote,**kwargs)
    runner.set_log_folder(make_log_folder("update-remote"))
    runner.run()

@task(pre=[call(assert_role_in,'remote')],auto_shortflags=False,
      help={'keep-password':'prevents removal of password-authenticated login'})
def updateNodeKey(c: Context, keep_password=False):
    """Rekey the remote nodes with newly generated keys"""
    kwargs = {'dry':c.config.run.dry,'verbose':c.config.verbose}
    UpdateNodeKey.configure(keep_password=True)
    runner = TaskRunner(c.config.hosts,UpdateNodeKey,**kwargs)
    runner.set_log_folder(make_log_folder("update-node-key"))
    runner.run()
        
@task
def updateAptKey(c: Context):
    """Update RIAPS apt repo key"""
    kwargs = {'dry':c.config.run.dry,'verbose':c.config.verbose}
    runner = TaskRunner(c.config.hosts,UpdateAptKey,**kwargs)
    runner.set_log_folder(make_log_folder("update-apt-key"))
    runner.run()

@task(help={'clean': 'Overwrite RIAPS config files'},
      auto_shortflags=False)
def install(c: Context, clean=False):
    kwargs = {'dry':c.config.run.dry,'verbose':c.config.verbose,'pty':True}
    logs_folder = Path(c.cwd,"logs")
    if not logs_folder.is_dir():
        logs_folder.mkdir()
    PycomInstallTask.configure(c.cwd,logs_folder,clean)
    runner = TaskRunner(c.config.hosts,PycomInstallTask,**kwargs)
    runner.set_log_folder(make_log_folder("install-pycom"))
    runner.run()

@task(pre=[call(assert_role_in,'remote')],
      help={'purge': "Purge RIAPS config files"},
      auto_shortflags=False)
def uninstall(c: Context, purge=False):
    """Uninstall all RIAPS packages from nodes"""
    kwargs = {'dry':c.config.run.dry,'verbose':c.config.verbose,'pty':True}
    PycomUninstallTask.configure(purge)
    runner = TaskRunner(c.config.hosts,PycomUninstallTask,**kwargs)
    runner.set_log_folder(make_log_folder("pycom_uninstall"))
    runner.run()

@task(pre=[call(assert_role_in,'nodes','remote')])
def reset(c: Context):
    kwargs = {'dry':c.config.run.dry,'verbose':c.config.verbose}
    runner = TaskRunner(c.config.hosts,ResetTask,**kwargs)
    runner.set_log_folder(make_log_folder("riaps_reset"))
    runner.run()

    


ns = Collection('riaps')
ns.add_task(update_control)
ns.add_task(update_remote)
ns.add_task(updateNodeKey)
ns.add_task(updateAptKey)
ns.add_task(install)
ns.add_task(uninstall)
ns.add_task(reset)