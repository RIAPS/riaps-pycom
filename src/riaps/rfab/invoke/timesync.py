from invoke import task, Collection, Context
from invoke.tasks import call
from riaps.rfab.api.timesync import *
from riaps.rfab.api.task import TaskRunner
from riaps.rfab.api.utils import make_log_folder


@task(positional = ["mode"],
      help={'mode':' Configure timesync to one of: standalone, master, slave'})
def config(c: Context, mode):
    """Change timesync configuration"""
    kwargs = {'dry':c.config.run.dry,'verbose':c.config.verbose}
    TimeConfig.configure(mode)
    runner = TaskRunner(c.config.hosts,TimeConfig,**kwargs)
    runner.set_log_folder(make_log_folder("time-config"))
    runner.run()

@task
def status(c: Context):
    """Get timesync status"""
    kwargs = {'dry':c.config.run.dry,'verbose':True}
    runner = TaskRunner(c.config.hosts,TimeStatus,**kwargs)
    runner.set_log_folder(make_log_folder("time-status"))
    runner.run()

@task
def restart(c: Context):
    """Restart timesync"""
    kwargs = {'dry':c.config.run.dry,'verbose':c.config.verbose}
    runner = TaskRunner(c.config.hosts,TimeRestart,**kwargs)
    runner.set_log_folder(make_log_folder("time-restart"))
    runner.run()
    
@task
def date(c: Context):
    """Get the system time"""
    kwargs = {'dry':c.config.run.dry,'verbose':True}
    runner = TaskRunner(c.config.hosts,TimeDate,**kwargs)
    runner.set_log_folder(make_log_folder("time-date"))
    runner.run()


@task
def rdate(c: Context):
    """Update the system time"""
    kwargs = {'dry':c.config.run.dry,'verbose':c.config.verbose}
    runner = TaskRunner(c.config.hosts,TimeRdate,**kwargs)
    runner.set_log_folder(make_log_folder("time-rdate"))
    runner.run()


ns = Collection('time')
ns.add_task(config)
ns.add_task(status)
ns.add_task(restart)
ns.add_task(date)
ns.add_task(rdate)