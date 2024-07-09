from fabric import Group, Connection
from riaps.rfab.api.utils import load_role
from riaps.consts.defs import *
from pathlib import Path
import riaps.rfab.api.deplo as deplo
from invoke.exceptions import UnexpectedExit

from riaps.rfab.api.task import SkipResult,Task
from fabric import Result
from time import sleep


packages = ['riaps-timesync','riaps-pycom']

class UpdateControl(Task):
    def update_timesync(self):
        return self.sudo(f"apt-get install riaps-timesync-$(dpkg --print-architecture) -y")
    
    def update_pycom(self):
        return self.sudo(f"apt-get install riaps-pycom-dev -y")

class UpdateRemote(Task):
    def update_timesync(self):
        return self.sudo(f"apt-get install riaps-timesync-$(dpkg --print-architecture) -y")
    
    def update_pycom(self):
        return self.sudo(f"apt-get install riaps-pycom -y")

class UpdateNodeKey(Task):
    keep_password = None
    ssh_privatekey = Path('/home/riaps/.ssh/id_rsa')
    ssh_key_dir = "/home/riaps/.ssh/"
    etc_key_dir = "/etc/riaps/"
    ssh_cert = Path(ssh_key_dir,str(const.ctrlCertificate))
    ssh_zmqcert = Path(ssh_key_dir,str(const.zmqCertificate))
    riaps_pubkey = Path(etc_key_dir,str(const.ctrlPublicKey))
    riaps_privatekey = Path(etc_key_dir,str(const.ctrlPrivateKey))
    riaps_cert = Path(etc_key_dir,str(const.ctrlCertificate))
    riaps_zmqcert = Path(etc_key_dir,str(const.zmqCertificate))

    @classmethod
    def configure(cls,keep_password: bool):
        if isinstance(keep_password,bool):
            cls.keep_password = keep_password
        else:
            raise TypeError(keep_password)

    def put_ssh(self):
        self.run('[ -e /etc/riaps ]',fail_msg='/etc/riaps doesn\'t exist. Is riaps-pycom installed?')
        res = self.put(self.ssh_privatekey,remote='/home/riaps/.ssh/')
        self.remote_ssh_privatekey_path = Path(res.remote)
        return res

    def cp_ssh(self):
        return self.sudo(f"cp {self.remote_ssh_privatekey_path} {self.riaps_privatekey}")
    
    def chown_riaps_private_key(self):
        return self.sudo(f"chown root:riaps {self.riaps_privatekey}")

    def chmod_riaps_private_key(self):
        return self.sudo(f"chmod 440 {self.riaps_privatekey}")

    def chmod_ssh_private_key(self):
        return self.run(f"chmod 400 {self.remote_ssh_privatekey_path}")

    def gen_pub_key(self):
        return self.sudo(f"ssh-keygen -y -f {self.remote_ssh_privatekey_path} > id_rsa.pub")
    
    def mv_pub_key(self):
        return self.sudo(f"mv id_rsa.pub {self.riaps_pubkey}")

    def add_authorized_key(self):
        return self.sudo(f"cat {self.riaps_pubkey} > /home/riaps/.ssh/authorized_keys")

    def chown_pub_key(self):
        return self.sudo(f"chown root:riaps {self.riaps_pubkey}")

    def chmod_pub_key(self):
        return self.sudo(f"chmod 440 {self.riaps_pubkey}")

    def rm_private_key(self):
        return self.sudo(f"rm {self.remote_ssh_privatekey_path}")

    def put_cert(self):
        res = self.put(self.ssh_cert,remote='.ssh')
        self.remote_ssh_cert_path = Path(res.remote)
        return res

    def cp_cert(self):
        return self.sudo(f"cp {self.remote_ssh_cert_path} {self.riaps_cert}")

    def chown_cert(self):
        return self.sudo(f"chown root:riaps {self.riaps_cert}")

    def chmod_cert(self):
        return self.sudo(f"chmod 440 {self.riaps_cert}")

    def rm_cert(self):
        return self.run(f"rm {self.remote_ssh_cert_path}")
    
    def put_zmq_cert(self):
        res = self.put(self.ssh_zmqcert,remote='.ssh')
        self.remote_zmqcert_path = Path(res.remote)
        return res

    def cp_zmq_cert(self):
        return self.sudo(f"cp {self.remote_zmqcert_path} {self.riaps_zmqcert}")

    def chown_zmq_cert(self):
        return self.sudo(f"chown root:riaps {self.riaps_zmqcert}")
    
    def chmod_zmq_cert(self):
        return self.sudo(f"chmod 444 {self.riaps_zmqcert}")

    def rm_zmq_cert(self):
        return self.sudo(f"rm {self.remote_zmqcert_path}")

    def remove_password(self):
        cmd = 'passwd -q -d riaps'
        if self.keep_password is None:
            self.logger.warn("keep_password was not configured! Defaulting to true. Password access still possible")
            self.keep_password = True
        if self.keep_password:
            return SkipResult(self.connection,cmd,"keep_password is set, skipping...")
        return self.sudo(cmd)
        
