from invoke import task, Collection, Context
from invoke.tasks import call
from fabric import Group, GroupResult
from fabric.exceptions import GroupException
from riaps.rfab import api


@task(positional = ["mode"],)
def config(c: Context, mode):
    """Change timesync configuration"""
    res = api.timesync.config(c.config.hosts,mode,hide=c.config.hide)
    res.pretty_print()

@task
def status(c: Context):
    """Get timesync status"""
    res = api.timesync.status(c.config.hosts,hide=c.config.hide)
    res.pretty_print()

@task
def restart(c: Context):
    """Restart timesync"""
    res = api.timesync.restart(c.config.hosts,hide=c.config.hide)
    res.pretty_print()
    
@task
def date(c: Context):
    """Get the system time"""
    res = api.timesync.date(c.config.hosts,hide=c.config.hide)
    res.pretty_print()


@task
def rdate(c: Context):
    """Update the system time"""
    res = api.timesync.rdate(c.config.hosts,hide=c.config.hide)
    res.pretty_print()


ns = Collection('time')
ns.add_task(config)
ns.add_task(status)
ns.add_task(restart)
ns.add_task(date)
ns.add_task(rdate)