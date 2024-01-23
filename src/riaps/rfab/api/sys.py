from fabric import Group
from .helpers import *

def check(hosts: Group, hide=True) -> RFabGroupResult:
    return groupRun("hostname",hosts,hide=hide)

def shutdown(hosts: Group, when='now', why='',hide=True) -> RFabGroupResult:
    return groupSudo(f"shutdown {when} {why}",hosts,hide=hide)

def reboot(hosts: Group, hide=True) -> RFabGroupResult:
    return groupSudo(f"reboot &",hosts,hide=hide)

sudo = groupSudo
run = groupRun

def put(hosts: Group, local_file, remote_dir):
    return groupPut(local_file, remote_dir,hosts)

def get(hosts: Group, remote_file, local_dir=''):
    return groupGet(remote_file,local_dir,hosts)