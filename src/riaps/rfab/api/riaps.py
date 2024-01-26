from fabric import Group, Connection
from .helpers import *
from .utils import load_role
import os
from riaps.consts.defs import *
from pathlib import Path
import riaps.rfab.api.deplo as deplo
from invoke.exceptions import UnexpectedExit

packages = ['riaps-timesync','riaps-pycom']

def update_control(host: str,**kwargs):
    results = {}
    for pack in packages:
        if pack == 'riaps-pycom':
            package = pack + '-dev'
        else:
            package = pack + '-$(dpkg --print-architecture)'
        results[pack] = Connection(host).sudo(f"apt-get install {package} -y",pty=True,**kwargs)
    return results
        
    
def update_remote(hosts: Group, **kwargs) -> dict:
    results = {}
    for pack in packages:
        package = pack + '-$(dpkg --print-architecture)'
        results[pack] = groupRun(f"apt-get install {package} -y",hosts,**kwargs)
    return results

def updateNodeKey(hosts: Group, keep_password=False, hide=True):
    '''
    Copies local keys to remote node, saving old ones as backups
    '''
    def _updateNodeKey(c: Connection, hide,keepPasswd):
        etc_key_path = "/etc/riaps/"
        ssh_key_path = "/home/riaps/.ssh/"
        ssh_pubkey_name = os.path.join(ssh_key_path, str(const.ctrlPublicKey))
        # ssh_privatekey_name = os.path.join(ssh_key_path, str(const.ctrlPrivateKey))
        ssh_privatekey_name = '/home/riaps/.ssh/id_rsa'
        ssh_cert_name = os.path.join(ssh_key_path, str(const.ctrlCertificate))
        ssh_zmqcert_name = os.path.join(ssh_key_path, str(const.zmqCertificate))
        riaps_pubkey_name = os.path.join(etc_key_path, str(const.ctrlPublicKey))
        riaps_privatekey_name = os.path.join(etc_key_path, str(const.ctrlPrivateKey))
        riaps_cert_name = os.path.join(etc_key_path, str(const.ctrlCertificate))
        riaps_zmqcert_name = os.path.join(etc_key_path, str(const.zmqCertificate))        
        steps = [
            [c.put,{},ssh_privatekey_name,'.ssh'],
            [c.sudo,{},'cp ' + ssh_privatekey_name + ' ' + riaps_privatekey_name],
            [c.sudo,{},'chown root:riaps ' + riaps_privatekey_name],
            [c.sudo,{},'chmod 440 ' + riaps_privatekey_name],
            [c.run,{},'chmod 400 ' + ssh_privatekey_name],
            [c.sudo,{},'ssh-keygen -y -f ' + ssh_privatekey_name + ' > /home/riaps/.ssh/authorized_keys'],
            [c.sudo,{},'cp /home/riaps/.ssh/authorized_keys ' + riaps_pubkey_name],
            [c.sudo,{},'chown root:riaps ' + riaps_pubkey_name],
            [c.sudo,{},'chmod 440 ' + riaps_pubkey_name],
            [c.sudo,{},'rm ' + ssh_privatekey_name],
            [c.put,{},ssh_cert_name,'.ssh'],
            [c.sudo,{},'cp ' + ssh_cert_name + ' ' + riaps_cert_name],
            [c.sudo,{},'chown root:riaps ' + riaps_cert_name],
            [c.sudo,{},'chmod 440 ' + riaps_cert_name],
            [c.run,{},'rm ' + ssh_cert_name],
            [c.put,{},ssh_zmqcert_name,'.ssh'],
            [c.sudo,{},'cp ' + ssh_zmqcert_name + ' ' + riaps_zmqcert_name],
            [c.sudo,{},'chown root:riaps ' + riaps_zmqcert_name],
            [c.sudo,{},'chmod 444 ' + riaps_zmqcert_name],
            [c.run,{},'rm ' + ssh_zmqcert_name],
        ]
        if keepPasswd == False:
            steps.append([c.sudo,{},'passwd -q -d riaps'])

        return run_multiple_steps(steps)
    return {conn:_updateNodeKey(conn,hide,keep_password) for conn in hosts}

        
def updateAptKey(hosts: Group, hide=True):
    return groupSudo('wget -qO - https://riaps.isis.vanderbilt.edu/keys/riapspublic.key | apt-key add -')

def install(dir, hosts: Group, keepConfig, **kwargs):
    def _install(c: Connection, package, keep, logfolder, **kwargs):
        if package == 'riaps-pycom':
            if c.host == controlhost:
                package += '-dev'
            package += '.deb'
        else:   
            res = c.run('dpkg --print-architecture',**kwargs)
            if res.exited != 0:
                return [(res, "FAILED AT --PRINT-ARCHITECTURE")]
            a = res.stdout.strip()
            package = f"{package}-{a}.deb"
        if not os.path.exists(package):
            return []
        filename = f"riaps-install-{c.host}-{package}.log"
        steps = [
            [c.put,{},package],
            [c.sudo,kwargs,f"dpkg {keep} -i {package} > {filename}"],
            [c.sudo,kwargs,f"rm -f {package}"],
            [c.get,{},filename,f"{logfolder}/{filename}"]
        ]
        return run_multiple_steps(steps)

    logfolder = Path(os.path.abspath(dir),'logs/')
    print(f"logfile is: {logfolder}")
    if not os.path.exists(logfolder):
        os.mkdir(logfolder)
    controlhost = load_role('control')[0].host
    keep = '--force-confold' if keepConfig else '--force-confnew'
    return {host:_install(host,pack,keep,logfolder,**kwargs) for pack in packages for host in hosts}

