'''
Controller: main class of the controller node
Created on Nov 10, 2016

@author: riaps
'''

import os
import sys
import stat
import time
import hashlib
import paramiko
import socket
from os.path import join
import subprocess
from threading import Timer
import functools
import logging
import json
import git
from git import Repo
import datetime
import yaml
import ipaddress
import tempfile
import shutil
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import PKCS1_v1_5
from Cryptodome.Hash import SHA256
from riaps.consts.defs import *
from riaps.utils.ifaces import getNetworkInterfaces
from riaps.utils.config import Config 
from riaps.utils.appdesc import AppDescriptor
from riaps.ctrl.ctrlsrv import ServiceThread, ServiceClient
from riaps.ctrl.ctrlgui import ControlGUIClient
from riaps.ctrl.ctrlcli import ControlCLIClient
from threading import RLock
from riaps.lang.lang import compileModel
from riaps.lang.depl import DeploymentModel
import zmq
import zmq.auth

import gi
import tarfile
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

ctrlLock = RLock()

class RSFTPClient(paramiko.SFTPClient):
    def put_dir(self, source, target):
        ''' Uploads the contents of the source directory to the target path. The
            target directory needs to exists. All subdirectories in source are 
            created under target.
        '''
        for item in os.listdir(source):
            if os.path.isfile(os.path.join(source, item)):
                self.put(os.path.join(source, item), '%s/%s' % (target, item))
            else:
                self.mkdir('%s/%s' % (target, item), ignore_existing=True)
                self.put_dir(os.path.join(source, item), '%s/%s' % (target, item))

    def mkdir(self, path, mode=511, ignore_existing=False):
        ''' Augments mkdir by adding an option to not fail if the folder exists  '''
        try:
            super(RSFTPClient, self).mkdir(path, mode)
        except IOError:
            if ignore_existing:
                pass
            else:
                raise

