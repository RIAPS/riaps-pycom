from invoke import task, Collection, Context
from invoke.tasks import call
from fabric import Group, GroupResult
from fabric.exceptions import GroupException
import socket
from riaps.rfab.api.deplo import *
from riaps.rfab.api.task import TaskRunner
from riaps.rfab.api.utils import make_log_folder
from .helpers import assert_role_in

@task(pre=[call(assert_role_in,'nodes','remote')])
def start(c: Context):
    """Start deployment service"""
    kwargs = {'dry':c.config.run.dry,'verbose':c.config.verbose}
    runner = TaskRunner(c.config.hosts,DeploStart,**kwargs)
    runner.set_log_folder(make_log_folder("deplo.start"))
    runner.run()

# @serial
# @task
# @roles('nodes','remote')
# def startSlow(delay=1):
#     """Start service serially with delay:[delay]"""
#     time.sleep(delay)
#     sudo('systemctl start riaps-deplo.service')

@task(pre=[call(assert_role_in,'nodes','remote')])
def startManual(c: Context):
    """Start deplo on hosts as standard process"""
    kwargs = {'dry':c.config.run.dry,'verbose':c.config.verbose}
    runner = TaskRunner(c.config.hosts,DeploStartManual,**kwargs)
    runner.set_log_folder(make_log_folder("deplo.startManual"))
    runner.run()

@task(pre=[call(assert_role_in,'nodes','remote')])
def restart(c: Context):
    """Restart deployment service"""
    kwargs = {'dry':c.config.run.dry,'verbose':c.config.verbose}
    runner = TaskRunner(c.config.hosts,DeploRestart,**kwargs)
    runner.set_log_folder(make_log_folder("deplo.restart"))
    runner.run()

@task(pre=[call(assert_role_in,'nodes','remote')])
def stop(c: Context):
    """Stop deployment service"""
    kwargs = {'dry':c.config.run.dry,'verbose':c.config.verbose}
    runner = TaskRunner(c.config.hosts,DeploStop,**kwargs)
    runner.set_log_folder(make_log_folder("deplo.stop"))
    runner.run()

@task(pre=[call(assert_role_in,'nodes','remote')])
def enable(c: Context):
    """Enable restarts for crash/startup"""
    kwargs = {'dry':c.config.run.dry,'verbose':c.config.verbose}
    runner = TaskRunner(c.config.hosts,DeploEnable,**kwargs)
    runner.set_log_folder(make_log_folder("deplo.enable"))
    runner.run()

@task(pre=[call(assert_role_in,'nodes','remote')])
def disable(c: Context):
    """Disable restarts for crash/startup"""
    kwargs = {'dry':c.config.run.dry,'verbose':c.config.verbose}
    runner = TaskRunner(c.config.hosts,DeploDisable,**kwargs)
    runner.set_log_folder(make_log_folder("deplo.disable"))
    runner.run()

@task(pre=[call(assert_role_in,'nodes','remote')],
      help={'n':'number of lines to collect (default: 10)',
            'grep':'arbitrary grep args to filter results, in quotes'})
def status(c: Context, n='10', grep=''):
    """Get systemctl service status"""
    kwargs = {'dry':c.config.run.dry,'verbose':True}
    DeploStatus.configure(n,grep)
    runner = TaskRunner(c.config.hosts,DeploStatus,**kwargs)
    runner.set_log_folder(make_log_folder("deplo.status"))
    runner.run()

@task(pre=[call(assert_role_in,'nodes','remote')],
      help={'n':'number of lines to collect (default: 10)',
            'grep':'arbitrary grep args to filter results, in quotes'})
def journal(c: Context, n='10', grep=''):
    """Get journald service log"""
    kwargs = {'dry':c.config.run.dry,'verbose':True}
    DeploJournal.configure(n,grep)
    runner = TaskRunner(c.config.hosts,DeploJournal,**kwargs)
    runner.set_log_folder(make_log_folder("deplo.journal"))
    runner.run()

ns = Collection('deplo')
ns.add_task(start)
ns.add_task(startManual)
ns.add_task(restart)
ns.add_task(stop)
ns.add_task(enable)
ns.add_task(disable)
ns.add_task(status)
ns.add_task(journal)