from invoke import task, Collection, Context
from invoke.tasks import call
from fabric import Group, GroupResult
from fabric.exceptions import GroupException
import socket
from riaps.rfab import api
from .helpers import assert_role_in

@task(pre=[call(assert_role_in,'nodes','remote')])
def start(c: Context):
    """Start service"""
    res = api.deplo.start(c.config.hosts,hide=c.config.hide)
    res.pretty_print()

# @serial
# @task
# @roles('nodes','remote')
# def startSlow(delay=1):
#     """Start service serially with delay:[delay]"""
#     time.sleep(delay)
#     sudo('systemctl start riaps-deplo.service')

@task(pre=[call(assert_role_in,'nodes','remote')])
def startManual(c: Context):
    """Start deplo on hosts without service"""
    res = api.deplo.startManual(c.config.hosts,hide=c.config.hide)
    res.pretty_print()
    # hostname = env.host_string
    # command = ('sudo -E riaps_deplo >~/riaps-' + hostname + '.log 2>&1 &')
    # run(command)

@task(pre=[call(assert_role_in,'nodes','remote')])
def restart(c: Context):
    """Restart service"""
    res = api.deplo.restart(c.config.hosts,hide=c.config.hide)
    res.pretty_print()

@task(pre=[call(assert_role_in,'nodes','remote')])
def stop(c: Context):
    """Stop service"""
    res = api.deplo.stop(c.config.hosts,hide=c.config.hide)
    res.pretty_print()

@task(pre=[call(assert_role_in,'nodes','remote')])
def enable(c: Context):
    """Enable service"""
    res = api.deplo.enable(c.config.hosts,hide=c.config.hide)
    res.pretty_print()

@task(pre=[call(assert_role_in,'nodes','remote')])
def disable(c: Context):
    """Disable service"""
    res = api.deplo.disable(c.config.hosts,hide=c.config.hide)
    res.pretty_print()

@task(pre=[call(assert_role_in,'nodes','remote')],
      help={'n':'number of lines to collect (default: 10)',
            'grep':'arbitrary grep args to filter results, in quotes'})
def status(c: Context, n='10', grep=''):
    """Get systemctl service status"""
    if grep != '':
        grep=" | grep " + grep
    res = api.deplo.status(c.config.hosts,hide=c.config.hide,n=n,grep=grep)
    res.pretty_print()

@task(pre=[call(assert_role_in,'nodes','remote')],
      help={'n':'number of lines to collect (default: 10)',
            'grep':'arbitrary grep args to filter results, in quotes'})
def journal(c: Context, n='10', grep=''):
    """Get journalctl service log"""
    if grep != '':
        grep=" | grep " + grep
    res = api.deplo.journal(c.config.hosts,hide=c.config.hide,n=n,grep=grep)
    res.pretty_print()

ns = Collection('deplo')
ns.add_task(start)
ns.add_task(startManual)
ns.add_task(restart)
ns.add_task(stop)
ns.add_task(enable)
ns.add_task(disable)
ns.add_task(status)
ns.add_task(journal)