class Controller(object):
    '''
    Main class of controller - manages everything and maintains global controller state
    '''
    def __init__(self,port,script):
        '''
        Initialize controller object, uses port for accepting connections 
        from clients: deployment services running on RIAPS nodes.
        FOR NOW: it is able to launch only one application
        '''       
        self.logger = logging.getLogger(__name__)
        self.dbase = None
        self.setupIfaces()
        self.port = port
        self.script = script
        self.context = zmq.Context()
        self.endpoint = "inproc://riaps-ctrl"
        self.gui = None
        self.clientMap = { }        # Maps hostIP -> ServiceClient 
        self.riaps_Folder = os.getenv('RIAPSHOME', './')
        self.keyFile = os.path.join(self.riaps_Folder,"keys/" + str(const.ctrlPrivateKey))
        self.certFile = os.path.join(self.riaps_Folder,"keys/" + str(const.ctrlCertificate))
        self.riaps_appName = None   # App name
        self.riaps_model = None     # App model to be launched
        self.riaps_depl = None      # App deployment model to be launched
        self.launchList = []        # List of launch operations
        self.setupHostKeys()

        # (DY) 2-18-2017:
        self.riaps_appInfoDict = dict()     # appName: {appFolder, model, depl}
        
    def setupIfaces(self):
        '''
        Find the IP addresses of the (host-)local and network(-global) interfaces
        '''
        (globalIPs,globalMACs,_globalNames,_localIP) = getNetworkInterfaces()
        try:
            assert len(globalIPs) > 0 and len(globalMACs) > 0
        except:
            self.logger.error("Error: no active network interface")
            raise
        globalIP = globalIPs[0]
        globalMAC = globalMACs[0]
        self.hostAddress = globalIP
        self.macAddress = globalMAC
        self.nodeName = str(self.hostAddress)
        self.service = None
        
    def startService(self):
        '''
        Launch the RIAPSCONTROL service (in its own thread)
        '''
        self.service = ServiceThread(self.port)
        self.service.setController(self)
        self.service.start()
        time.sleep(0.001)           # Yield to thread to enable 
        
    def startDbase(self):
        '''
        Start the (redis) database
        ''' 
        dbase_config = join(self.riaps_Folder,"etc/redis.conf")
        # Launch the database process
        try: 
            self.logger.info('Launching redis server')
            self.dbase = subprocess.Popen(['redis-server',dbase_config])
        except:
            self.logger.error("Error when starting database: %s", sys.exc_info()[0])
            raise
        
    def startUI(self):
        '''
        Start the GUI (which runs in 
        '''
        if self.script == None:
            self.gui = ControlGUIClient(self.port,self)
        else:
            self.gui = ControlCLIClient(self.port,self,self.script)
        
    def start(self):
        '''
        Start up everything in the controller
        '''
        self.startDbase()
        self.startUI()
        self.startService()
        
    def run(self):
        '''
        Yield control to the main GUI loop. When the loop terminates this operation will return
        '''
        self.gui.run()
            
    def log(self,msg):
        '''
        Log a message on the GUI
        '''
        if self.gui:
            self.gui.log(msg)
        else:
            print(msg)
        
    def stop(self):
        '''
        Stop everything started by this class
        '''
        if self.dbase != None:
            self.dbase.kill()
        if self.service != None:
            self.service.stop()
            
    def updateClient(self,clientName,client,res):
        if not res or res.error:
            self.log('? Query')
            return
        if not self.gui:
            return
        if res.ready:
            value = res.value
            if not value: return
            self.gui.update_node_apps(clientName,value)
        else:
            exe = functools.partial(self.updateClient,  # Keep waiting if result not ready yet
                                    clientName=clientName,client=client,res=res)
            timeout = const.ctrlDeploDelay/1000.0
            Timer(timeout, exe).start()
        
    def queryClient(self,clientName,client):
        '''
        Query the client for apps already running
        '''
        res = client.query()
        self.updateClient(clientName,client,res)
            
    def addClient(self,clientName,client):
        '''
        Add a client object, representing a RIAPS node to the list. The operation is called
        from the service thread, so it is protected by the lock
        '''
        with ctrlLock:
            self.clientMap[clientName] = client
            self.queryClient(clientName,client)
        
    def delClient(self,clientName):
        '''
        Remove a client object, representing a RIAPS node from the list. The operation is called
        from the service thread, so it is protected by the lock
        '''
        with ctrlLock:
            if clientName in self.clientMap:
                del self.clientMap[clientName]
    
    def isClient(self,clientName):
        '''
        Check if the name stands for a known client
        '''
        with ctrlLock:
            res = clientName in self.clientMap
        return res
    
    def getClient(self,clientName):
        '''
        Find a known client by name
        '''
        res = None
        with ctrlLock:
            if clientName in self.clientMap:
                res = self.clientMap[clientName]
        return res

    def killAll(self):
        for client in self.clientMap.values():
            client.kill()
    
    def cleanAll(self):
        for client in self.clientMap.values():
            self.removeAppFromClient(client, appName='')
                
    def setupHostKeys(self):
        # get host key, if we know one
        self.hostKeys = {}
        try:
            self.hostKeys = paramiko.util.load_host_keys(os.path.expanduser(os.path.join('~','.ssh','known_hosts')))
        except IOError:
            try:
                # try ~/ssh/ too, e.g. on windows
                self.hostKeys = paramiko.util.load_host_keys(os.path.expanduser(os.path.join('~','ssh','known_hosts')))
            except IOError:
                pass     

    def addKeyToAgent(self,agent_keys,rsa_private_key):
        if os.path.isfile(rsa_private_key):
            try:
                ki = paramiko.RSAKey.from_private_key_file(rsa_private_key)
                agent_keys=agent_keys + (ki,)
                self.logger.info('added key %s'% rsa_private_key)
            except Exception as e:
                self.logger.error('Failed loading %s' % (rsa_private_key, e))
        return agent_keys

    def authenticate(self,transport,username):
        """
        Attempt to authenticate to the given transport using any of the private
        keys available from an SSH agent or from a local private RSA key file (assumes no pass phrase).
        """
        agent = paramiko.Agent()
        agent_keys = agent.get_keys() 
        rsa_private_key = join(self.riaps_Folder,"keys/" + str(const.ctrlPrivateKey))
        agent_keys=self.addKeyToAgent(agent_keys,rsa_private_key)
        rsa_private_key = os.path.expanduser(os.path.join('~','.ssh',str(const.ctrlPrivateKey)))        
        agent_keys=self.addKeyToAgent(agent_keys,rsa_private_key)
        if len(agent_keys) == 0:
            self.logger.error('no suitable key found.')
            return
        for key in agent_keys:
            self.logger.info('trying user %s ssh-agent key %s' % (username,key.get_fingerprint().hex()))
            try:
                transport.auth_publickey(username, key)
                self.logger.info ('... success!')
                return
            except paramiko.SSHException as e:
                self.logger.info ('... failed! - %s' % str(e))
                
    def startClientSession(self,client):
        hostName = client.name
        hostKey = None
        hostKeyType = None
        if hostName in self.hostKeys:
            hostKeyType = self.hostKeys[hostName].keys()[0]
            hostKey= self.hostKeys[hostName][hostKeyType]
            self.logger.info('Using host key of type %s' % hostKeyType)
        try:
            port = const.ctrlSSHPort
            self.logger.info ('Establishing SSH connection to: %s:%s' % (str(hostName),str(port)))
            t = paramiko.Transport((hostName, port))
            t.start_client()
            self.authenticate(t,Config.TARGET_USER)
            self.logger.info('out of authenticate')
            if not t.is_authenticated():
                self.logger.warning ('RSA key auth failed!') 
                # t.connect(username=username, password=password, hostkey=hostkey)
                return None
            return t
        except Exception as e:
            self.logger.warning('Caught exception: %s: %s' % (e.__class__, e))
            try:
                t.close()
                return None
            except:
                return None
            
    def signPackage(self,keyName, dataName):
        with open(keyName, 'rb') as f: key = f.read()
        with open(dataName, 'rb') as f: data = f.read()
        rsakey = RSA.importKey(key)
        signer = PKCS1_v1_5.new(rsakey)
        digest = SHA256.new()
        digest.update(data)
        return signer.sign(digest)
            
    def buildPackage(self,appName,files,libraries):
        ''' Build a download package in a temporary folder.
        The package contains a tgz file with all the artifacts to be downloaded
        and a signature file.
        '''
        tempDir = tempfile.mkdtemp()                        # Temp folder
        tgz_file = os.path.join(tempDir,appName + '.tgz')   # Construct tgz file
        with tarfile.open(tgz_file,"w:gz") as tar:
            for f in files: tar.add(f,os.path.join(appName,f))
            for l in libraries: tar.add(l,os.path.join(appName,l))
        # Sign package
        rsa_private_key = join(self.riaps_Folder,"keys/" + str(const.ctrlPrivateKey))
        sign = self.signPackage(rsa_private_key, tgz_file)
        sha_file = tgz_file + '.sha256'
        with open(sha_file,'wb') as f: f.write(sign)
        return (tgz_file, sha_file)

    def installClientComplete(self,client,appName,res):
        if not res or res.error:
            self.log('? Install on %s failed' % client.name)
            return
        if res.ready:
            return
        else:
            exe = functools.partial(self.installClientComplete,  # Keep waiting if result not ready yet
                                    client=client,appName=appName,res=res)
            timeout = const.ctrlDeploDelay/1000.0
            Timer(timeout, exe).start()
            
    def downloadAppToClient(self,appName,tgz_file,sha_file,client,resList):

        # Transfer package
        transport = self.startClientSession(client)
        if transport == None:
            return False
        try:
            sftpSession = transport.open_session()
            sftpClient = RSFTPClient.from_transport(transport)
            
            appFolder = self.riaps_appInfoDict[appName]['riaps_appFolder']
            dirRemote = os.path.join(client.appFolder,appName)
           
            appFolderRemote = client.appFolder # os.path.join(client,appFolder)
            for fileName in [tgz_file,sha_file]:
                localFile = fileName
                remoteFile = os.path.join(appFolderRemote, os.path.basename(fileName))                
                self.logger.info ('Copying' + str(localFile) + ' to ' + str(remoteFile))
                sftpClient.put(localFile, remoteFile)
            res = client.install(appName)
            self.installClientComplete(client, appName, res)
            resList += [res]
            
            # Old method = transfer files one by one
