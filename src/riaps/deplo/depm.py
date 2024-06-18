'''
Deployment manager service main class
Created on Oct 19, 2016

@author: riaps
'''

import os,signal
import sys
import errno
import time
import json
import hashlib
from os.path import join
from collections import namedtuple
import subprocess
import shutil
import threading
import logging
import traceback
import psutil
import pwd
import functools
import tarfile
import yaml
import socket
import prctl
import importlib

import capnp
from concurrent.futures.thread import ThreadPoolExecutor

import zmq
# from zmq import devices
from riaps.deplo.relay import Relay 

try:
    import cPickle
    pickle = cPickle
except:
    cPickle = None
    import pickle

from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import PKCS1_v1_5
from Cryptodome.Hash import SHA256

from riaps.consts.defs import *
from riaps.utils.sudo import riaps_sudo,is_su
from riaps.utils.config import Config
from riaps.proto import deplo_capnp
from riaps.proto import disco_capnp
from riaps.run.exc import BuildError
from riaps.deplo.resm import ResourceManager
from riaps.deplo.procm import ProcessManager
from riaps.deplo.appdb import AppDbase
from riaps.utils.ifaces import get_unix_dns_ips
from riaps.utils.names import actorIdentity
from riaps.utils.appdesc import AppDescriptor

# Record of the app
DeploAppRecord = namedtuple('DeploAppRecord', 'model hash file home hosts network')
# Record of a user
DeploUserRecord = namedtuple('DeploUserRecord', 'name home uid gid')
# Record of an actor
DeploActorRecord = namedtuple('DeploActorRecord', 
                              'app model actor args zdevice zdeviceCtrl control monitor')
# Record of an device actor
DeploDeviceRecord = namedtuple('DeploDeviceRecord', 
                               'app model type inst args zdevice zdeviceCtrl control monitor')
# Record of an app actor command 
DeploActorCommand = namedtuple('DeploActorCommand', 
                               'app model actor args cmd pid firewall isdevice')
# Record of the disco command
DeploDiscoCommand = namedtuple('DeploDiscoCommand', 'cmd pid args')

IPT_WAIT = ' -w 1'

