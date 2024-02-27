from fabric import Group
from .helpers import *

def start(hosts: Group, hide=True):
    return groupSudo('systemctl start riaps-deplo.service',hosts,hide=hide)

def startManual(hosts: Group, hide=True):
    return groupSudo('riaps_deplo >~/riaps-$(hostname).log 2>&1 &',hosts,hide=hide,pty=True)

def restart(hosts: Group, hide=True):
    return groupSudo('systemctl restart riaps-deplo.service',hosts,hide=hide)

def stop(hosts: Group, hide=True):
    return groupSudo('systemctl stop riaps-deplo.service',hosts,hide=hide)

def enable(hosts: Group, hide=True):
    return groupSudo('systemctl enable riaps-deplo.service',hosts,hide=hide)

def disable(hosts: Group, hide=True):
    return groupSudo('systemctl disable riaps-deplo.service',hosts,hide=hide)

def status(hosts: Group, hide=True, n='10', grep=''):
    return groupSudo(f"systemctl status riaps-deplo --no-pager -n {n} {grep}",hosts,test= lambda x: x.exited in [0,3], hide=hide)

def journal(hosts: Group, hide=True, n='10', grep=''):
    return groupSudo(f"journalctl -u riaps-deplo.service --no-pager -n {n} {grep}",hosts,hide=hide)