#             sftpClient.mkdir(dirRemote,ignore_existing=True)
# 
#             for fileName in files:
#                 isUptodate = False
#                 #localFile = os.path.join(self.riaps_appFolder,fileName)
#                 localFile = os.path.join(appFolder, fileName)
#                 remoteFile = dirRemote + '/' + os.path.basename(fileName)
# 
#                 #if remote file exists
#                 try:
#                     if sftpClient.stat(remoteFile):
#                         localFileData = open(localFile, "rb").read()
#                         remoteFileData = sftpClient.open(remoteFile).read()
#                         md1 = hashlib.md5(localFileData).digest()
#                         md2 = hashlib.md5(remoteFileData).digest()
#                         if md1 == md2:
#                             isUptodate = True
#                             self.logger.info ("Unchanged: %s" % os.path.basename(fileName))
#                         else:
#                             self.logger.info ("Modified: %s" % os.path.basename(fileName))
#                 except:
#                     self.logger.info ("New: %s" % os.path.basename(fileName))
# 
#                 if not isUptodate:
#                     self.logger.info ('Copying' + str(localFile) + ' to ' + str(remoteFile))
#                     sftpClient.put(localFile, remoteFile)
# 
#             for libraryName in libraries:
#                 localDir = os.path.join(self.riaps_appFolder,libraryName)
#                 remoteDir = os.path.join(dirRemote,libraryName)
#                 sftpClient.mkdir(remoteDir,ignore_existing=True)
#                 self.logger.info ('Copying' + str(localDir) + ' to ' + str(remoteDir))
#                 sftpClient.put_dir(localDir,remoteDir)
            # End old method

            transport.close()
            return True
        
        except Exception as e:
            self.logger.warning('Caught exception: %s: %s' % (e.__class__, e))
            try:
                transport.close()
            except:
                pass
            return False

    def downloadApp(self,files,libraries,clients,appName):
        result = True
        (tgz_file, sha_file) = self.buildPackage(appName,files,libraries)
        with ctrlLock:
            resList = []
            for client in clients:
                if client.stale:
                    self.log('S %s',client.name)    # Stale client, we don't deploy
                else:
                    ok = self.downloadAppToClient(appName,tgz_file,sha_file,client,resList)
                    result = result and ok
            for res in resList:
                while not res.ready: time.sleep(0.5)
                value = res.value
                if value == True:
                    self.log('I %s %s' % (client.name,appName))
                else:
                    self.log('? %s on %s: %s' % (appName,client.name,str(value)))
        os.remove(tgz_file)
        os.remove(sha_file)
        return result
                    
    def findClient(self,clientName):
        '''
        Find a client based on its name that can be be an IP address or
        a DNS name. Clients log in with their numeric IP address, but the
        deployment plan may have DNS names.  
        '''
        if clientName in self.clientMap:
            return self.clientMap[clientName]
        else:
            try:
                hostIP = socket.gethostbyname(clientName)   # Note: works only with IPV4
                if hostIP in self.clientMap:
                    return self.clientMap[hostIP]
                else:
                    return None
            except:
                return None
            
    def buildArgs(self,actuals):
        '''
        Build argument list from actual list
        '''
        res = []
        for actual in actuals:
            argName = '--' + str(actual["name"])
            argValue = str(actual["value"])
            res.append(argName)
            res.append(argValue)
        return res
    
    def buildAppDescriptor(self,hosts, network):
        ''' Build an app descriptor file for the app that is being downloaded
        and record the download event in the git repository the app has
        come from (if there is a git repo).
        Generate certs for the app.    
        '''
        url = 'file:///' + os.getcwd()
        mac = self.macAddress
        sha = mac
        host = str(int(ipaddress.IPv4Address(self.hostAddress)))
        dateTime = datetime.datetime.now().isoformat() 
        try:
            repo = Repo(os.getcwd())
            for r in repo.remotes:  # find 1st remote url
                for u in r.urls:
                    url = str(u)
                    break
                break
            commit = repo.head.commit   # find last commit
            sha = commit.hexsha         # use its hash
            # tag last commit as 'deployed'
            path = host + '.' + mac
            ref = commit                # tag refers to last commit
            try:                        # delete old tag (if any)
                repo.delete_tag(repo.tags[path])
            except:
                pass
            _tag = repo.create_tag(path, ref, 'riaps deplo @ %s' % dateTime)
        except git.exc.InvalidGitRepositoryError:
            pass
        home = os.getcwd()

        with open(const.appDescFile,'w') as f:
            yaml.dump(AppDescriptor(url,host,mac,sha,home,hosts,network),f)
        
    def buildDownload(self, appName):
        '''
        Build a download package for the application.
        '''
        noresult = ([],[],[],[])
        download = []
        if appName not in self.riaps_appInfoDict:
            return noresult
        appInfoDict = self.riaps_appInfoDict[appName]
        appNameJSON = appName + ".json"
        
        if ('riaps_model' not in appInfoDict) or ('riaps_depl' not in appInfoDict):
            self.log("Error: Mismatched model or deployment for app '%s'" % appName)
            return noresult
        
        if appName not in appInfoDict['riaps_model']:
            self.log("Error: App '%s' not found in model" % appName)
            return noresult
        else:
            download.append(appNameJSON)
        
        if os.path.isfile(const.logConfFile) and os.access(const.logConfFile, os.R_OK):
            download.append(const.logConfFile)
        
        appObj = appInfoDict['riaps_model'][appName]
        depls = appInfoDict['riaps_depl'].getDeployments()
        #  Network: (ip|'[]') -> [] | [ ('dns' | ip) ]+  
        network = appInfoDict['riaps_depl'].getNetwork()
        
        hosts = []          # List of IP addresses of hosts used by the app
        # Check the all actors are present in the model
        for depl in depls:
            actors = depl['actors']
            for actor in actors:
                actorName = actor["name"]
                if actorName not in appObj['actors']:
                    self.log("Error: Actor '%s' not found in model" % actorName)
                    return noresult
                
        # Collect all app components (python and c++)
        for component in appObj["components"]:
            pyComponentFile = str(component) + ".py"
            ccComponentFile = "lib" + str(component).lower() + ".so"
            if os.path.isfile(pyComponentFile):
                download.append(pyComponentFile)
            if os.path.isfile(ccComponentFile):
                download.append(ccComponentFile)

        # Get capnp files
        entries = os.scandir(self.riaps_appFolder)
        for entry in entries:
            if entry.is_file() and os.path.splitext(entry.name)[1] == '.capnp':
                download.append(entry.name)

        for device in appObj["devices"]:
            pyDeviceFile = str(device) + ".py"
            ccDeviceFile = "lib" + str(device).lower() + ".so"
            if os.path.isfile(pyDeviceFile):
                download.append(pyDeviceFile)
            if os.path.isfile(ccDeviceFile):
                download.append(ccDeviceFile)

        # Collect libraries
        libraries = []
        for library in appObj["libraries"]:
            libraryName = library["name"]
            libraries.append(libraryName)
            
        # Process the deployment and download app #  (ip|[]) -> 'any' | [ ('dns' | ip) ]+  
        clients = set()
        for depl in depls:
            targets = depl['target']
            actors = depl['actors']
            with ctrlLock:
                if targets == []:
                    for clientName in self.clientMap:
                        client = self.clientMap[clientName]
                        clients.add(client)
                else:
                    for target in targets:
                        client = self.findClient(target)    # Use DNS resolver if needed
                        if client != None:
                            clients.add(client)
                        else:
                            self.log('? %s ' % target)
        
        # Hosts on internal network
        for c in clients:
            hosts.append(socket.gethostbyname(c.name))
            
        self.buildAppDescriptor(hosts,network)                      # Add app descriptor 
        download.append(const.appDescFile)
        os.chmod(const.appDescFile,stat.S_IRUSR|stat.S_IWUSR|stat.S_IRGRP|stat.S_IROTH)
        _public,cert = zmq.auth.create_certificates('.', "riaps")   # Add certs
        shutil.move(cert,const.appCertFile)
        download.append(const.appCertFile)
        os.chmod(const.appCertFile,stat.S_IRUSR)
        return (download,libraries,clients,depls)

    def launchByName(self, appName):
        '''
        Launch an app. The model of the app is in self.riaps_model, and the corresponding deployment
        is in self.riaps_depl.
        '''
        download,libraries,clients,depls = self.buildDownload(appName)
        if download == []:
            self.log("* Nothing to download")
            return False
        ok = self.downloadApp(download,libraries,clients,appName)
        if not ok:
            self.log("* App download fault")
            return False
        # Process the deployment and launch all actors.
        appNameJSON = appName + ".json"
        for depl in depls:
            targets = depl['target']
            actors = depl['actors']
            with ctrlLock:
                if targets == []:
                    for clientName in self.clientMap:
                        client = self.clientMap[clientName]
                        client.setupApp(appName,appNameJSON)
                        for actor in actors:
                            actorName = actor["name"]
                            actuals = actor["actuals"]
                            actualArgs = self.buildArgs(actuals)
                            try:
                                client.launch(appName,appNameJSON,actorName,actualArgs)
                                self.launchList.append([client,appName,actorName])
                                self.log("L %s %s %s %s" % (clientName,appName,actorName,str(actualArgs)))
                            except Exception:
                                info = sys.exc_info()[1].args[0]
                                self.log("? %s" % info)
                else:
                    for target in targets:
                        client = self.findClient(target)
                        if client != None:
                            client.setupApp(appName,appNameJSON)
                            for actor in actors:
                                actorName = actor["name"]
                                actuals = actor["actuals"]
                                actualArgs = self.buildArgs(actuals)
                                try:
                                    client.launch(appName,appNameJSON,actorName,actualArgs)
                                    self.launchList.append([client,appName,actorName])
                                    self.log("L %s %s %s %s" % (client.name,appName,actorName,str(actualArgs)))
                                except Exception:
                                    info = sys.exc_info()[1].args[0]
                                    self.log("? %s" % info)
                        else:
                            self.log('? %s ' % target)
        return True

    def haltByName(self, appNameToHalt):
        '''
        Halt (terminate) all launched actors of an app
        '''
        newLaunchList = []
        clientList = []
        for elt in self.launchList:
            client,appName,actorName = elt[0], elt[1], elt[2]
            if appName == appNameToHalt:
                client.halt(appName,actorName)
                self.log("H %s %s %s" % (client.name,appName,actorName))
                clientList.append(client)
            else:
                newLaunchList.append(elt)
        for client in clientList:
            res = client.reclaim(appName)
            if res == None: continue
            if res.error:
                self.log('? Query')
            while not res.ready: time.sleep(1.0)
        self.launchList = newLaunchList

    def addToLaunchList(self,clientName,appName,actorName):
        client = self.clientMap[clientName]
        self.launchList.append([client,appName,actorName])
    
    def isdir(self,sftp,path):
        '''
        Return True  if a remote folder path points to a directory
        '''
        try:
            return S_ISDIR(sftp.stat(path).st_mode)
        except IOError:
            return False

    def rm(self,sftp,path,top=True):
        '''
        Recursively remove the content of a remote directory.  
        '''
        files = sftp.listdir(path)

        for f in files:
            filepath = os.path.join(path, f)
            try:
                sftp.remove(filepath)
            except IOError:
                self.rm(sftp,filepath)
        if top == True:                 # Remove top dir?
            sftp.rmdir(path)
    
    def removeAppFromClient(self,client,appName,files=[],libraries=[]):
        transport = self.startClientSession(client)
        if transport == None:
            return False
        try:
            sftpSession = transport.open_session()
            sftpClient = paramiko.SFTPClient.from_transport(transport)
            
            dirRemote = os.path.join(client.appFolder, appName)
            self.rm(sftpClient,dirRemote,appName != '')
            
            transport.close()
            return True
        except Exception as e:
            self.logger.warning('Caught exception: %s: %s' % (e.__class__, e))
            try:
                transport.close()
            except:
                pass
            return False

    def removeSignature(self):
        '''
        Remove a 'signature' file from the current app folder,
        and remove the corresponding tag from the git repository 
        of the app (if it came from one).  
        '''
        obj = None
        try:
            with open(const.sigFile,'r') as f:
                obj = yaml.load(f)
        except:
            pass
        if obj == None: return
        if not obj.url.startswith('file:///'):
            host,mac = obj.host,obj.mac
            try:
                repo = Repo(os.getcwd())
                path = host + '.' + mac
                try:                        # delete old tag (if any)
                    repo.delete_tag(repo.tags[path])
                except:
                    pass
            except:
                pass
        os.remove(const.sigFile)
            
    def removeApp(self, appName):
        files, libraries, clients, depls = self.buildDownload(appName)
        self.removeSignature()
        with ctrlLock:
            for client in clients:
                if client.stale:
                    self.log('? %s', client.name)  # Stale client, we don't remove
                else:
                    res = client.cleanupApp(appName)
                    while not res.ready: time.sleep(1.0)
                    ok = self.removeAppFromClient(client,appName,files,libraries)
                    if not ok:
                        return False
        return True

    def removeAppByName(self, appName):
        ok = self.removeApp(appName)
        if ok:
            self.log("R %s " % appName)
        else:
            self.log("? %s " % appName)
        del self.riaps_appInfoDict[appName]     # remove app info

    def setAppFolder(self,appFolderPath):
        self.riaps_appFolder = appFolderPath
        os.chdir(appFolderPath)
        
    def compileApplication(self,appModelName,appFolder):
        '''
        Compile an application model (create both the JSON file and the data structure)
        '''
        # .riaps -> compile
        # .json -> load 
        try:
            if appModelName.endswith('.riaps'):
                self.log("Compiling app: %s" % appModelName)
                appInfo = compileModel(appModelName)
                if len(appInfo) < 1:        # empty
                    return None
                appNameKey = list(appInfo.keys())[0]    # Load the first app only
            elif appModelName.endswith('.json'):
                self.log("Loading app model: %s" % appModelName)
                # TODO: Validate that this is a correct RIAPS model file
                fp = open(appModelName,'r')             # Load model file (one app)
                jsonModel = json.load(fp)
                appNameKey = jsonModel['name']
                appInfo = {}
                appInfo[appNameKey] = jsonModel
            else:
                self.log("Must be .riaps or .json: '%s'" % (appModelName))
                self.gui.clearApplication()
                return None
            if appNameKey not in self.riaps_appInfoDict:
                self.riaps_appInfoDict[appNameKey] = dict()
            self.riaps_appInfoDict[appNameKey]['riaps_model'] = appInfo
            self.riaps_appInfoDict[appNameKey]['riaps_appFolder'] = appFolder
            return appNameKey
        except Exception as e:
            self.log("Error while processing '%s':\n%s" % (appModelName,e.args[0]))
            self.gui.clearApplication()
            return None

    def compileDeployment(self,depModelName):
        '''
        Compile a deployment model (create both the JSON file and the data structure)
        '''
        # .riaps -> compile
        # .json -> load 
        if depModelName.endswith('.depl'):
            self.log("Compiling deployment: %s" % depModelName)
        else:
            self.log("Loading deployment model: %s" % depModelName)
        try:
            depInfo = DeploymentModel(depModelName)
            if depInfo is None:
                return None
            appNameKey = depInfo.appName
            if appNameKey not in self.riaps_appInfoDict:
                self.riaps_appInfoDict[appNameKey] = dict()
            self.riaps_appInfoDict[appNameKey]['riaps_depl'] = depInfo
            #print(self.riaps_appInfoDict)
            return appNameKey
        except Exception as e:
            self.log("Error in compiling depl '%s':\n%s" % (depModelName,e.args[0]))
            self.gui.clearDeployment()
            return None