class UpdateAptKey(Task):
    def run_update(self):
        return self.sudo('wget -qO - https://riaps.isis.vanderbilt.edu/keys/riapspublic.key | apt-key add -')

class UpdateLogConfig(Task):
    def put_log_conf(self):
        return self.put('riaps-log.conf')
    
    def move_log_conf(self):
        return self.sudo("mv riaps-log.conf /etc/riaps/riaps-log.conf")
 
    def chown_log_conf(self):
        return self.sudo("chown root:root /etc/riaps/riaps-log.conf")
    
class UpdateRiapsConfig(Task):
    def put_conf(self):
        self.run('[ -e /etc/riaps ]',fail_msg='Remote dir "/etc/riaps" doesn\'t exist. Is riaps-pycom installed?')
        return self.put('riaps.conf')

    def move_conf(self):
        return self.sudo("mv riaps.conf /etc/riaps/riaps.conf")

    def chown_conf(self):
        return self.sudo("chown root:root /etc/riaps/riaps.conf")
    

class TimesyncInstallTask(Task):
    pkg_folder = None
    log_folder = None
    clean: bool = None

    @classmethod
    def configure(cls,package_folder,install_log_folder,clean: bool):
        pkg_folder = Path(package_folder)
        if pkg_folder.is_dir():
            cls.pkg_folder = pkg_folder
        else:
            raise NotADirectoryError(pkg_folder)
        
        log_folder = Path(install_log_folder)
        if not log_folder.is_dir():
            raise NotADirectoryError(log_folder)
        cls.log_folder = log_folder

        if isinstance(clean,bool):
            cls.clean = clean
        else:
            raise TypeError(clean)

    def get_arch(self):
        res = self.run('dpkg --print-architecture')
        self.arch = res.stdout.strip()
        self.timesync = f"riaps-timesync-{self.arch}.deb"
        #Hack to simplify following steps...
        return SkipResult(self.connection,"Set packages to install",f"Timesync: {self.timesync}")
    
    def put_timesync(self):
        filepath = Path(self.pkg_folder,self.timesync)
        if not filepath.exists():
            raise UnexpectedExit(SkipResult(self.connection,"",f"{self.timesync} isn't in {self.pkg_folder}, skipping transfer...",exited=-1))
        res = self.put(filepath)
        self.remote_timesync = res.remote
        return res
    
    def install_timesync(self):
        keep = '--force-confold' if self.clean else '--force-confnew'
        self.log_filename = f"riaps-install-{self.timesync}.log"
        cmd = f"dpkg {keep} -i {self.remote_timesync} > {self.log_filename}"
        return self.sudo(cmd)

    def retrieve_timesync_logs(self):
        return self.get(self.log_filename,f"{self.log_folder}/{self.connection.host}-{self.timesync}")

