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
    res = api.sys.sudo('apt-get update',c.config.hosts,hide=c.config.hide)
    if len(res.excepted) + len(res.failed) > 0:
        print("ERROR: apt-get update failed")
        res.pretty_print()
        exit(-1)
    if c.config.role in ['control','all']:
        print("Updating control machine...")
        control = api.utils.load_hostfile()['control']
        res_dict = api.riaps_cmds.update_control(control,hide=c.config.hide)
        for pack,res in res_dict.items():
            print(f"Installing {pack} returned ({res.exited}): {res.stdout}")
    if c.config.role in ['remote','all']:
        print("Updating remote machine(s)...")
        remoteGroup = api.utils.load_role(c.config.role)
        res_dict = api.riaps_cmds.update_remote(remoteGroup,hide=c.config.hide)
        for pack, groupGres in res_dict.items():
            print(f"Installing {pack} results:")
            groupGres.pretty_print()

@task(pre=[call(assert_role_in,'remote')],auto_shortflags=False,
      help={'keep-password':'prevents removal of password-authenticated login'})
def updateNodeKey(c: Context, keep_password=False):
    """Rekey the remote nodes with newly generated keys"""
    api_res = api.riaps_cmds.updateNodeKey(c.config.hosts,keep_password,hide=c.config.hide)
    for conn, results in api_res.items():
        print(f"{conn.host}: ",end='')
        if api.helpers.multi_step_print_errors(results):
            print(f"succeeded")


@task
def updateAptKey(c: Context):
    """Update RIAPS apt key"""
    res = api.riaps_cmds.updateAptKey(c.config.hosts,hide=c.config.hide)

@task
def install(c: Context, keepConfig=True):
    """Install RIAPS packages from host"""
    api_res = api.riaps_cmds.install(c.cwd,c.config.hosts,keepConfig,hide=c.config.hide)
    for conn, results in api_res.items():
        print(f"{conn.host}: ",end='')
        if api.helpers.multi_step_print_errors(results):
            print(f"succeeded")

@task(pre=[call(assert_role_in,'remote')],
      help={'keepConfig': "keep RIAPS system config files"})
def uninstall(c: Context, keepConfig=True):
    """Uninstall all RIAPS packages from nodes"""
    api_res = api.riaps_cmds.uninstall(c.config.hosts,keepConfig,c.config.hide)
    for conn, results in api_res.items():
        print(f"{conn.host}: ",end='')
        if api.helpers.multi_step_print_errors(results):
            print(f"succeeded")

@task(pre=[call(assert_role_in,'nodes','remote')])
def reset(c: Context):
    """Kill riaps_, clean, restart riaps_*"""
    api.riaps_cmds.reset(c.config.hosts,c.config.hide)


ns = Collection('riaps')
ns.add_task(update)
ns.add_task(updateNodeKey)
ns.add_task(updateAptKey)
ns.add_task(install)
ns.add_task(uninstall)
ns.add_task(reset)