class DeploymentManager(threading.Thread):
    '''
    Deployment manager (DM) service main class, implemented as a thread 
    '''    
    DISCONAME = 'riaps.disco'
    ERRORMARK = 'Exc:'
    
    def __init__(self,parent,resm,fm):
        threading.Thread.__init__(self,name='DeploymentManager',daemon=False)
        self.logger = logging.getLogger(__name__)
        self.context = parent.context
        self.hostAddress = parent.hostAddress
        self.macAddress = parent.macAddress
        self.suffix = self.macAddress
        self.riapsApps = parent.riapsApps
        self.riapsHome = parent.riapsHome
        self.launchMap = { }            # Map of launched actors
        # self.launchRefs = { }           # Reference count for device actors
        self.mapLock = threading.RLock()          # Lock to protect launchMap
        self.discoLock = threading.RLock()        # Lock to protect disco 
        self.disco = None
        self.dbaseHost = None 
        self.dbasePort = None
        self.fm = fm                    # Fault manager
        self.resm = resm                # Resource manager
        self.procm = ProcessManager(self)
        # self.devm.setProcessManager(self.procm)
        self.appModels = { }            # App models loaded
        self.users = { } 
        self.setupUser(Config.TARGET_USER)
        self.appUser = { }
        self.actors = { }       # Actors started
        self.peerQueue = { }    # Peer messages for actors
        self.devices = { }      # Device actors started
        self.monitors = { }     # Monitors of actor messages
        self.poller = None

        self.riaps_actor_file = self.find_origin('riaps_actor')

        self.riaps_device_file = self.find_origin('riaps_device')       
        
        self.riaps_disco_file = self.find_origin('riaps_disco')
        
        self.depmCommandEndpoint = parent.depmCommandEndpoint
        # self.devmCommandEndpoint = parent.devmCommandEndpoint
        self.procMonEndpoint = parent.procMonEndpoint
        
        self.commandS = { }             # Command sockets (per thread)
        self.callLock = threading.RLock()
        
        self.discoCommand = None
        
        self.executor = ThreadPoolExecutor(max_workers=3)
        self.appDbase = AppDbase()
        self.is_su = is_su()
        self.uuid = None                    # Deployment unique ID (for this deplo process)
        self.started = False
        self.pendingCall = False
        if Config.SECURITY:
            riaps_sudo('iptables -A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT' + IPT_WAIT)  # track conn's
            riaps_sudo('iptables -A INPUT -m conntrack --ctstate INVALID -j DROP' + IPT_WAIT)                # drop invalid state packets
            riaps_sudo('iptables -A INPUT -i lo -j ACCEPT' + IPT_WAIT)                                       # accept lo
            self.dns_ips = get_unix_dns_ips()
        else:
            self.dns_ips = []
    
    def find_origin(self,module_name):
        try:
            spec = importlib.util.find_spec(module_name)
            return spec.origin
        except:
            pass
        return module_name
    
    def getCommand(self,thread):
        if thread in self.commandS:
            return self.commandS[thread]
        else:
            command = self.context.socket(zmq.DEALER)        # Socket to recv commands from main
            command.setsockopt(zmq.RCVTIMEO,const.depmRecvTimeout)
            command.setsockopt_string(zmq.IDENTITY,str(thread))
            command.connect(self.depmCommandEndpoint)
            time.sleep(0.1)
            self.commandS[thread] = command
            return command
        
    def callCommand(self,cmd):
        '''
        Call a command in the DM. Runs in the DeploService background thread that handles the requests 
        coming from riaps_ctrl, but can be called from the main thread (for setDisco).    
        '''        
        with self.callLock:                                     # Lock out other thread (if any) 
            self.logger.info("callCommand: %s" % str(cmd))
            command = self.getCommand(threading.get_native_id())
            reply = None
            command.send_pyobj(cmd)
            while True:
                try:
                    reply = command.recv_pyobj()
                    break
                except zmq.error.ZMQError as e:
                    if e.errno == zmq.EAGAIN:
                        continue
                    else:
                        raise  
            if type(reply) == str and reply.startswith(self.ERRORMARK):
                info = reply[len(self.ERRORMARK):]
                raise BuildError(info)
            return reply
        
    def setupUser(self,user_name):
        '''
        Set up a new user record (with the given user_name). 
        The user must already exist in the OS. 
        '''
        if user_name in self.users: return
        pw_record = pwd.getpwnam(user_name)
        user_record = DeploUserRecord(
                    name = pw_record.pw_name, 
                    home = pw_record.pw_dir, 
                    uid = pw_record.pw_uid, 
                    gid = pw_record.pw_gid)
        self.users[user_name] = user_record
        
    def delUser(self,user_name):
        '''
        Delete the user record. 
        '''
        if user_name == Config.TARGET_USER: return
        if user_name not in self.users: return
        del self.users[user_name]
    
    def makeLdLibEnv(self,os_env,libs=[]):
        '''
        Add an entry to the user environment that sets up
        LD_LIBRARY_PATH to include the library directories (shipped with the app).  
        '''
        if libs != []:
            ld_libs = os.getenv('LD_LIBRARY_PATH')
            if ld_libs != None:
                ld_libs += ':' + ':'.join(str(l) for l in libs)
            else:
                ld_libs = ':'.join(str(l) for l in libs)
            os_env['LD_LIBRARY_PATH'] = ld_libs
        
    def makeUserEnv(self,user_name,ld_libs=[]):
        '''
        Build a dictionary from the user record (belonging to the user name)
        to contain the environment for a new user process (that runs the app actor). 
        '''
        user_env = os.environ.copy()
        user_record = self.users[user_name]
        user_env[ 'HOME'     ]  = user_record.home
        user_env[ 'LOGNAME'  ]  = user_record.name
        user_env[ 'PWD'      ]  = os.getcwd()
        user_env[ 'USER'     ]  = user_record.name
        user_env[ 'RIAPSHOME']  = os.getenv('RIAPSHOME')
        user_env[ 'RIAPSAPPS']  = os.getenv('RIAPSAPPS')
        if ld_libs != []:
            self.makeLdLibEnv(user_env,ld_libs)
        return user_env

    @staticmethod
    def demote(is_su,rt_actor,user_uid,user_gid):
        ''' 
        Demote the user (actor) process from root to user_uid/gid  
        '''
        def result():
            if is_su:
                if rt_actor:
                    prctl.cap_inheritable.sys_nice = True
                    prctl.cap_permitted.sys_nice = True
                    prctl.securebits.keep_caps = True
                    prctl.set_ambient(prctl.CAP_SYS_NICE,True)
                os.setgid(user_gid)
                os.setuid(user_uid)
                if rt_actor:
                    prctl.cap_permitted.limit(prctl.CAP_SYS_NICE)
                    prctl.cap_inheritable.sys_nice = True
                    prctl.cap_permitted.sys_nice = True
                    prctl.cap_effective.sys_nice = True
                    prctl.set_ambient(prctl.CAP_SYS_NICE,True)
        return result
    
    def connectDisco(self):
        '''
        Set up and connect the ZMQ socket for communicating with the 
        Discovery Service. 
        '''        
        if self.discoCommand is None:
            self.discoCommand = self.context.socket(zmq.REQ)           # Socket to command disco
            self.discoCommand.setsockopt(zmq.RCVTIMEO,const.discoEndpointRecvTimeout)
            self.discoCommand.setsockopt(zmq.SNDTIMEO,const.discoEndpointSendTimeout)
            self.discoCommand.connect(const.discoEndpoint)
        
    def startDisco(self):
        '''
        Start the Discovery Service process 
        '''
        self.logger.info("starting disco")
        disco_prog = 'riaps_disco'
        disco_mod = self.riaps_disco_file   # File name for python script riaps_disco.py

        disco_arg1 = '--database'
        disco_arg2 = '%s:%s' % (self.dbaseHost,self.dbasePort)
        user_record = self.users[Config.TARGET_USER]
        user_env = self.makeUserEnv(Config.TARGET_USER)
        user_uid = user_record.uid
        user_gid = user_record.gid
        user_cwd = os.getcwd()
        user_env["PWD"] = user_cwd
        command = [disco_prog,disco_arg1,disco_arg2]
        try:
            self.disco = psutil.Popen(command,
                                      preexec_fn=self.demote(is_su,False,user_uid, user_gid), 
                                      cwd=user_cwd, env=user_env)
        except FileNotFoundError:
            try:
                command = ['python3',disco_mod] + command[1:]
                self.disco = psutil.Popen(command,
                                          preexec_fn=DeploymentManager.demote(is_su,False,user_uid, user_gid), 
                                          cwd=user_cwd, env=user_env)    
            except:
                # traceback.print_exc()
                self.logger.error("Error while starting disco: %s" % sys.exc_info()[0])
                raise
        self.procm.monitor(self.DISCONAME,self.disco)
        self.connectDisco()
        proc = self.disco
        pid = proc.pid
        cmdline = [p.info for p in psutil.process_iter(attrs=['pid','cmdline'])
                   if pid == p.info['pid']][0]['cmdline']
        self.appDbase.setDiscoCommand(DeploDiscoCommand(cmd=cmdline,pid=pid, args=disco_arg2))
        self.logger.info("disco started")


    def setupDisco(self,msg):
        '''
        Set up the Discovery Service.
        If it is not running yet start it (this will also connect to it),
        otherwise connect to it.  
        '''
        assert type(msg) == tuple and len(msg) == 2
        self.dbaseHost, self.dbasePort = msg
        if self.disco == None:
            self.appDbase.setDisco(msg)
            self.startDisco()
        else:
            self.logger.info('disco already started')
            self.connectDisco()
    
    def setupApp(self,msg):
        ''' 
        Set up model and unique user name for app
        '''
        assert type(msg) == tuple and len(msg) == 2
        
        appName,appModelName = msg
        appFolder = join(self.riapsApps, appName)
        appModelPath = join(appFolder, appModelName)
        
        if not os.path.isdir(appFolder):
            raise BuildError('app folder is missing: %s' % appFolder)
        
        # Load the app model
        self.loadModel(appName,appModelPath)
        # Make it unique (to last 4 digits of suffix)
        userName = appName.lower() + self.suffix[-4:]  
        # self.appUser[appName] = userName
        self.fm.setupApp(appName,appFolder)
        self.resm.setupApp(appName,appFolder,userName)  # Adds user 
        userName = self.resm.getUserName(appName)       # resm may revert to default user
        self.appUser[appName] = userName
        self.setupUser(userName)
        self.appDbase.addApp(appName)
        
    def verifyPackage(self,keyName,sigName,dataName):
        '''
        Very the application package (in file 'dataName')
        against the key (in file 'keyName)' and 
        signature (in file 'sigName)  
        '''
        with open(keyName, 'rb') as f: key = f.read()
        with open(sigName,'rb') as f: sig = f.read()
        with open(dataName, 'rb') as f: data = f.read()
        rsakey = RSA.importKey(key)
        signer = PKCS1_v1_5.new(rsakey)
        digest = SHA256.new()
        digest.update(data)
        return signer.verify(digest, sig)
    
    def installPackage(self,msg):
        '''
        Install a downloaded app package
        '''
        assert type(msg) == tuple and len(msg) == 1
        (appName,) = msg
        ok,err = True,None
        try:
            tgz_file = join(self.riapsApps,appName + '.tgz')
            sha_file = tgz_file + '.sha256'
            rsa_public_key = join(self.riapsHome,"keys/" + str(const.ctrlPublicKey))
            ok = self.verifyPackage(rsa_public_key,sha_file,tgz_file)
            assert(ok)
        except:
            ok,err = False,"Error while verifying app '%s'" % appName
    
        if ok:
            while True:
                try:
                    with tarfile.open(tgz_file, "r:gz") as tar:
                        tar.extractall(self.riapsApps+'/')
                        break
                except PermissionError as ex:
                    try:
                        shutil.rmtree(join(self.riapsApps,appName))
                        continue
                    except Exception as ex:
                        self.logger.error("Remove old app failed: %s(%s)" % (str(type(ex)),str(ex.args)))
                        ok, err = False, 'Old app cannot be removed'
                        break
                except Exception as ex:
                    self.logger.error("Extract app failed: %s(%s)" % (str(type(ex)),str(ex.args)))
                    ok, err = False, 'Content extraction failed'
                    break 
        try:
            os.remove(tgz_file)
            os.remove(sha_file)
        except:
            ok, err = False, 'App package removal failed'
        os.sync()
        if not ok: raise BuildError(err)
        return ok
    
    def installApp(self,msg):
        '''
        Install the app whose name is in the message. 
        '''
        reply = self.installPackage(msg)
        return reply
        
    def cleanupApp(self,msg):
        ''' 
        Clean up everything related to an app
        '''
        assert type(msg) == tuple and len(msg) == 1
        (appName,) = msg
        if appName not in self.appModels:
            return
        del self.appModels[appName]
        self.resm.cleanupApp(appName)
        self.fm.cleanupApp(appName)
        self.appDbase.delApp(appName)
        if appName not in self.appUser:
            return
        userName = self.appUser[appName]
        del self.appUser[appName]
        self.delUser(userName)
    
    def cleanupApps(self,msg):
        ''' 
        Clean up all known apps 
        '''
        assert type(msg) == tuple and len(msg) == 0
        for k in self.appModels.keys():
            del self.appModels[k]
            self.appDbase.delApp(k)
        self.resm.cleanupApps()
        self.fm.cleanupApps()
                
    def loadModel(self,appName,modelFileName):
        '''
        Load the (json) model file for the app. 
        Loads the app descriptor file as well amd creats a DeploAppRecord.  
        '''
        try:
            fp = open(modelFileName, 'rb')  
        except IOError as e:
            self.logger.error("I/O error({0}): {1}".format(e.errno, e.strerror))
            raise
        except:
            self.logger.error("Unexpected error:", sys.exc_info()[0])
            raise
        # Check if the app model is already loaded
        _fileHash = 0
        fileData = fp.read()
        fileHash = hashlib.md5(fileData).digest()
        fp.close()
        if appName in self.appModels:   # There is an app with this name
            appRecord = self.appModels[appName]
            appHash = appRecord.hash
            if fileHash == appHash:     # Hash is the same, we have the model loaded
                return
        else:
            pass 
        # Not loaded yet (or new)
        fp = open(modelFileName, 'r')  
        try:
            model = json.load(fp)
        except IOError as e:
            self.logger.error("I/O error({0}): {1}".format(e.errno, e.strerror))
            raise
        except:
            self.logger.error("Unexpected error:", sys.exc_info()[0])
            raise
        home = ''
        network = { }
        hosts = []
        try:
            with open(os.path.join(os.path.dirname(modelFileName),const.appDescFile),'r') as f:
                org = yaml.load(f, Loader=yaml.Loader)
                home = org.home
                network = org.network
                hosts = org.hosts
        except:
            self.logger.error("Error loading app descriptor:%s",str(sys.exc_info()[1]))
        self.appModels[appName] = DeploAppRecord(hash=fileHash, model=model, 
                                                 file=modelFileName, home=home,
                                                 hosts=hosts, network=network)
        fp.close()
    
    def getAppRecord(self,appName):
        '''
        Find the app record with the app name. 
        '''
        if appName not in self.appModels:
            raise BuildError('App "%s" unknown' % appName)
        return self.appModels[appName]
    
    def getAppModel(self,appName):
        '''
        Get the app's model.
        '''
        return self.getAppRecord(appName).model
    
    def getAppHome(self,appName):
        '''
        Get the 'home' (organizational source) of the app.
        '''
        return self.getAppRecord(appName).home
    
    def getAppHosts(self,appName):
        '''
        Get the list of hosts the app is to have access to.
        '''
        return self.getAppRecord(appName).hosts
    
    def getAppNetwork(self,appName):
        '''
        Get the list of the networks the app can have access to/
        '''
        return self.getAppRecord(appName).network
    
    def setupAppSite(self,site,user_name,done,firewall):
        '''
        Allow the app's user to communicate with a site (represented by an IPv4 address)
        '''
        if site in done: return 
        try:
            host = socket.gethostbyname(site)
            cmd = "OUTPUT -d %s -m owner --uid-owner %s -j ACCEPT" % (host,user_name)
            riaps_sudo("iptables -A %s" % cmd  + IPT_WAIT)
            firewall += [cmd]
        except:
            raise BuildError('Error in setting up access to %s for %s' % (site,user_name))
    
    def setupAppDNS (self,user_name,done,firewall):
        '''
        All the app's user to access the available DNS servers.  
        '''
        for dns_ip in get_unix_dns_ips():  
            self.setupAppSite(dns_ip,user_name,done,firewall)
    
    def setupAppNetworkSites(self,sites,user_name,done,firewall):
        '''
        Allow the app's user to access the sites (represented by IPv4 addresses) 
        '''
        if sites is not None:
            if len(sites) == 0: return True  # Node can access any network
            for site in sites:
                if site == 'dns':
                    self.setupAppDNS(user_name, done,firewall)
                else:
                    self.setupAppSite(site,user_name,done,firewall)
        return False
                    
    def setupAppNetwork(self,appName,user_name):
        '''
        Set up an app's network. 
        The app's user will be allowed to communicate through the firewall.  
        '''
        firewall = []
        if not Config.SECURITY: return firewall             # No security
        if user_name == Config.TARGET_USER: return firewall # Don't restrict default target user 
        done = set()
        self.setupAppSite('127.0.0.1',user_name,done,firewall)       # ACCEPT localhost
        sites = self.getAppHosts(appName)                            # ACCEPT riaps peers
        self.setupAppNetworkSites(sites, user_name, done,firewall)
        network = self.getAppNetwork(appName)
        sites = network['[]'] if '[]' in network.keys() else None   # Sites from global list
        if self.setupAppNetworkSites(sites, user_name, done,firewall): return firewall     # Access to any network
        sites = network[self.hostAddress] if self.hostAddress in network.keys() else None
        if self.setupAppNetworkSites(sites, user_name, done,firewall): return firewall     # Access to any network
        host = '0.0.0.0/0'                                 # deny access to all others
        cmd = "OUTPUT -d %s -m owner --uid-owner %s -j DROP" % (host,user_name)
        riaps_sudo("iptables -A %s" % cmd  + IPT_WAIT)
        firewall += [cmd]
        return firewall
    
    def startActor(self,msg):
        '''
        Start an actor of an application 
        '''
        assert type(msg) == tuple and len(msg) == 4
        appName,appModel,actorName,actorArgs = msg
        
        appHome = self.getAppHome(appName)
        
        # Starter
        riaps_prog = 'riaps_actor'

        appFolder = join(self.riapsApps, appName)
        appModelPath = join(appFolder, appModel)
         
        if not os.path.isdir(appFolder):
            raise BuildError('App folder is missing: %s' % appFolder)
    
        rt_actor = self.isRealTime(appName,actorName)
        componentTypes = self.getComponentTypes(appName, actorName)
        if len(componentTypes) == 0:
            self.logger.warning('Actor has no components: %s.%s.' % (appName,actorName))
            # raise BuildError('Actor has no components: %s.%s.' % (appName,actorName))
        for componentType in componentTypes:
            # Look up the Python version first
            pyFilePath = join(appFolder, componentType + '.py')
            if os.path.isfile(pyFilePath): continue
            # Look up the C++version 
            ccFilePath = join(appFolder, 'lib' + componentType.lower() + '.so')
            if not os.path.isfile(ccFilePath):
                raise BuildError('Implementation of component %s is missing' % componentType)

        self.resm.addActor(appName, actorName, self.getActorModel(appName, actorName))
        self.fm.addActor(appName, actorName, self.getActorModel(appName, actorName))
        riaps_mod = self.riaps_actor_file   #  File name for python script 'riaps_actor.py'
    
        userName = self.appUser[appName]
        user_record = self.users[userName]
        user_ld_libs = self.getAppLibs(appName)
        user_env = self.makeUserEnv(userName,user_ld_libs)
        
        user_env['PATHS_FROM_ECLIPSE_TO_PYTHON'] = '[[\"%s\",\"%s\"]]' %(appHome,appFolder)
        
        user_uid = user_record.uid
        user_gid = user_record.gid
        user_cwd = appFolder
        user_env["PWD"] = user_cwd
        
        firewall = self.setupAppNetwork(appName,userName)
        
        riaps_arg1 = appName
        riaps_arg2 = appModelPath
        riaps_arg3 = actorName
        command = [riaps_prog,riaps_arg1,riaps_arg2,riaps_arg3]
        for arg in actorArgs:
            command.append(arg)
        if Config.APP_LOGS == 'log':
            logFileName = os.path.join(self.riapsApps,appName,actorName + '.log')
            logFile = open(logFileName ,"ab")
            os.chown(logFileName,user_uid,user_gid)
        else:
            logFile = None
        self.logger.info("Launching %s " % str(command))
        try:
            proc = psutil.Popen(command,
                                preexec_fn=self.demote(self.is_su,rt_actor,user_uid, user_gid), 
                                cwd=user_cwd, env=user_env,
                                stdout=logFile,stderr=subprocess.STDOUT)
            self.logger.info("Launched %s " % str(command))
        except (FileNotFoundError,PermissionError):
            try:
                # if isPython:
                command = ['python3',riaps_mod] + command[1:]
                # else:
                #    command = [riaps_prog] + command[1:]
                proc = psutil.Popen(command,
                                    preexec_fn=self.demote(self.is_su,rt_actor,user_uid, user_gid), 
                                    cwd=user_cwd, env=user_env,
                                    stdout=logFile,stderr=subprocess.STDOUT)
                self.logger.info("Launched %s " % str(command))
            except:
                # traceback.print_exc()
                self.logger.error("Error while starting actor: %s -- %s" % (command,sys.exc_info()[0]))
                raise BuildError("Actor failed to start [imm]: %s.%s " % (appName,actorName))
        try:
            rc = proc.wait(const.depmStartTimeout)
        except psutil.TimeoutExpired:
            rc = None
        if rc != None:
            raise BuildError("Actor terminated: %s.%s [%r]" % (appName,actorName,rc))
        
        pid = proc.pid
        cmdline = [p.info for p in psutil.process_iter(attrs=['pid','cmdline']) 
                   if pid == p.info['pid']][0]['cmdline']
                   
        self.resm.startActor(appName, actorName, proc)
        self.fm.startActor(appName, actorName, proc)
        
        key = str(appName) + "." + str(actorName)
        with self.mapLock:
            self.launchMap[key] = proc
            self.actors[key] = DeploActorRecord(app=appName, model=appModel, actor=actorName, args = actorArgs, 
                                                zdevice=None, zdeviceCtrl=None, control = None, monitor = None)
            self.peerQueue[key] = [ ]
        self.appDbase.addAppActor(appName, DeploActorCommand(app=appName, model=appModel, actor=actorName,args=actorArgs,
                                                             cmd=cmdline,pid=pid,firewall=firewall,isdevice=False))
        self.procm.monitor(key,proc)
        self.logger.info("Started %s" % key)

    def getActorModel(self,appName,actorName):
        model = self.getAppModel(appName)
        
        if actorName in model["actors"]:
            actorModel = model["actors"][actorName]
        elif actorName in model["devices"]:
            actorModel = model["devices"][actorName]    # TODO:needs a proper actor model
        else:
            raise BuildError('Actor "%s" unknown' % actorName)
        
        return actorModel

    def getAppLibs(self,appName):
        model = self.getAppModel(appName)
        app_libs = []
        libraries = model["libraries"]
        for lib in libraries:
            app_libs += [lib['name']]
        return app_libs
        
    def isRealTime(self,appName,actorName):
        actorModel = self.getActorModel(appName,actorName)
        return actorModel["real-time"] if "real-time" in actorModel else False
        
    def getComponentTypes(self,appName, actorName):
        '''
        Collects all the component types of an actor.
        '''
        componentTypes = []
        appModel = self.getAppModel(appName)
        componentDefs = appModel["components"]
        deviceDefs = appModel["devices"]
        actorModel = self.getActorModel(appName,actorName)

        for key in actorModel["instances"]:
            compType = actorModel["instances"][key]["type"]
            if compType in componentDefs:           # Component
                componentTypes.append(compType)
            elif compType in deviceDefs:
                componentTypes.append(compType)     # Device component
            else:
                pass                                # Error
            
        return componentTypes
    
    def terminateActor(self,proc,appName,actorName):
        '''
        Terminate actor (runs in a background thread)
        '''
        qualName = str(appName) + "." + str(actorName)
        proc.poll()
        if proc.returncode == None:
            self.logger.info("Terminating %s" % qualName)
            try:          
                proc.terminate()                    # Should check for errors
                proc.wait(const.depmTermTimeout)    # Wait here
                self.logger.info("Actor %s terminated" % qualName)
            except psutil.TimeoutExpired:
                self.logger.info("Actor %s did not terminate - killing it" % qualName)
                self.unRegisterActor(appName,actorName,proc.pid)
                proc.send_signal(signal.SIGKILL)
                time.sleep(1.0)
            except:
                traceback.print_exc()
    
    def undoAppNetwork(self,firewall):
        if not Config.SECURITY: return 
        for cmd in firewall:
            riaps_sudo("iptables -D %s" % cmd  + IPT_WAIT)

    def stopActor(self,appName,actorName):
        '''
        Stop the actor of an application.
        '''
        qualName = str(appName) + "." + str(actorName)
        proc = None
        with self.mapLock:
            # assert qualName in self.launchMap
            if qualName not in self.launchMap:
                self.logger.error('Actor %s has no process' % qualName)
                return
            proc = self.launchMap[qualName]
            del self.launchMap[qualName]
        
        assert proc != None
        if qualName not in self.actors:
            self.logger.error('Actor %s has not been started' % qualName)
            return
        # assert qualName in self.actors      
        
        self.logger.info("Stopping actor %s" % qualName)
        self.resm.stopActor(appName, actorName, proc)
        self.fm.stopActor(appName, actorName, proc)
        self.procm.release(qualName)
        
        self.executor.submit(self.terminateActor,proc,appName,actorName)
        time.sleep(0)
        
        record = self.actors[qualName]
        zdevice = record.zdevice
        if zdevice:
            _control = record.control
            _control.close(); del _control
            _monitor = record.monitor
            self.delMonitor(appName,actorName,_monitor)
            _monitor.close(); del _monitor
            _zdeviceCtrl = record.zdeviceCtrl
            _zdeviceCtrl.send(b'TERMINATE')
            zdevice.join()
            del zdevice  
        del self.actors[qualName]
        
        firewall = self.appDbase.getAppActor(appName, actorName).firewall
        self.undoAppNetwork(firewall)
        self.appDbase.delAppActor(appName, actorName)
            
        self.logger.info("Stop complete: %s" % qualName)

    def haltActor(self,msg):
        '''
        Ask the background thread to stop the actor of an application  
        '''
        assert type(msg) == tuple and len(msg) == 2
        appName,actorName = msg 
        try:
            self.stopActor(appName,actorName)
        except BuildError as buildError:
            self.logger.error(str(buildError.args[1]))
            raise
    
    def unRegisterActor(self,appName,actorName,actorPid):
        '''
        Unregister a dead actor from the disco service
        '''
        with self.discoLock:
            reqt = disco_capnp.DiscoReq.new_message()
            appMessage = reqt.init('actorUnreg')
            appMessage.appName = appName
            appMessage.version = '0.0.0'
            appMessage.actorName = actorName
            appMessage.pid = actorPid
                      
            msgBytes = reqt.to_bytes()
            
            try:
                self.discoCommand.send(msgBytes)
            except Exception as e:
                self.logger.error("Unable to unregister app with discovery: %s" % e.args)
                return
            
            try:
                respBytes = self.discoCommand.recv()
            except Exception as e:
                self.logger.error("No response from discovery service: %s" % e.args)
                return
            
            with disco_capnp.DiscoRep.from_bytes(respBytes) as resp:
                which = resp.which()
                if which == 'actorUnreg':
                    respMessage = resp.actorUnreg
                    status = respMessage.status
                    if status == 'ok':
                        self.logger.info("unregistered '%s.%s'" % (appName,actorName))
                    else:
                        self.logger.error("Bad response from disco service at app unregistration")
                else:
                    self.logger.error("Unexpected response from disco service at app unregistration")

    def queryApps(self):
        reply = {}
        # This should be self.actors 
        for key in self.launchMap.keys():
            appName,actorName = key.split('.',1)
            if key in self.devices: continue
            if appName in reply.keys():
                actors = reply[appName]
                actors += [actorName]
                reply[appName] = actors
            else:
                reply[appName] = [actorName]
        reply = list(reply.items())
        return reply
    
    def reclaimApp(self,msg):
        assert type(msg) == tuple and len(msg) == 1
        appName = msg[0]
        self.resm.reclaimApp(appName)

    def handleCommand(self,msgFrames):
        (identFrame,msgFrame) = msgFrames
        msg = pickle.loads(msgFrame)
        self.logger.info("handleCommand[%r]: %s" % (identFrame,str(msg)))
        reply = 'ok'
        try: 
            cmd = msg[0]
            if cmd == 'launch':             # Launch an actor
                self.startActor(msg[1:])
            elif cmd == "halt":             # Halt an actor
                self.haltActor(msg[1:])
            elif cmd == "setupApp":         # Setup an app
                self.setupApp(msg[1:])
            elif cmd == "cleanupApp":       # Cleanup an app
                self.cleanupApp(msg[1:])
            elif cmd == "cleanupApps":      # Cleanup all apps
                self.cleanupApps(msg[1:])
            elif cmd == "setDisco":         # Set up disco 
                self.setupDisco(msg[1:])
            elif cmd == "query":            # Query running apps
                reply = self.queryApps()
            elif cmd == "reclaim":          # Reclaim app files (for riaps)
                self.reclaimApp(msg[1:])
            elif cmd == "install":          # Install downloaded package
                reply = self.installApp(msg[1:])
            else:
                pass
        except Exception: 
            # traceback.print_exc()
            info = sys.exc_info()
            reply = '%s: %s %s' %(self.ERRORMARK, info[0].__name__,info[1])
            self.logger.error("Error in handleCommand '%s':\n   %s: %s" % (cmd, info[0].__name__, info[1]))
        resp = [identFrame, zmq.Frame(pickle.dumps(reply))]
        self.ctrl.send_multipart(resp)
    
    def kill(self,what,pid):
        self.logger.info("terminating %s [%d]" % (what,pid))
        try:
            os.kill(pid, signal.SIGTERM)
        except OSError as err:
            if err.errno == errno.ESRCH:
                return
        for _cnt in range(3):
            time.sleep(1.0)
            try:
                os.kill(pid,0)
            except OSError as err:
                if err.errno == errno.ESRCH:
                    self.logger.info("terminated [%d]" % pid)
                    return
        self.logger.info("killing [%d]" % pid)
        try:
            os.kill(pid, signal.SIGKILL)
            time.sleep(1.0)
            os.kill(pid,0)
        except OSError as err:
            if err.errno == errno.ESRCH:
                self.logger.info("killed [%d]" % pid)
                return
        
    def stopOrphanDisco(self):
        record = self.appDbase.getDiscoCommand()
        result = (self.dbaseHost,self.dbasePort)
        if record != None:
            cmdline = record.cmd
            pid = record.pid 
            result = tuple(record.args.split(':'))
            infoList = [p.info for p in psutil.process_iter(attrs=['pid','cmdline'])
                        if pid == p.info['pid']]
            for info in infoList:
                if cmdline == info['cmdline']:
                    self.logger.info("stopping orphan disco [%d] '%s'" % (pid,' '.join(cmdline)))
                    self.kill('orphan disco',pid)
                    self.appDbase.delDiscoCommand()
        return result
                    
    def stopOrphanActor(self,record):
        cmdline = record.cmd
        pid,appName,actorName = record.pid, record.app, record.actor
        infoList = [p.info for p in psutil.process_iter(attrs=['pid','cmdline'])
                    if pid == p.info['pid']]
        for info in infoList:
            if cmdline == info['cmdline']:
                self.logger.info("stopping orphan actor [%d] '%s'" % (pid,' '.join(cmdline)))
                self.kill('orphan actor',pid)
        self.appDbase.delAppActor(appName, actorName)
                
    def unregisterOrphanActor(self,record):
        pid,appName,actorName = record.pid, record.app, record.actor
        self.unRegisterActor(appName,actorName,pid)
        
    def recover(self):
        disco = self.appDbase.getDisco()
        apps = self.appDbase.getApps()
        cmds = { } 
        recs = [ ]
        for app in apps:                            # Stop orphan actors 
            acts = self.appDbase.getAppActors(app)
            cmds[app] = acts
            for act in acts:
                self.stopOrphanActor(act)
                recs += [act]
        if disco != None:                           # Recover discovery
            args = self.stopOrphanDisco()
            self.logger.info("recover: disco = %s" % str(disco))
            self.setupDisco(args)             # Try to use old dbase
        for act in recs:                            # Unregister orphan actors from disco
            self.unregisterOrphanActor(act)
        for app in apps:
            appSet = False
            self.logger.info("recover: app = %s" % str(app))
            acts = cmds[app]
            for act in acts:
                appName = str(act.app)
                actName = str(act.actor)
                try:
                    if not appSet:
                        self.setupApp((act.app,act.model))
                        appSet = True
                    self.logger.info("recover: actor = %s.%s" % (appName,actName))
                    if not act.isdevice:
                        self.startActor((act.app,act.model,act.actor,act.args))
                except Exception as exc:
                    self.logger.error("recovery failed: actor = %s.%s with %r" % (appName,actName,exc))
                    self.appDbase.delAppActor(appName,actName)
    
    def addMonitor(self,appName,actorName,sock):
        if self.poller != None:
            self.monitors[(appName,actorName)] = sock
            self.monitors[sock] = (appName,actorName)
            self.poller.register(sock,zmq.POLLIN)
            
    def delMonitor(self,appName,actorName,sock):
        if self.poller != None:
            del self.monitors[(appName,actorName)]
            del self.monitors[sock]
            self.poller.unregister(sock)
        
    def run(self):
        '''
        Main loop of the depl service
        '''
        self.logger.info("starting")
        # self.printApps()
        try:
            # Server socket for client requests
            self.server = self.context.socket(zmq.REP)  
            endpoint = const.deplEndpoint
            self.server.bind(endpoint)
            # Control socket to receive commands from main thread
            self.ctrl = self.context.socket(zmq.ROUTER)
            self.ctrl.setsockopt(zmq.ROUTER_MANDATORY,1)
            self.ctrl.bind(self.depmCommandEndpoint)
            # Socket to communicate with procmon threads
            self.procmon = self.context.socket(zmq.ROUTER)        
            self.procmon.bind(self.procMonEndpoint)
            # Socket for communication with fault monitor
            self.fmmon = self.fm.setupFMMon()
            # Deployment-unique ID is coming from the UUID of the zyre p2p network
            self.uuid = self.fm.getUUID()               
            # Socket for communication with NIC manager
            self.nicmon = self.fm.setupNICMon()
            # Poller for commands, requests, and procmon messages             
            self.poller = zmq.Poller()                   
            self.poller.register(self.server,zmq.POLLIN)
            self.poller.register(self.ctrl,zmq.POLLIN)
            self.poller.register(self.procmon,zmq.POLLIN)
            self.poller.register(self.fmmon,zmq.POLLIN)
            self.poller.register(self.nicmon,zmq.POLLIN)
            # Map of clients
            self.clients = { }  
            # Event for termination
            self.terminated = threading.Event()     # Event flag to signal termination
            self.terminated.clear()
            self.logger.info("running")
            self.started = True
        # 
        except:
            self.logger.error("start failed")
            self.stop()
            raise
        self.recover()
        while True:
            if self.terminated.is_set(): break
            sockets = dict(self.poller.poll(1000.0)) # Poll client messages, with timeout 1 sec
            if len(sockets) == 0:                    # If no message but timeout expired, 
                if self.terminated.is_set(): 
                    break                           # break out if terminated
            toDelete = []           
            for s in sockets:
                if s == self.ctrl:                  # Handle commands from main
                    msgFrames = self.ctrl.recv_multipart()
                    self.handleCommand(msgFrames)
                elif s == self.server:              # Handle client requests
                    msg = self.server.recv()
                    self.handleClient(msg)
                elif s == self.procmon:             # Handle procmon messages
                    self.handleProcmon()
                elif s == self.fmmon:               # Handle fault monitor messages
                    self.handleFMMon()
                elif s == self.nicmon:              # Handle NIC monitor messages
                    self.handleNICMon()
                else:
                    if s in self.monitors:
                        (appName,actorName) = self.monitors[s]
                        msgBytes = s.recv()
                        self.handleActorMessage(appName,actorName,msgBytes)
                    else:
                        self.logger.info("unknown socket")
                        try:
                            _discard = s.recv()
                        except:
                            pass
                toDelete += [s]
            for s in toDelete:
                del sockets[s]                
        self.stop()
    
            
    def handleClient(self,msgBytes):
        '''
        Handle a message from a client (i.e. an actor) 
        '''
        self.logger.info("handleClient")
        try:
            with deplo_capnp.DeplReq.from_bytes(msgBytes) as msg:
                which = msg.which()
                if which == 'actorReg':
                    self.handleActorReg(msg)
                elif which == 'deviceGet':
                    self.handleDeviceReq(msg)
                elif which == 'deviceRel':
                    self.handleDeviceRel(msg)
                elif which == 'reportEvent':
                    self.handleReportEvent(msg)
                else:
                    pass
        except: 
            info = sys.exc_info()
            self.logger.error("Error in handleClient '%s': %s %s" % (which, info[0], info[1]))
            traceback.print_exc()


    def setupClient(self,appName,_appVersion,appActorName):
        '''
        Set up a new client of the deplo manager. The client actors are to register with
        the manager using the 'server' (REQ/REP) socket. The manager will then create a dedicated
        (PAIR) socket for the client to connect to. This socket is used as a private communication
        channel between a specific client actor and the service.   
        '''
        sock = self.context.socket(zmq.PAIR)
        port = sock.bind_to_random_port('tcp://127.0.0.1')
        clientKeyBase = "/" + appName + '/' + appActorName + "/"
        self.clients[clientKeyBase] = sock
        clientKeyLocal = clientKeyBase + self.macAddress
        self.clients[clientKeyLocal] = port
        clientKeyGlobal = clientKeyBase + self.hostAddress
        self.clients[clientKeyGlobal] = port
        sock.close()
        time.sleep(0.1)
        return port
    
    def binder(self):
        binder = self.context.socket(zmq.REQ)
        iface = 'tcp://127.0.0.1'
        port = binder.bind_to_random_port(iface)
        binder.close()
        return port
    
    def handleActorReg(self,msg):
        '''
        Handle the registration of an application actor with the service. 
        '''
        actReg = msg.actorReg
        appName = actReg.appName
        appVersion = actReg.version   
        appActorName = actReg.actorName
        isDevice = actReg.isDevice
    
        self.logger.info("handleActorReg: %s %s %s" 
                         % (appName, appActorName, '[device]' if isDevice else ''))
        
        qualName = str(appName) + "." + str(appActorName)
        deviceTypeName = None
        err = True        
        if qualName in self.launchMap:
            if not isDevice and qualName in self.actors:
                _actorRecord = self.actors[qualName]
                err = False
            elif isDevice and qualName in self.devices:
                _actorRecord = self.devices[qualName]
                deviceTypeName = _actorRecord.type
                err = False
        
        if err:
            self.logger.error('unknown actor: %s - rejected' % qualName)
            rsp = deplo_capnp.DeplRep.new_message()
            rspMessage = rsp.init('actorReg')
            rspMessage.status = 'err'
            rspBytes = rsp.to_bytes()
            self.server.send(rspBytes)   
            return
        
        clientPort = self.setupClient(appName,appVersion,appActorName)
        clientPID  = self.launchMap[qualName].pid
        
        iface = 'tcp://127.0.0.1'
        # zmqDevice = devices.ThreadProxySteerable(zmq.DEALER,zmq.PAIR,zmq.PUB,zmq.PAIR)
        identity = actorIdentity(appName, appActorName, clientPID)
        zmqDevice = Relay(self.context,identity,zmq.DEALER,zmq.PAIR,zmq.PUB,zmq.PAIR)
        self.logger.info("zmqDevice ID = %s" % identity)
        zmqDevice.setsockopt_in(zmq.IDENTITY, identity.encode(encoding='utf_8'))
        # device.setsockopt_in(zmq.RCVTIMEO,const.deplEndpointRecvTimeout)
        # device.setsockopt_out(zmq.SNDTIMEO,const.deplEndpointSendTimeout)
        zmqDevice.bind_out('%s:%i' % (iface,clientPort)) 
        
        self.resm.addClientDevice(appName,appActorName,zmqDevice)
        
        # Socket for sending control messages to the actor
        actorControl = self.context.socket(zmq.ROUTER)
        actorPort = actorControl.bind_to_random_port(iface)
        zmqDevice.connect_in('%s:%i' % (iface,actorPort))
        
        # Monitoring socket to intercept messages going to the actor
        monPort = self.binder()
        monAddr = '%s:%i' % (iface,monPort)
        zmqDevice.bind_mon(monAddr)

        actorMonitor = self.context.socket(zmq.SUB)
        actorMonitor.setsockopt(zmq.SUBSCRIBE, b'')
        actorMonitor.connect(monAddr)

        ctrlPort = self.binder()
        ctrlAddr = "%s:%i" % (iface, ctrlPort)
        zmqDevice.bind_ctrl(ctrlAddr)
        
        zdeviceCtrl = self.context.socket(zmq.PAIR)
        zdeviceCtrl.connect(ctrlAddr)
         
        self.addMonitor(appName,appActorName,actorMonitor)
        self.fm.addClientDevice(appName,appActorName,zmqDevice)
        
        time.sleep(0.1)
        zmqDevice.start()
        time.sleep(0.1)
        self.logger.info(f"handleActorReg: ({appName},{appActorName}) proxy: {zmqDevice.native_id})")
        
        actorArgs = _actorRecord.args
        appModel = _actorRecord.model
        if isDevice:
            self.devices[qualName] = DeploDeviceRecord(app=appName, model=appModel, 
                                                       type=deviceTypeName, inst=appActorName, args=actorArgs,
                                                       zdevice=zmqDevice, zdeviceCtrl=zdeviceCtrl,
                                                       control = actorControl, monitor = actorMonitor)
        else:
            self.actors[qualName] = DeploActorRecord(app=appName, model=appModel, actor=appActorName, args=actorArgs,
                                                     zdevice=zmqDevice, zdeviceCtrl=zdeviceCtrl,
                                                     control = actorControl, monitor = actorMonitor)
                
        rsp = deplo_capnp.DeplRep.new_message()
        rspMessage = rsp.init('actorReg')
        rspMessage.status = "ok"
        rspMessage.port = clientPort
        rspMessage.uuid = self.uuid.decode()
        rspBytes = rsp.to_bytes()
        self.server.send(rspBytes)
        if not isDevice:
            self.handlePeerQueue(qualName)

    def handlePeerQueue(self,qualName):
        '''
        Process delayed messages from peer message queue
        '''
        with self.mapLock:
            record = self.actors[qualName]
            control = record.control
            assert control != None
            msgs = self.peerQueue[qualName]
            for msg in msgs:
                cmd,appName,actorName,peer = msg
                assert cmd in ('peer+','peer-')
                key = str(appName) + "." + str(actorName)
                assert key == qualName
                msg = deplo_capnp.DeplCmd.new_message()
                msgMessage = msg.init('peerInfoMsg')
                msgMessage.peerState = 'on' if cmd == 'peer+' else 'off'
                msgMessage.uuid = peer.decode()
                msgBytes = msg.to_bytes()
                payload = zmq.Frame(msgBytes)
                pid = self.launchMap[qualName].pid
                identity = actorIdentity(appName, actorName, pid)
                header = identity.encode(encoding='utf-8')
                control.send_multipart([header,payload])
            self.peerQueue[qualName] = []
        
    def startDevice(self,appName,appModel,typeName, instName, actorArgs):
        '''
        Start a device actor for an application 
        '''
        key = str(appName) + "." + str(instName)
        # with self.mapLock:
        #     if key in self.launchMap:
        #         self.launchRefs[key] += 1 
        #         return
        
        appHome = self.getAppHome(appName)
        
        # Starter 
        riaps_prog = 'riaps_device'      #
        
        riaps_mod = self.riaps_device_file  # Module file name for script 
        
        appFolder = join(self.riapsApps,appName)
        appModelPath = join(appFolder,appModel)
        
        if not os.path.isdir(appFolder):
            raise BuildError('App folder is missing: %s' % appFolder)
        
        componentType = typeName 
        # Look up the Python version first
        pyFilePath = join(appFolder, componentType + '.py')
        if os.path.isfile(pyFilePath):
            pass                # Use the Python implementation
        else:                   # Find C++ implementation
            ccFilePath = join(appFolder, 'lib' + componentType.lower() + '.so')
            if not os.path.isfile(ccFilePath):
                raise BuildError('Implementation of component %s is missing' % componentType)
        
        self.resm.addActor(appName, instName, self.getActorModel(appName, typeName))
        self.fm.addActor(appName, instName, self.getActorModel(appName, typeName))
        
        dev_env = os.environ.copy()          
        
        dev_env['PATHS_FROM_ECLIPSE_TO_PYTHON'] = '[[\"%s\",\"%s\"]]' %(appHome,appFolder)
           
        app_libs = self.getAppLibs(appName)
        self.makeLdLibEnv(dev_env,app_libs)
        dev_env["PWD"] = appFolder
               
        riaps_arg1 = appName 
        riaps_arg2 = appModelPath
        riaps_arg3 = typeName
        riaps_arg4 = instName
        command = [riaps_prog,riaps_arg1,riaps_arg2,riaps_arg3,riaps_arg4]
        for arg in actorArgs:
            command.append(arg)
        if Config.APP_LOGS == 'log':
            logFileName = os.path.join(self.riapsApps,appName,instName + '.log')
            logFile = open(logFileName ,"ab")
        else:
            logFile = None
        self.logger.info("Launching %s " % str(command))
        try:
            proc = psutil.Popen(command,cwd=appFolder,env=dev_env, 
                                stdout=logFile, stderr=subprocess.STDOUT)
        except FileNotFoundError:
            try:
                command = ['python3',riaps_mod] + command[1:]
                proc = psutil.Popen(command,
                                        cwd=appFolder,env=dev_env,
                                        stdout=logFile, stderr=subprocess.STDOUT)
            except:
                if self.logger.level >= logging.info: 
                    traceback.print_exc()
                self.logger.error("Error while starting device: %s -- %s" % (command,sys.exc_info()[0]))
                raise BuildError("Device failed to start: %s" % (appName,instName))
        try:
            rc = proc.wait(const.depmStartTimeout)
        except:
            rc = None
        if rc != None:
            raise BuildError("Device failed to start: %s " % (command,))
        
        pid = proc.pid
        cmdline = [p.info for p in psutil.process_iter(attrs=['pid','cmdline']) 
                   if pid == p.info['pid']][0]['cmdline']
                   
        self.resm.startActor(appName, instName, proc)
        self.fm.startActor(appName, instName, proc)
        
        key = str(appName) + "." + str(instName)
        with self.mapLock:
            self.launchMap[key] = proc
            # self.launchRefs[key] = 1
            self.devices[key] = DeploDeviceRecord(app=appName, model=appModel, 
                                                  type=typeName, inst=instName, args=actorArgs, 
                                                  zdevice=None, zdeviceCtrl=None, control = None, monitor = None)
        self.appDbase.addAppActor(appName, DeploActorCommand(app=appName, model=appModel, actor=instName,args=actorArgs,
                                                             cmd=cmdline,pid=pid,firewall=[],isdevice=True))
        self.procm.monitor(key,proc)
        self.logger.info("Started %s" % key)

    def terminateDevice(self,proc,appName,instName):
        '''
        Ultimate operation to terminate a device
        '''
        qualName = str(appName) + "." + str(instName)
        try: 
            proc.terminate()            # Should check for errors
            proc.wait(const.depmTermTimeout)   
            self.logger.info("Device %s terminated" % qualName) # 
        except psutil.TimeoutExpired:
            self.logger.info("Device %s did not stop - killing it" % qualName)
            self.unRegisterActor(appName,instName,proc.pid)    # Clean discovery service
            proc.send_signal(signal.SIGKILL)
            time.sleep(1.0)
        except:
            traceback.print_exc()
    
    def stopDevice(self,appName,instName):
        '''
        Stop a device actor of an application 
        '''        
        qualName = str(appName) + "." + str(instName)
        proc = None
        running = False
        with self.mapLock:
            if qualName not in self.launchMap:
                return
            proc = self.launchMap[qualName]
            res = proc.poll()
            self.logger.info("Device poll: %s"  % str(res))
            running = True if proc.returncode == None else False
            del self.launchMap[qualName]
        if proc != None:
            self.logger.info("Stopping device %s" % qualName)
            assert qualName in self.devices
            self.resm.stopActor(appName, instName, proc)
            self.fm.stopActor(appName, instName, proc)
            self.procm.release(qualName)
            if running:       
                self.executor.submit(self.terminateDevice,proc,appName,instName) 
        self.logger.info("Stopped %s" % qualName)
        
    def handleDeviceReq(self,msg):
        '''
        Handle the request for a device 
        '''
        devGet = msg.deviceGet
        appName = devGet.appName 
        modelName = devGet.modelName
        typeName = devGet.typeName
        instName = devGet.instName
        self.logger.info("handleDeviceReq: %s.%s.%s(%s) " 
                         % (appName,typeName,instName,str(devGet.deviceArgs)))
        
        cmdArgs = []
        for deviceArg in devGet.deviceArgs:
            argName = deviceArg.name
            argValue = deviceArg.value
            cmdArgs.append('--' + argName)
            cmdArgs.append(argValue)
        
        ok = True
        try:
            self.startDevice(appName, modelName, typeName, instName, cmdArgs)
        except BuildError as buildError:
            ok = False
            self.logger.error(str(buildError.args[0]))

        #      
        rsp = deplo_capnp.DeplRep.new_message()
        rspMessage = rsp.init('deviceGet')
        rspMessage.status = "ok" if ok else "err"
        rspBytes = rsp.to_bytes()
        self.server.send(rspBytes)
        self.logger.info("handleDeviceReq: done")

    def handleDeviceRel(self,msg):
        '''
        Handle the release of a device 
        '''
        devRel = msg.deviceRel
        appName = devRel.appName 
        _modelName = devRel.modelName
        typeName = devRel.typeName
        instName = devRel.instName 
        self.logger.info("handleDeviceRel: %s.%s.%s" % (appName,typeName,instName))
        
        ok = True
        try:
            self.stopDevice(appName, instName)
            # self.executor.submit(self.stopDevice,appName,typeName)
        except BuildError as buildError:
            ok = False
            self.logger.error(str(buildError.args[1]))
        #      
        rsp = deplo_capnp.DeplRep.new_message()
        rspMessage = rsp.init('deviceRel')
        rspMessage.status = "ok" if ok else "err"
        rspBytes = rsp.to_bytes()
        self.server.send(rspBytes)
        self.logger.info("handleDeviceRel: done")
    
    def handleReportEvent(self,msg):
        '''
        Handle the event report from actor 
        '''
        repEvt = msg.reportEvent
        appName = repEvt.appName
        _appVersion = repEvt.version   
        actorName = repEvt.actorName
        msg = repEvt.msg

        self.logger.info("handleReportEvent: %s.%s" % (appName,actorName))
        
        ok = True
        try:
            # self.stopDevice(appName, typeName)
            self.logger.error('Event from %s.%s = %s' % (appName,actorName,msg))
        except BuildError as buildError:
            ok = False
            self.logger.error(str(buildError.args[1]))
        #      
        rsp = deplo_capnp.DeplRep.new_message()
        rspMessage = rsp.init('reportEvent')
        rspMessage.status = "ok" if ok else "err"
        rspBytes = rsp.to_bytes()
        self.server.send(rspBytes)
        self.logger.info("handleReportEvent: done")
    
    def stop(self):
        self.logger.info("stopping")
        # Clean up everything
        # Logout from service
        # Kill actors
        toHalt = []
        for key in self.launchMap.keys():
            appName,actorName = key.split('.',1)
            toHalt += [(appName,actorName)]
        for h in toHalt:
            self.haltActor(h)
        # time.sleep(3.0) # Allow actors terminate cleanly
        self.executor.shutdown()    # Ensure all actors have terminated 
        # Cleanup resm 
        self.resm.cleanupApps()
        # Cleanup fm
        self.fm.cleanupApps()
        # Terminate disco
        if self.disco != None:
            self.procm.release(self.DISCONAME)
            self.logger.info("stopping disco")
            self.disco.terminate()
            try:
                self.disco.wait(const.depmTermTimeout)
            except:
                pass
            self.logger.info("disco stopped")
            self.disco = None
        self.appDbase.closeDbase()
        self.logger.info("stopped")
        

    def reinstate(self):
        '''
        Ask actors to reinstate their connections to deplo
        '''
        for qualName,proc in self.launchMap.items():
            proc.poll()
            if proc.returncode == None:
                if qualName in self.actors:
                    record = self.actors[qualName]
                    actName = record.actor
                elif qualName in self.devices:
                    record = self.devices[qualName]
                    actName = record.inst
                appName, control = record.app,record.control
                if control != None: 
                    msg = deplo_capnp.DeplCmd.new_message()
                    msgMessage = msg.init('reinstateCmd')
                    msgMessage.msg = 'doit'
                    msgBytes = msg.to_bytes()
                    payload = zmq.Frame(msgBytes)
                    identity = actorIdentity(appName,actName,proc.pid)
                    header = identity.encode(encoding='utf-8')
                    control.send_multipart([header,payload])
                    self.logger.info('reinstate req to %s' % qualName)
                else:
                    # TODO queue up reinstate command for later send
                    pass
        
    def handleProcmon(self):
        '''
        Handle messages from process monitor: restart disco/actor/device 
        '''
        
        msgFrames = self.procmon.recv_multipart()
        identity = msgFrames[0]
        msg = pickle.loads(msgFrames[1])
        (qualName,) = msg
        self.logger.info(f"handleProcmon: {qualName}")
        if qualName == self.DISCONAME:
            self.logger.info("restarting disco")
            self.startDisco()
            self.reinstate()
        else:
            appName,actorName = qualName.split('.',1)
            if qualName in self.actors:
                record = self.actors[qualName]
                assert appName == record.app and actorName == record.actor                
                appModel = record.model
                actorArgs = record.args
                assert qualName in self.launchMap
                proc = self.launchMap[qualName]
                actorPid = proc.pid    
                self.stopActor(appName, actorName)
                self.unRegisterActor(appName,actorName,actorPid)
                # self.appDbase.delAppActor(appName, actorName)
                msg = (appName,appModel,actorName,actorArgs)
                self.startActor(msg)
            elif qualName in self.devices:
                record = self.devices[qualName]
                appModel = record.model
                typeName = record.type
                instName = record.inst
                actorArgs = record.args
                self.stopDevice(appName,actorName)
                self.startDevice(appName, appModel, typeName, instName, actorArgs)
        py_response = 'ok'
        response = pickle.dumps(py_response)
        payload = zmq.Frame(response)
        self.procmon.send_multipart([identity,payload])
    
    def handleFMMon(self):
        '''
        Handle fault monitor messages (peer changes from the network)
        '''
        msg = self.fmmon.recv_pyobj()
        self.logger.info("handleFMMon: %s " % str(msg))
        cmd,appName,actorName,peer = msg
        assert cmd in ('peer+','peer-')
        qualName = str(appName) + "." + str(actorName)
        with self.mapLock:
            if qualName in self.actors and qualName in self.launchMap:
                record = self.actors[qualName]
                pid = self.launchMap[qualName].pid
                control = record.control
                if control != None:
                    msg = deplo_capnp.DeplCmd.new_message()
                    msgMessage = msg.init('peerInfoMsg')
                    msgMessage.peerState = 'on' if cmd == 'peer+' else 'off'
                    msgMessage.uuid = peer.decode()
                    msgBytes = msg.to_bytes()
                    payload = zmq.Frame(msgBytes)
                    pid = self.launchMap[qualName].pid
                    identity = actorIdentity(appName,actorName,pid)
                    header = identity.encode(encoding='utf-8')
                    control.send_multipart([header,payload])
                else:
                    self.peerQueue[qualName].append(msg)        # TODO: limit the queue size

    
    def handleNICMon(self):
        '''
        Handle NIT state changes messages from NIC monitor
        '''
        msg = self.nicmon.recv_pyobj()
        assert type(msg) == tuple and len(msg) == 1
        flag = msg[0]
        assert flag in ('nic+','nic-')
        self.logger.info("handleNICMon: %s " % str(msg))
        for qualName in self.actors:
            record = self.actors[qualName]
            appName,actName = record.app,record.actor
            control = record.control
            if control == None: continue
            msg = deplo_capnp.DeplCmd.new_message()
            msgMessage = msg.init('nicStateMsg')
            msgMessage.nicState = 'up' if flag == 'nic+' else 'down'
            msgBytes = msg.to_bytes()
            payload = zmq.Frame(msgBytes)
            pid = self.launchMap[qualName].pid
            identity = actorIdentity(appName,actName,pid)
            header = identity.encode(encoding='utf-8')
            control.send_multipart([header,payload])

        
    def handleActorMessage(self,appName,actorName,msgBytes):
        '''
        Handle a  message that has been sent to the actor
        '''
        with deplo_capnp.DeplCmd.from_bytes(msgBytes) as msg:      
            which = msg.which()
            if which == 'resourceMsg':      # Resource violation
                what = msg.resourceMsg.which()
                self.logger.info('handleActorMessage: %s.%s - %s' 
                                 % (appName,actorName,what))
                # TODO: send message to fault manager
            elif which == 'reinstateCmd':   # Reinstate command - ignore
                pass
            elif which == 'nicStateMsg':    # NIC state has changed - ignore
                pass
            elif which == 'peerInfoMsg':    # Peer info has changed - ignore
                pass
            else:
                self.logger.error("unknown msg from monitor: '%s'" % which)
                pass
        
    def terminate(self):
        if self.started:
            self.terminated.set()