class TimesyncUninstallTask(Task):
    controlhost = "riaps-VirtualBox.local"
    purge = None

    @classmethod
    def configure(cls,purge: bool):
        cls.purge = purge

    def get_arch(self):
        if self.purge is None:
            raise Exception("TimesyncUninstallTask was not configure(d)")
        res = self.run('dpkg --print-architecture')
        self.arch = res.stdout.strip()
        self.timesync = f"riaps-timesync-{self.arch}"
        return SkipResult(self.connection,"Set packages to uninstall",f"timesync: {self.timesync}")

    def uninstall_timesync(self):
        cmd = f"apt-get remove -y {self.timesync}"
        return self.sudo(cmd)

    def purge_timesync(self):
        if self.purge:
            return self.sudo(f"dpkg --purge {self.timesync}")
        return SkipResult(self.connection,"Not set to purge dpkg, skipping...","")
    
class PycomInstallTask(Task):
    controlhost = 'riaps-VirtualBox.local'
    pkg_folder = None
    log_folder = None
    clean = None

    @classmethod
    def configure(cls,package_folder,install_log_folder,clean):
        pkg_folder = Path(package_folder)
        if pkg_folder.is_dir():
            cls.pkg_folder = pkg_folder
        else:
            raise NotADirectoryError(pkg_folder)
        
        log_folder = Path(install_log_folder)
        if not log_folder.is_dir():
            raise NotADirectoryError(log_folder)
        cls.log_folder = log_folder

        if isinstance(clean,bool):
            cls.clean = clean
        else:
            raise TypeError(clean)

    def get_arch(self):
        res = self.run('dpkg --print-architecture')
        self.arch = res.stdout.strip()
        pycom = 'riaps-pycom'
        if self.connection.host == PycomInstallTask.controlhost:
            pycom += '-dev'
        self.pycom = pycom + '.deb'
        if not Path(self.pkg_folder,self.pycom).exists():
            raise UnexpectedExit(SkipResult(self.connection,"","",f"{self.pycom} not found in {self.pkg_folder.absolute()}"))
        return SkipResult(self.connection,"Set packages to install",f"pycom: {self.pycom}")

    def put_pycom(self):
        filepath = Path(self.pkg_folder,self.pycom)
        res = self.put(filepath)
        self.remote_file = res.remote
        return res
    
    def install_pycom(self):
        keep = '--force-confnew' if self.clean else '--force-confold'
        self.log_filename = f"riaps-install-{self.pycom}.log"
        cmd = f"dpkg {keep} -i {self.remote_file} > {self.log_filename}"
        return self.sudo(cmd)
    
    def remove_pycom_deb(self):
        cmd = f"rm -r {self.remote_file}"
        return self.sudo(cmd)
    
    def retrieve_pycom_logs(self):
        return self.get(self.log_filename,f"{self.log_folder}/{self.connection.host}-{self.pycom}.log")


class PycomUninstallTask(Task):
    controlhost = "riaps-VirtualBox.local"
    purge = None

    @classmethod
    def configure(cls,purge: bool):
        cls.purge = purge

    def get_arch(self):
        res = self.run('dpkg --print-architecture')
        self.arch = res.stdout.strip()
        self.pycom = 'riaps-pycom'
        if self.connection.host == self.controlhost:
            self.pycom += '-dev'
        return SkipResult(self.connection,"Set packages to uninstall",f"pycom: {self.pycom}")

    def uninstall_pycom(self):
        cmd = f"apt-get remove -y {self.pycom}"
        return self.sudo(cmd)

    def purge_pycom(self):
        if self.purge == True:
            return self.sudo(f"dpkg --purge {self.pycom}")
        return SkipResult(self.connection,"Not set to purge dpkg, skipping...","")


