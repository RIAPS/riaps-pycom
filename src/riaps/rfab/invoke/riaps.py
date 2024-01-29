from invoke import task, Collection, Context
from invoke.tasks import call
from fabric import Group, GroupResult, Result
from fabric.exceptions import GroupException
import socket
from riaps.rfab import api
from .helpers import assert_role_in

@task(pre=[call(assert_role_in,'control','remote','all')])
def update(c: Context):
    """Update RIAPS packages from official release"""
    kwargs = {'dry':c.config.run.dry,'hide':c.config.hide}
    res = api.sys.sudo('apt-get update',c.config.hosts,hide=c.config.hide)
    if len(res.excepted) + len(res.failed) > 0:
        print("ERROR: apt-get update failed")
        res.pretty_print()
        exit(-1)
    if c.config.role in ['control','all']:
        print("Updating control machine...")
        control_group = api.utils.load_role('control')
        control = control_group[0].host
        res_dict = api.riaps.update_control(control,**kwargs)
        for pack,res in res_dict.items():
            print(f"Installing {pack} returned ({res.exited}): {res.stdout}")
    if c.config.role in ['remote','all']:
        print("Updating remote machine(s)...")
        remoteGroup = api.utils.load_role(c.config.role)
        res_dict = api.riaps.update_remote(remoteGroup,**kwargs)
        for pack, groupGres in res_dict.items():
            print(f"Installing {pack} results:")
            groupGres.pretty_print()

@task(pre=[call(assert_role_in,'remote')],auto_shortflags=False,
      help={'keep-password':'prevents removal of password-authenticated login'})
def updateNodeKey(c: Context, keep_password=False):
    """Rekey the remote nodes with newly generated keys"""
    api_res = api.riaps.updateNodeKey(c.config.hosts,keep_password,hide=c.config.hide)
    for conn, results in api_res.items():
        print(f"{conn.host}: ",end='')
        if api.helpers.multi_step_print_errors(results):
            print(f"succeeded")

@task
def updateAptKey(c: Context):
    """Update RIAPS apt key"""
    res = api.riaps.updateAptKey(c.config.hosts,hide=c.config.hide)

@task(help={'keepConfig': "keep RIAPS system config files"})
def install(c: Context, keepConfig=True):
    """Install RIAPS packages from host"""
    kwargs = {'dry':c.config.run.dry,'hide':c.config.hide,'pty':True}
    api_res = api.riaps.install(c.cwd,c.config.hosts,keepConfig,**kwargs)
    for conn, results in api_res.items():
        print(f"{conn.host}: ",end='')
        if api.helpers.multi_step_print_errors(results):
            print(f"succeeded")

@task(pre=[call(assert_role_in,'remote')],
      help={'keepConfig': "keep RIAPS system config files"})
def uninstall(c: Context, keepConfig=True):
    """Uninstall all RIAPS packages from nodes"""
    kwargs = {'dry':c.config.run.dry,'hide':c.config.hide,'pty':True}
    api_res = api.riaps.uninstall(c.config.hosts,keepConfig,**kwargs)
    for conn, results in api_res.items():
        print(f"{conn.host}: ",end='')
        if api.helpers.multi_step_print_errors(results):
            print(f"succeeded")

@task(pre=[call(assert_role_in,'nodes','remote')])
def reset(c: Context):
    """Kill riaps_, clean, restart riaps_*"""
    api.riaps.reset(c.config.hosts,c.config.hide)


ns = Collection('riaps')
ns.add_task(update)
ns.add_task(updateNodeKey)
ns.add_task(updateAptKey)
ns.add_task(install)
ns.add_task(uninstall)
ns.add_task(reset)