def uninstall(hosts: Group, keepConfig, **kwargs):
    def _uninstall(c: Connection,package,keep,**kwargs):
        if package == 'riaps-pycom':
            if c.host == controlhost:
                package += '-dev'
        else:   
            res = c.run('dpkg --print-architecture',**kwargs)
            if res.exited != 0:
                return [(res, "FAILED AT --PRINT-ARCHITECTURE")]
            a = res.stdout.strip()
            package = f"{package}-{a}"

        steps = [
            [c.sudo,kwargs,f"apt-get -s remove -y {package}"],
        ]
        if not keep:
            steps.append([c.sudo,kwargs,f"dpkg --no-act --purge {package}"])
        
        return run_multiple_steps(steps)
    
    controlhost = load_role('control')[0].host
    keep = '--force-confold' if keepConfig else '--force-confnew'
    return {host:_uninstall(host,pack,keepConfig,**kwargs) for pack in reversed(packages) for host in hosts}


def reset(hosts: Group, hide = True):
    #TODO: Verify robustness + error reporting

    def _pgrep_acceptance_test(result: Result):
        if str(result.exited) in ['0','1']:
            return True
        return False

    riapsApps = os.getenv('RIAPSAPPS')
    if riapsApps  == None:
        print("RIAPS Configuration - RIAPSAPPS  is not set, using /home/riaps/riaps_apps")
        riapsApps = '/home/riaps/riaps_apps'

    print("Stopping deplo...")
    deplo.stop(hosts,hide).pretty_print()
    print("Disabling deplo...")
    deplo.disable(hosts,hide).pretty_print()

    res = groupSudo('pkill -SIGKILL "(riaps_deplo|riaps_disco|riaps_actor|riaps_device)"',hosts,test=_pgrep_acceptance_test)
    res.pretty_print()

    def _cleanup(c: Connection, hide=True):
        results = []
        pgrepcmd = 'pgrep -l riaps_'
        try:
            res = c.sudo(pgrepcmd,hide=hide,warn=True)
        except BaseException as e:
            results.append((pgrepcmd,e))
            return results
        if not _pgrep_acceptance_test(res):
            results.append((pgrepcmd,res))
            

        remains = list(filter(lambda x: len(x) > 2, res.stdout.split('\n')))
        print(f"{c.host} still alive: {remains}")

        hnamecmd = 'hostname'
        ok, res = run_step([c.run,{"hide":hide},hnamecmd])
        if not ok:
            results.append((hnamecmd,res))
            if isinstance(res,BaseException):
                return results
        
        hostname = res.stdout.strip()
        if hostname[0:4] == 'riaps':
            host_last_4 = hostname[-4:]
        else:
            # If it doesn't start with riaps, assume it is a development VM
            # Get last for digits of mac address since that is how apps and users are named.
            getniccmd = 'python3 -c "from riaps.utils.config import Config; c=Config(); print(c.NIC_NAME)"'
            ok, res = run_step([c.sudo,{"hide":hide},getniccmd])
            if not ok:
                results.append((getniccmd,res))
                if isinstance(res,BaseException):
                    return results
            
            nic_name = res.stdout.strip()
            if nic_name != None:
                maccmd = 'ip link show %s | awk \'/ether/ {print $2}\'' % nic_name
                ok, res = run_step([c.sudo,{"hide":hide},maccmd])
                if not ok:
                    results.append((maccmd,res))
                    if isinstance(res, BaseException):
                        return results
                mac = res.stdout.strip()
                host_last_4 = mac[-5:-3] + mac[-2:]
            else:                           # Should have set the NIC_NAME ...
                host_last_4 = '0000'
        lsriapsapps = f"\ls {riapsApps}"
        ok, res = run_step([c.sudo,{"hide":hide},lsriapsapps])
        if not ok:
            results.append((lsriapsapps,res))
            if isinstance(res, BaseException):
                return results
        apps = res.stdout.split()
        apps = list(set(apps).difference(set(['riaps-apps.lmdb','riaps-disco.lmdb'])))
        for app in apps:
            rmcmd = f"rm -R {riapsApps}/{app}/"
            ok, res = run_step([c.sudo,{"hide":hide},rmcmd])
            if not ok:
                results.append((rmcmd,res))
                if isinstance(res, BaseException):
                    return results
                
        rmlmdb = f"rm -r {riapsApps}/riaps-apps.lmbd {riapsApps}/riaps-disco.lmdb"
        def _accept_rm(r: Result):
            return (r.exited in [0,1],r)
        try:
            ok, res = run_step([c.sudo,{"hide":hide},rmlmdb])
            if not ok:
                results.append((rmlmdb,res))
                if isinstance(res, BaseException):
                    return results
        except UnexpectedExit as e:
            r = e.result
            ok, res = _accept_rm(r)
            if not ok:
                results.append((rmlmdb,res))
            
        return results

    for h in hosts:
        print(f"Cleaning up {h.host}: ",end='')
        reslist = _cleanup(h,hide)
        if multi_step_print_errors(reslist):
            print("succeeded")
    print("Enabling deplo...")
    deplo.enable(hosts,hide).pretty_print()
    print("Restarting deplo...")
    deplo.start(hosts,hide)