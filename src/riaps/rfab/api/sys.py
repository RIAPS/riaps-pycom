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

def put(hosts: Group, local_file, remote):
    '''SFTP a file from caller to host(s)
    
    :param hosts: A fabric.Group of Connection objects to "put" to
    :param local_file: Relative path to send to host(s)
    :param remote: Folder
    '''
    return groupPut(hosts, local_file, remote)

def get(hosts: Group, 
        remote_file: str, 
        local_dir: str = '', 
        local_name: str = ''
    ) -> RFabGroupResult: 
    '''SFTP a file from host(s) to caller

    Local folders WILL be created to satisfy local paths.
    
    :param hosts: a fabric.Group of Connection objects to "get" from
    :param remote_file: Remote filename relative to SSH user's home dir,
                        Cannot be a path
    :param local_dir: Dir to store transferred file(s) into
     '''

    local_path = "{host}/"
    local_path += local_name if len(local_name)>0 else "{basename}"
    if len(local_dir) > 0:
        local_path = local_dir+"/"+local_path
    return groupGet(hosts, remote_file,local_path)