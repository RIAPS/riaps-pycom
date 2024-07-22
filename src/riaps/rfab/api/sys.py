from fabric import Group
from riaps.rfab.api.task import Task
from pathlib import Path

class SysCheck(Task):
    def sys_check(self):
        return self.sudo("uname -a")

class SysShutdown(Task):
    when = '1'
    why = ''

    @classmethod
    def configure(cls,when,why):
        cls.when = when
        cls.why = why

    def sys_shutdown(self):
        return self.sudo(f"shutdown -h {self.when} {self.why}")

class SysReboot(Task):
    def sys_reboot(self):
        return self.sudo("reboot &")

class SysClearJournal(Task):
    def rotate_logs(self):
        return self.sudo('journalctl --rotate')
        
    def set_vacuum_time(self):
        return self.sudo('journalctl --vacuum-time=1s')

class SysSudo(Task):
    cmd = None

    @classmethod
    def configure(cls,cmd):
        cls.cmd = cmd

    def do_sudo(self):
        if self.cmd is None:
            raise Exception("SysSudo doesn't have a cmd configure(d)")
        return self.sudo(self.cmd)

class SysRun(Task):
    cmd = None

    @classmethod
    def configure(cls,cmd):
        cls.cmd = cmd

    def do_run(self):
        if self.cmd is None:
            raise Exception("SysRun doesn't have a cmd configure(d)")
        return self.run(self.cmd)

class SysPut(Task):
    '''SFTP a file from caller to host(s)
    
    :param hosts: A fabric.Group of Connection objects to "put" to
    :param local_file: Relative path to send to host(s)
    :param remote: Folder
    '''
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

class SysGet(Task):
    '''SFTP a file from host(s) to caller
     '''
    remote_file = None
    local_path = None

    @classmethod
    def configure(cls,remote_file,local_dir='',local_name=''):
        '''Set paths to transfer

        Local folders WILL be created to satisfy local paths.
        :param remote_file: Remote filename relative to SSH user's home dir,
                        Cannot be a path
        :param local_dir: Dir to store transferred file(s) into
        :param local_name: Name for resulting file(s)
        '''
        local_path = "{host}/"
        local_path += local_name if len(local_name)>0 else "{basename}"
        if len(local_dir) > 0:
            local_path = local_dir+"/"+local_path
        cls.remote_file = remote_file
        cls.local_path = local_path

    def do_get(self):
        if self.local_path is None:
            raise Exception("SysGet was never configure(d)")
        return self.get(self.remote_file,self.local_path)
    
class SysArch(Task):
    def get_arch(self):
        return self.run('dpkg --print-architecture')
    
class SysFlushIPTables(Task):
    def flush_iptables(self):
        return self.sudo('iptables --flush')
    

class SysGetConfig(Task):
    logfolder = None

    @classmethod
    def configure(cls, logfolder: Path):
        cls.logfolder = logfolder
        return cls
    
    def clear_file(self):
        if self.logfolder is None:
            raise Exception(f"{self.__class__.__name__}.logfolder not configured")
        self.log = '/tmp/rfab-getsysconfig'
        return self.sudo(f'rm -f {self.log}')

    def get_config(self):
        steps = ['echo "### system"',
            'echo "hostname: " `hostname` ',
            'uname -a ',
            'lsb_release -a ',
            'python3 --version ',
            'echo "### apt packages" ',
            'dpkg -l | grep zmq ',
            'dpkg -l | grep riaps ',
            'echo "### riaps.conf" ',
            'cat /etc/riaps/riaps.conf ',
            'echo "### pip packages" ',
            'pip3 list ',
            'echo "### local libraries" ',
            'ls -l /usr/local/lib/lib* ',
            'echo "### riaps-log.conf" ',
            'cat /etc/riaps/riaps-log.conf ',
            'echo "### redis version" ',
            'redis-server --version ',
            'echo "### redis.conf" ',
            'cat /etc/redis/redis.conf'
            ]
        kwargs={'warn':True} # Ignore invoke.exceptions.UnexpectedExit
        for s in steps:
            self.run(f"{s} >> {self.log}",**kwargs)

        return self.get(remote=self.log,local=f"{self.logfolder}/{self.connection.host}-config.txt")