from fabric import Group
from .helpers import *

def config(hosts: Group, mode, hide=True):
    return groupSudo("timesyncctl config "+ mode,hosts,hide=hide)

def status(hosts: Group, hide=True):
    return groupSudo("timesyncctl status",hosts,hide=hide)

def restart(hosts: Group, hide=True):
    return groupSudo("timesyncctl restart",hosts,hide=hide)

def date(hosts: Group, hide=True):
    return groupRun("date",hosts,hide=hide)

def rdate(hosts: Group, hide=True):
    return groupSudo("rdate -s -n -4 time.nist.gov",hosts,hide=hide)