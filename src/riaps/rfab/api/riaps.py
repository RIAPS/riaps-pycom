from fabric import Group, Connection
from riaps.rfab.api.helpers import *
from riaps.rfab.api.utils import load_role
import os
from riaps.consts.defs import *
from pathlib import Path
import riaps.rfab.api.deplo as deplo
from invoke.exceptions import UnexpectedExit

from riaps.rfab.api.task import SkipResult,Task
from fabric import Result
from time import sleep


packages = ['riaps-timesync','riaps-pycom']

# def update_control(host: str,**kwargs):
#     results = {}
#     for pack in packages:
#         if pack == 'riaps-pycom':
#             package = pack + '-dev'
#         else:
#             package = pack + '-$(dpkg --print-architecture)'
#         results[pack] = Connection(host).sudo(f"apt-get install {package} -y",pty=True,**kwargs)
#     return results

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

# def updateNodeKey(hosts: Group, keep_password=False, hide=True):
#     '''
#     Copies local keys to remote node, saving old ones as backups
#     '''
#     def _updateNodeKey(c: Connection, hide,keepPasswd):
#         etc_key_path = "/etc/riaps/"
#         ssh_key_path = "/home/riaps/.ssh/"
#         ssh_pubkey_name = os.path.join(ssh_key_path, str(const.ctrlPublicKey))
#         # ssh_privatekey_name = os.path.join(ssh_key_path, str(const.ctrlPrivateKey))
#         ssh_privatekey_name = '/home/riaps/.ssh/id_rsa'
#         ssh_cert_name = os.path.join(ssh_key_path, str(const.ctrlCertificate))
#         ssh_zmqcert_name = os.path.join(ssh_key_path, str(const.zmqCertificate))
#         riaps_pubkey_name = os.path.join(etc_key_path, str(const.ctrlPublicKey))
#         riaps_privatekey_name = os.path.join(etc_key_path, str(const.ctrlPrivateKey))
#         riaps_cert_name = os.path.join(etc_key_path, str(const.ctrlCertificate))
#         riaps_zmqcert_name = os.path.join(etc_key_path, str(const.zmqCertificate)) 
#         steps = [
#             [c.put,{},ssh_privatekey_name,'.ssh'],
#             [c.sudo,{},'cp ' + ssh_privatekey_name + ' ' + riaps_privatekey_name],
#             [c.sudo,{},'chown root:riaps ' + riaps_privatekey_name],
#             [c.sudo,{},'chmod 440 ' + riaps_privatekey_name],
#             [c.run,{},'chmod 400 ' + ssh_privatekey_name],
#             [c.sudo,{},'ssh-keygen -y -f ' + ssh_privatekey_name + ' > /home/riaps/.ssh/authorized_keys'],
#             [c.sudo,{},'cp /home/riaps/.ssh/authorized_keys ' + riaps_pubkey_name],
#             [c.sudo,{},'chown root:riaps ' + riaps_pubkey_name],
#             [c.sudo,{},'chmod 440 ' + riaps_pubkey_name],
#             [c.sudo,{},'rm ' + ssh_privatekey_name],

#             [c.put,{},ssh_cert_name,'.ssh'],
#             [c.sudo,{},'cp ' + ssh_cert_name + ' ' + riaps_cert_name],
#             [c.sudo,{},'chown root:riaps ' + riaps_cert_name],
#             [c.sudo,{},'chmod 440 ' + riaps_cert_name],
#             [c.run,{},'rm ' + ssh_cert_name],

#             [c.put,{},ssh_zmqcert_name,'.ssh'],
#             [c.sudo,{},'cp ' + ssh_zmqcert_name + ' ' + riaps_zmqcert_name],
#             [c.sudo,{},'chown root:riaps ' + riaps_zmqcert_name],
#             [c.sudo,{},'chmod 444 ' + riaps_zmqcert_name],
#             [c.run,{},'rm ' + ssh_zmqcert_name],
#         ]
#         if keepPasswd == False:
#             steps.append([c.sudo,{},'passwd -q -d riaps'])