class ResetTask(Task):
    '''stop deplo, find&kill all riaps_ procs, delete state, start deplo

    '''

    def stop_deplo(self):
        return self.sudo('systemctl stop riaps-deplo.service')
    
    def disable_deplo(self):
        return self.sudo('systemctl disable riaps-deplo.service')

    def kill_riaps(self):
        killcmd = 'pkill -SIGKILL "(riaps_deplo|riaps_disco|riaps_actor|riaps_device)"'
        # if zero procs are killed, pgrep exits 1, which raises invoke..UnexpectedExit
        #   warn=True surpresses this
        kwargs = {'warn':True}
        return self.sudo(killcmd,**kwargs)

    def pgrep_riaps(self):
        pgrepcmd = 'pgrep -l "(riaps_deplo|riaps_disco|riaps_actor|riaps_device)"'
        kwargs = {'warn':True}
        res = self.sudo(pgrepcmd,**kwargs)
        if len(res.stdout.strip())>0:
            self.logger.warn(f"Processes still running: {res.stdout.splitlines()}")
        return res

    def getnic(self):
        getniccmd = 'python3 -c \'from riaps.utils.config import Config; c=Config(); print(c.NIC_NAME)\''
        res = self.run(getniccmd)
        self.nic_name = res.stdout.strip()
        return res

    def gethost_last_4(self):
        maccmd = 'ip link show %s | awk \'/ether/ {print $2}\' | sed \'s/://g\'| rev | cut -c 1-4 | rev' % self.nic_name
        res = self.sudo(maccmd)
        self.host_last_4 = res.stdout.strip()
        return res
    
    def lsriapsapps(self):
        res = self.sudo("ls $RIAPSAPPS -I riaps-disco.lmdb -I riaps-apps.lmdb")
        self.applist = res.stdout.split()
        return res
    
    def rmapps(self):
        self.logger.info(f"Apps to rm: {self.applist}")
        a = " ".join([f"$RIAPSAPPS/{app.strip()}/" for app in self.applist])
        rmcmd = f"rm -R {a}"
        if len(self.applist)<1:
            return SkipResult(self.connection,rmcmd,"No apps, skipping...")
        return self.sudo(rmcmd)
    
    def userdel(self):
        cmd = ";".join([f"userdel {app.lower()}{self.host_last_4}" for app in self.applist])
        if len(self.applist)<1:
            return SkipResult(self.connection,cmd,"No users, skipping...")
        return self.sudo(cmd,warn=True)

    def rmlmdbs(self):
        cmd = "rm -r $RIAPSAPPS/riaps-apps.lmdb $RIAPSAPPS/riaps-disco.lmdb"
        return self.sudo(cmd,warn=True)
    
    def enable_deplo(self):
        return self.sudo('systemctl enable riaps-deplo.service')
    
    def start_deplo(self):
        return self.sudo('systemctl start riaps-deplo.service')
    
class SetSecurityTask(Task):
    security_on = None

    @classmethod
    def configure(cls,security_on: bool):
        cls.security_state = 'on' if security_on else 'off'
        return cls

    def check_config(self):
        if self.security_state is None:
            raise Exception("SetSecurityTask.security_on not configured")
        self.run('[ -e /etc/riaps/riaps.conf ]',fail_msg='"/etc/riaps/riaps.conf" doesn\'t exist. Is riaps-pycom installed?')
        result = self.run('grep -n \'^\\s*security\\s*=.*$\' /etc/riaps/riaps.conf',
                          fail_msg='riaps.conf doesn\'t have any "security" line defined! Don\'t trust its contents')
        res = result.stdout.splitlines()
        if len(res) != 1:
            raise Exception(f"riaps.conf didn't find exactly one \"security = (on|off)\" line")
        self.line_num = res[0].split(':')[0]
        return result
    
    def stop_deplo(self):
        return self.sudo('systemctl stop riaps-deplo.service')

    def edit_security(self):
        sed_cmd = f'sed -i \'{self.line_num} s/^\\s*security\\s*=.*$/security = {self.security_state}/g\' /etc/riaps/riaps.conf'
        return self.sudo(sed_cmd)
    
    def start_deplo(self):
        return self.sudo('systemctl start riaps-deplo.service')
