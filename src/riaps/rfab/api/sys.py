from fabric import Group
from riaps.rfab.api.task import Task
from .helpers import *
from pathlib import Path

# def check(hosts: Group, hide=True) -> RFabGroupResult:
#     return groupRun("hostname",hosts,hide=hide)

class SysCheck(Task):
    def sys_check(self):
        return self.sudo("hostname")

# def shutdown(hosts: Group, when='now', why='',hide=True) -> RFabGroupResult:
#     return groupSudo(f"shutdown {when} {why}",hosts,hide=hide)

class SysShutdown(Task):
    when = 'now'
    why = ''

    @classmethod
    def configure(cls,when,why):
        cls.when = when
        cls.why = why

    def sys_shutdown(self):
        return self.sudo(f"shutdown {self.when} {self.why}")

# def reboot(hosts: Group, hide=True) -> RFabGroupResult:
#     return groupSudo(f"reboot &",hosts,hide=hide)

class SysReboot(Task):
    def sys_reboot(self):
        return self.sudo("reboot &")

# sudo = groupSudo

class SysSudo(Task):
    cmd = None

    @classmethod
    def configure(cls,cmd):
        cls.cmd = cmd

    def do_sudo(self):
        if self.cmd is None:
            raise Exception("SysSudo doesn't have a cmd configure(d)")
        return self.sudo(self.cmd)

# run = groupRun

class SysRun(Task):
    cmd = None

    @classmethod
    def configure(cls,cmd):
        cls.cmd = cmd

    def do_run(self):
        if self.cmd is None:
            raise Exception("SysRun doesn't have a cmd configure(d)")
        return self.run(self.cmd)

def put(hosts: Group, local_file, remote):
    '''SFTP a file from caller to host(s)
    
    :param hosts: A fabric.Group of Connection objects to "put" to
    :param local_file: Relative path to send to host(s)
    :param remote: Folder
    '''
    return groupPut(hosts, local_file, remote)

class SysPut(Task):
    local_file = None
    remote = None

    @classmethod
    def configure(cls,local_file,remote):
        cls.local_file = str(local_file)
        cls.remote = str(remote)

    def do_put(self):
        if self.local_file is None:
            raise Exception("SysPut doesn't have a local_file configure(d)")
        if self.remote is None:
            raise Exception("SysPut doesn't have a remote configure(d)")
        return self.put(self.local_file,remote=self.remote)

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