#         return run_multiple_steps(steps)
#     return {conn:_updateNodeKey(conn,hide,keep_password) for conn in hosts}

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
        res = self.put(self.ssh_privatekey,remote='.ssh')
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
        return self.sudo(f"cat {self.riaps_pubkey} >> /home/riaps/.ssh/authorized_keys")

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
        
# def updateAptKey(hosts: Group, hide=True):
    # return groupSudo('wget -qO - https://riaps.isis.vanderbilt.edu/keys/riapspublic.key | apt-key add -')


class UpdateAptKey(Task):
    def run_update(self):
        return self.sudo('wget -qO - https://riaps.isis.vanderbilt.edu/keys/riapspublic.key | apt-key add -')


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

    # def put_pycom(self):
    #     filepath = Path(self.file_dir,self.pycom)
    #     if not filepath.exists():
    #         return SkipResult(self.connection,"",f"{self.pycom} isn't in {self.file_dir}, skipping transfer...",exited=-1)
    #     return self.put(filepath)
    
    # def install_pycom(self):
    #     put_pycom_res = self.results.get("put_pycom")
    #     if isinstance(put_pycom_res,SkipResult):
    #         return SkipResult(self.connection,"","Pycom wasn't transferred, skipping install...")
    #     remote_file = put_pycom_res.remote
    #     pycom_filename = self.pycom
    #     keep = '--force-confold' if self.clean else '--force-confnew'
    #     log_filename = f"riaps-install-{pycom_filename}.log"
    #     cmd = f"dpkg {keep} -i {remote_file} > {log_filename}"
    #     return self.sudo(cmd)
    
    # def remove_pycom_deb(self):
    #     remote_path = self.results.get('put_pycom').remote
    #     cmd = f"rm -r {remote_path}"
    #     return self.sudo(cmd)
    
    def put_timesync(self):
        timesync_file = self.timesync
        filepath = Path(self.pkg_folder,timesync_file)
        if not filepath.exists():
            raise UnexpectedExit(SkipResult(self.connection,"",f"{timesync_file} isn't in {self.pkg_folder}, skipping transfer...",exited=-1))
        return self.put(filepath) 
    
    def install_timesync(self):
        timesync_filename = self.timesync
        remote_file = self.results.get("put_timesync").remote
        keep = '--force-confold' if self.clean else '--force-confnew'
        self.log_filename = f"riaps-install-{timesync_filename}.log"
        cmd = f"dpkg {keep} -i {remote_file} > {self.log_filename}"
        return self.sudo(cmd)

    def retrieve_timesync_logs(self):
        return self.get(self.log_filename,f"{self.log_folder}/{self.connection.host}-{self.timesync}")


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
        return self.put(filepath)
    
    def install_pycom(self):
        put_pycom_res = self.results.get("put_pycom")
        remote_file = put_pycom_res.remote
        keep = '--force-confnew' if self.clean else '--force-confold'
        log_filename = f"riaps-install-{self.pycom}.log"
        cmd = f"dpkg {keep} -i {remote_file} > {log_filename}"
        return self.sudo(cmd)
    
    def remove_pycom_deb(self):
        remote_path = self.results.get('put_pycom').remote
        cmd = f"rm -r {remote_path}"
        return self.sudo(cmd)
    
    def retrieve_pycom_logs(self):
        log_filename = f"riaps-install-{self.pycom}.log"
        return self.get(log_filename,f"{self.log_folder}/{self.connection.host}-{self.pycom}.log")


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
    

class DevelopmentTask(Task):

    def getnic(self):
        getniccmd = "env"
        # getniccmd = 'source /etc/riaps/env.conf && echo $RIAPSHOME'
        res = self.sudo(getniccmd)
        return res