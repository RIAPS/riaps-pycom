'''
Resource manager 

Created on Nov 23, 2017

@author: riaps
'''

from cgroupspy import trees
import os
import stat
import time
import signal
import subprocess
import psutil
import logging
import random
from riaps.consts.defs import *
from riaps.run.exc import *
from riaps.utils.sudo import riaps_sudo,is_su
from riaps.utils.config import Config
from butter.eventfd import Eventfd
import traceback
import pwd
from filelock import FileLock
from pwd import getpwnam  
from riaps.deplo.cpumon import CPUMonitorThread
from riaps.deplo.memmon import MemMonitorThread
from riaps.deplo.spcmon import SpcMonitorThread
from riaps.deplo.netmon import NetMonitorThread

class ActorResourceManager(object):
    '''
    Resource manager for an actor
    '''
    def __init__(self,parent,actorName,actorDef):
        self.logger = logging.getLogger(__name__)
        self.parent = parent
        self.context  = self.parent.context
        self.actorName = actorName
        self.cpuCGroup = self.memCGroup = self.netCGroup = None
        self.hasCPU = self.hasMem = self.hasSpace = self.hasNet = self.hasRate = False

        self.cpuMonitor = self.memMonitor = None
        self.spcMonitor = self.parent.spcMonitor
        self.netMonitor = self.parent.netMonitor
        self.managed = 'usage' in actorDef 
        # If no usage spec, ignore
        if not self.managed: return
        self.settings = actorDef['usage']
        # Setup cgroups
        if self.parent.cpuCGroup:
            # CPU
            cpuPath = self.parent.cpuCGroup.path + ('/' + actorName).encode('utf-8')
            cpuNode = self.parent.cgroupTree.get_node_by_path(cpuPath)
            self.cpuCGroup = cpuNode if (cpuNode != None) else self.parent.cpuCGroup.create_cgroup(actorName)
        if self.parent.memCGroup:
            # Memory
            memPath = self.parent.memCGroup.path + ('/' + actorName).encode('utf-8')
            memNode = self.parent.cgroupTree.get_node_by_path(memPath)
            self.memCGroup = memNode if (memNode != None) else self.parent.memCGroup.create_cgroup(actorName)                
        if self.parent.netCGroup:
            # Net 
            netPath = self.parent.netCGroup.path + ('/' + actorName).encode('utf-8')
            netNode = self.parent.cgroupTree.get_node_by_path(netPath)
            self.netCGroup = netNode if (netNode != None) else self.parent.netCGroup.create_cgroup(actorName)    
        # Setup resource monitors
        self.hasCPU = self.setupCPU()
        self.hasMem = self.setupMem()
        self.hasSpace = self.setupSpace()
        if self.hasSpace:
            self.parent.addQuota(self.spcUsage)
        self.hasNet = self.setupNet()
        self.proc = None
        self.started = False
    
    def setupCPU(self):
        if 'cpu' not in self.settings: return False
        self.cpuSettings = self.settings['cpu']
        try:
            self.cpuUsage = self.cpuSettings['use']         # %
            self.cpuInterval = self.cpuSettings['interval'] # msec
            self.cpuMax = self.cpuSettings['max']
        except KeyError:
            return False
        if (self.cpuMax):
            self.cpuMonitor = CPUMonitorThread(self,self.cpuInterval/1000.0,self.cpuUsage)
        else:
            if self.cpuCGroup:
                self.cpuController = self.cpuCGroup.controller
                interval = self.cpuInterval * 1000 # usec 
                interval = 1000 if interval < 1000 \
                                else 1000000 if interval > 1000000 else interval
                quota = self.cpuUsage * 0.01 * interval
                quota = 1000 if quota < 1000 \
                                else 1000000 if quota > 1000000 else quota
                self.cpuController.cfs_period_us = interval    # usec 
                self.cpuController.cfs_quota_us = quota        # usec 
        return True
    
    def setupMem(self):
        if 'mem' not in self.settings: return False
        self.memSettings = self.settings['mem']
        try:
            self.memUsage = self.memSettings['use']
        except KeyError:
            return False
        if self.memCGroup:
            try:
                self.memController = self.memCGroup.controller
                # Hard (OOM) limit - not used
                # self.memController.limit_in_bytes = self.memUsage * 1024 # Value is in kBytes
                efd = Eventfd()
                mem = self.memCGroup
                # Threshold
                mub = mem.full_path.decode('utf-8') + '/memory.usage_in_bytes'
                os.chmod(mub,stat.S_IRUSR) #  | stat.S_IWUSR)
                mub_file = open(mub,'rb')
                
                buf1 = '%d %d %s' % (efd.fileno(),mub_file.fileno(),
                                     "%d" % (self.memUsage * 1024))
                buf1 = buf1.encode('utf-8')
                
                # Detector
                mpl = mem.full_path.decode('utf-8') + '/memory.pressure_level'
                os.chmod(mpl,stat.S_IRUSR) #  | stat.S_IWUSR)
                mpl_file = open(mpl,'rb')
                
                buf2 = '%d %d %s' % (efd.fileno(),mpl_file.fileno(),'low')
                buf2 = buf2.encode('utf-8')        
                
                cgc = mem.full_path.decode('utf-8') + '/cgroup.event_control'
                # os.chmod(cgc,stat.S_IRUSR | stat.S_IWUSR)
                cgc_file = open(cgc,'ab',buffering=0)
        
                _wrl1 = cgc_file.write(buf1)
                _wrl2 = cgc_file.write(buf2)
                
                assert (_wrl1 == len(buf1) and _wrl2 == len(buf2))
                
                os.close(cgc_file.fileno())
                os.close(mpl_file.fileno())
                os.close(mub_file.fileno())
            except:
                traceback.print_exc() 
                return False
            self.memMonitor = MemMonitorThread(self,efd,self.memUsage)
            return True
        else:
            return False

    def setupSpace(self):
        if 'spc' not in self.settings: return False
        self.spcSettings = self.settings['spc']
        try:
            self.spcUsage = self.spcSettings['use']
            return True
        except KeyError:
            self.spcUsage = 0       # No space quota
            return False
        
    def setupNet(self):
        self.hasRate = None
        if 'net' not in self.settings:
            self.logger.info("actor.setupNet: no 'net' setting") 
            return False
        self.netSettings = self.settings['net']
        if 'rate' not in self.netSettings: 
            self.logger.info("actor.setupNet: no 'rate' setting") 
            return False
        self.netRate = self.netSettings['rate'] 
        self.netCeil = self.netSettings['ceil']
        self.netBurst = self.netSettings['burst']
        self.hasRate = True
        if self.netCGroup:
            self.netController = self.netCGroup.controller
            major = self.parent.uid
            parentID = str(major)
            self.actorID = self.parent.nextActorID()
            childID = str(self.actorID)
            minor = self.actorID
            classid = (major << 16) | minor
            self.netController.class_id = classid
            try:
                # tc class add dev enp0s3 parent 1002: classid 1002:2 htb rate 100kbps ceil 110kbps
                cmd = ('tc class add dev %s parent %s: classid %s:%s htb rate %sbps ' \
                % (Config.NIC_NAME,parentID,parentID,childID,self.netRate)) + \
                ("" if self.netCeil == 0 else "ceil %sbps " % (self.netCeil)) + \
                ("" if self.netBurst == 0 else "burst %s" % (self.netBurst))
                _res = riaps_sudo(cmd)
                # tc filter add dev enp0s3 parent 1002:1 protocol ip prio 10 handle 1: cgroup
                cmd = "tc filter add dev %s parent %s:%s protocol ip prio 10 handle %s: cgroup" \
                        % (Config.NIC_NAME,parentID,childID,childID)
                _res = riaps_sudo(cmd)
            except:
                self.logger.info("actor.setupNet: exception while setting'tc'")
                return False
            # Create net monitor here
        else:
            self.logger.info("actor.setupNet: no netCGroup")
            return False
        return True
    
    def addClientDevice(self,device):
        appName = self.parent.appName
        actorName = self.actorName
        self.logger.info('actor.addClientDevice %s.%s' % (appName,actorName))
        if self.hasCPU and self.cpuMonitor != None:
            self.cpuMonitor.addClientDevice(appName,actorName,device)
        if self.hasMem and self.memMonitor != None:
            self.memMonitor.addClientDevice(appName,actorName,device)
        if self.hasSpace and self.spcMonitor != None:
            self.spcMonitor.addClientDevice(appName,actorName,device,self.proc)
        if (self.hasNet or self.hasRate) and self.netMonitor != None:
            self.netMonitor.addClientDevice(appName,actorName,device,self.proc,self.netRate)
    
    def startActor(self,proc):
        # Setup CPU resource monitor
        if self.hasCPU:
            if self.cpuMax:
                self.cpuMonitor.setup(proc)
                if self.cpuMonitor.is_running():
                    self.cpuMonitor.restart()
                else:
                    self.cpuMonitor.start()
            else:
                if self.parent.cpuCGroup:
                    self.cpuController.tasks = [proc.pid]
        if self.hasMem:
            self.memController.tasks = [proc.pid]
            self.memMonitor.setup(proc)
            if self.memMonitor.is_running():
                self.memMonitor.restart()
            else:
                self.memMonitor.start()
        appName = self.parent.appName
        actName = self.actorName
        if self.hasSpace:
            self.parent.spcMonitor.addProc(appName,actName,proc)
        if self.hasNet and self.parent.netMonitor:
            self.netController.tasks = [proc.pid]
            self.parent.netMonitor.addProc(appName,actName,proc)
        self.proc = proc
        self.started = True

    
    def stopActor(self,proc):
        # Stop CPU resource monitor
        if not self.started: return
        if self.hasCPU:
            if self.cpuMax:
                self.cpuMonitor.stop()
            else:
                if self.parent.cpuCGroup:
                    pass # 
        if self.hasMem:
            self.memMonitor.stop()
        appName = self.parent.appName
        actName = self.actorName
        if self.hasSpace:
            self.parent.spcMonitor.delProc(appName,actName,proc)
        if self.parent.netMonitor and (self.hasNet or self.hasRate):
            # self.netController.tasks = remove proc.pid
            self.parent.netMonitor.delProc(appName,actName,proc) 
        self.started = False
    
    def cleanupActor(self):
        # Get rid of monitoring setup
        if self.hasCPU:
            if self.cpuMax:
                if self.cpuMonitor.is_running():
                    self.cpuMonitor.terminate()
                    self.cpuMonitor.join()
                self.cpuMonitor = None
            else:
                if self.parent.cpuCGroup:
                    try:
                        self.parent.cpuCGroup.delete_cgroup(self.actorName)
                    except:
                        pass
        if self.hasMem:
            if self.memMonitor.is_running():
                self.memMonitor.terminate()
                self.memMonitor.join()
            self.memMonitor = None
            if self.parent.memCGroup:
                try:
                    self.parent.memCGroup.delete_cgroup(self.actorName)
                except:
                    pass           
        if self.hasNet:
            if self.parent.netCGroup:
                try:
                    self.parent.netCGroup.delete_cgroup(self.actorName)
                except:
                    pass
            major = self.parent.uid
            parentID = str(major)
            childID = str(self.actorID)
            try:
                # tc class del dev enp0s3 parent 1002: classid 1002:2
                cmd = ('tc class del dev %s parent %s: classid %s:%s' \
                        % (Config.NIC_NAME,parentID,parentID,childID))
                _res = riaps_sudo(cmd)
#                 # tc filter add dev enp0s3 parent 1002:1 protocol ip prio 10 handle 1: cgroup
#                 cmd = "tc filter add dev %s parent %s:%s protocol ip prio 10 handle %s: cgroup" \
#                         % (Config.NIC_NAME,parentID,childID,childID)
#                 _res = riaps_sudo(cmd)
            except:
                pass
                
        
class AppResourceManager(object):
    '''
    Resource manager for an app
    '''
    def __init__(self,parent,appName,appFolder,userName):
        self.logger = logging.getLogger(__name__)
        self.parent = parent
        self.context = self.parent.context
        self.appName = appName
        self.userName = userName
        self.appFolder = appFolder
        self.actors = { }
        self.cgroupTree = parent.cgroupTree
        self.cpuCGroup = None
        self.memCGroup = None
        self.netCGroup = None
        self.actorID = 1
        # Check if cgroup already exist, use it or create a new one. 
        if self.parent.riapsCPU:
            # CPU
            cpuPath = self.parent.riapsCPU.path + ('/' + appName).encode('utf-8')
            cpuNode = self.parent.cgroupTree.get_node_by_path(cpuPath)
            self.cpuCGroup = cpuNode if (cpuNode != None) else self.parent.riapsCPU.create_cgroup(self.appName)
        if self.parent.riapsMem:
            # Memory
            memPath = self.parent.riapsMem.path + ('/' + appName).encode('utf-8')
            memNode = self.parent.cgroupTree.get_node_by_path(memPath)
            self.memCGroup = memNode if (memNode != None) else self.parent.riapsMem.create_cgroup(self.appName)
        # Set up the data space for the app
        self.uid = -1
        try:
            self.uid = getpwnam(self.userName).pw_uid   # Known uid
        except:
            pass
        if self.uid == -1:                              # Unknown uid
            try:
                lock = FileLock("/tmp/riaps.adduser.lock")
                with lock:
                    _res = riaps_sudo('adduser --disabled-login --gecos GECOS --no-create-home %s' % self.userName)
                self.uid = getpwnam(self.userName).pw_uid
            except:
                # traceback.print_exc()
                self.logger.warning('creating app user %s failed' % (self.userName))
                self.userName = Config.TARGET_USER          # Default user
                self.uid = os.getuid()
        _res = riaps_sudo('chown -R %s:%s %s' % (self.userName,self.userName,self.appFolder))
        _res = riaps_sudo('chmod o-rwx %s' % self.appFolder)
        # _res = riaps_sudo('chown %s %s/%s' % (Config.TARGET_USER,self.appFolder,const.appDescFile))
        self.spcUsage = 0
        self.spcMonitor = self.parent.spcMonitor
        # Set up the net limits for the app
        riaps_uid = self.parent.riaps_uid
        try:
        # tc class add dev enp0s3 parent 1000:1000 classid 1000:1001 htb rate 1000kbps ceil 1100kbps
            _res = riaps_sudo('tc class add dev %s parent %s:%s '
                              'classid %s:%s htb rate %s ceil %s'
                              % (Config.NIC_NAME,riaps_uid,riaps_uid,
                                 riaps_uid,self.uid,
                                 Config.NIC_RATE, Config.NIC_CEIL)) # Give the full bandwidth for the app
            # tc qdisc add dev enp0s3 parent 1000:1001 handle 1001: htb
            _res = riaps_sudo('tc qdisc add dev %s parent %s:%s handle %s: htb'
                              % (Config.NIC_NAME,riaps_uid,self.uid,self.uid))
        except:
            pass
        if self.parent.riapsNet:
            # Net cls
            netPath = self.parent.riapsNet.path + ('/' + appName).encode('utf-8')
            netNode = self.parent.cgroupTree.get_node_by_path(netPath)
            self.netCGroup = netNode if (netNode != None) else self.parent.riapsNet.create_cgroup(self.appName)
        else:
            pass
        self.netMonitor = self.parent.netMonitor
            
    def getUserName(self):
        return self.userName
    
    def nextActorID(self):
        res = self.actorID
        self.actorID += 1 
        return res
    
    def addQuota(self,usage):
        self.spcUsage += usage
        if self.userName != Config.TARGET_USER:             # Don't set quotas for the default user
            if self.spcUsage != 0:
                # Assume here that the spcUsage value is in 1024 byte blocks
                try:
                    softblock = int(0.9 * self.spcUsage)
                    hardblock = self.spcUsage
                    softinode = 100000
                    hardinode = 100000
                    command = 'setquota -u %s %d %d %d %d /' % (self.userName,softblock,hardblock,softinode,hardinode)
                    self.logger.info('exec: %s' % command)
                    _res = riaps_sudo(command)
                except:
                    self.logger.warning('setting quota failed')
    
    def delQuota(self):
        if self.userName != Config.TARGET_USER:             # Don't set quotas for the default user
            if self.spcUsage != 0:
                try:
                    softblock = 0 
                    hardblock = 0 
                    softinode = 0 
                    hardinode = 0
                    command = 'setquota -u %s %d %d %d %d /' % (self.userName,softblock,hardblock,softinode,hardinode)
                    self.logger.info('exec: %s' % command)
                    _res = riaps_sudo(command)
                except:
                    self.logger.warning('re-setting quota failed')
                    
    def addActor(self,actorName,actorDef):
        if actorName in self.actors:
            return
        else:
            actor = ActorResourceManager(self,actorName,actorDef)
            self.actors[actorName] = actor
            
    def addClientDevice(self,actorName,device):
        if actorName not in self.actors:
            raise SetupError("actor '%s' is unknown" % (actorName))
        else:
            self.actors[actorName].addClientDevice(device)
            
    def startActor(self,actorName,proc):
        if actorName not in self.actors:
            raise SetupError("actor '%s' is unknown" % (actorName))
        else:
            self.actors[actorName].startActor(proc)
            
    def stopActor(self,actorName,proc):
        if actorName not in self.actors:
            raise SetupError("actor '%s' is unknown" % (actorName))
        else:
            self.actors[actorName].stopActor(proc)
    
    def reclaimApp(self):
        try:
            riaps_user = Config.TARGET_USER
            _res = riaps_sudo('chown -R %s:%s %s' % (riaps_user,riaps_user,self.appFolder))
        except:
            traceback.print_exc()
            pass
        
    def claimApp(self):
        try:
            _res = riaps_sudo('chown -R %s:%s %s' % (self.userName,self.userName,self.appFolder))
            # _res = riaps_sudo('chown %s %s/%s' % (Config.TARGET_USER,self.appFolder,const.appDescFile))
        except:
            # traceback.print_exc()
            self.logger.warning('claiming app for user %s failed' % (self.userName))
            self.userName = Config.TARGET_USER          # Default user
        
    def cleanupApp(self):
        for actor in self.actors.values():
            actor.cleanupActor()
            # Delete app cgroups
        try:
            if self.cpuCGroup is not None:
                self.cpuCGroup.delete_empty_children()
                self.parent.riapsCPU.delete_cgroup(self.appName)
            if self.memCGroup is not None:
                self.memCGroup.delete_empty_children()
                self.parent.riapsMem.delete_cgroup(self.appName)
            if self.netCGroup is not None:
                self.netCGroup.delete_empty_children()
                self.parent.riapsNet.delete_cgroup(self.appName)
        except: 
            pass
        self.delQuota()
        riaps_uid = self.parent.riaps_uid
        try:
            # tc qdisc del dev enp0s3 parent 1000:1001 handle 1001:
            _res = riaps_sudo('tc qdisc del dev %s parent %s:%s handle %s:'
                                % (Config.NIC_NAME,riaps_uid,self.uid,self.uid))
            # tc class del dev enp0s3 parent 1000:1000 classid 1000:1001
            _res = riaps_sudo('tc class del dev %s parent %s:%s classid %s:%s'
                              % (Config.NIC_NAME,riaps_uid,riaps_uid,
                                riaps_uid,self.uid))
        except:
            pass
        try:
            if self.userName != Config.TARGET_USER:
                _res = riaps_sudo('deluser %s' % self.userName)
                _res = riaps_sudo('delgroup %s' % self.userName)
            riaps_user = Config.TARGET_USER
            _res = riaps_sudo('chown -R %s:%s %s' % (riaps_user,riaps_user,self.appFolder))
        except:
            traceback.print_exc()
            pass
            

class ResourceManager(object):
    '''
    Resource manager 
    '''
    def __init__(self,context):
        self.logger = logging.getLogger(__name__)
        self.appID = 1      # App ID counter
        # Map of apps
        self.appMap = { } 
        # Context
        self.context = context
        # Cgroups
        self.cgroupTree = trees.Tree()
        if self.cgroupTree.get_node_by_path('/cpu/riaps/') == None:
            self.logger.info("attempting to create cgroup 'riaps'")
            _res = riaps_sudo('user_cgroups %s' % (Config.TARGET_USER))
            self.cgroupTree = trees.Tree()      
        self.riapsCPU = self.cgroupTree.get_node_by_path('/cpu/riaps/')     # CPU scheduling
        self.riapsMem = self.cgroupTree.get_node_by_path('/memory/riaps/')  # Memory usage
        self.riapsNet = self.cgroupTree.get_node_by_path('/net_cls/riaps/') # Net usage
        self.hasCGroup = (self.riapsCPU is not None) and \
                            (self.riapsMem is not None) and \
                            (self.riapsNet is not None)
        if not self.hasCGroup:
            self.logger.warning("cgroup 'riaps' is incomplete - limited resource management.")
        # File space is handled through the quota system
        self.spcMonitor = SpcMonitorThread(self)
        self.spcMonitor.start()
        # Network limits are handled through tc
        self.cleanupNet()
        riaps_user = Config.TARGET_USER
        pw_record = pwd.getpwnam(riaps_user)
        self.riaps_uid = str(pw_record.pw_uid)
        _res = riaps_sudo('tc qdisc add dev %s root handle %s: htb'         # Root qdisc = htb
                          % (Config.NIC_NAME,self.riaps_uid))
        _res = riaps_sudo('tc class add dev %s parent %s: '                 # Root class
                          'classid %s:%s htb rate %s ceil %s'
                          % (Config.NIC_NAME,self.riaps_uid,
                             self.riaps_uid,self.riaps_uid,
                             Config.NIC_RATE, Config.NIC_CEIL))
        if Config.NETMON: 
            self.netMonitor = NetMonitorThread(self)
            self.netMonitor.start()
        else: 
            self.netMonitor = None
        self.logger.info("__init__ed")
        
    
    def setupApp(self,appName,appFolder,userName):
        '''
        Start an app: create an app resource manager for this app if it has not been created yet
        '''
        self.logger.info("setupApp %s" % appName)
        if appName not in self.appMap:
            self.appMap[appName] = AppResourceManager(self,appName,appFolder,userName)
        else:
            self.appMap[appName].claimApp()
        # print(self.appMap)
    
    def getUserName(self,appName):
        if appName in self.appMap:
            return self.appMap[appName].getUserName()
        else:
            return Config.TARGET_USER
    
    def addActor(self,appName,actorName,actorDef):
        self.logger.info("addActor %s.%s" % (appName,actorName))
        if appName not in self.appMap:
            raise BuildError("appName '%s' is unknown" % (appName))
        else:
            appRM = self.appMap[appName]
            appRM.addActor(actorName,actorDef)

    def addClientDevice(self,appName,actorName,device):
        self.logger.info("addClientDevice %s.%s" % (appName,actorName))
        if appName not in self.appMap:
            raise BuildError("appName '%s' is unknown" % (appName))
        else:
            appRM = self.appMap[appName]
            appRM.addClientDevice(actorName,device)
        
    def startActor(self,appName,actorName,proc):
        self.appMap[appName].startActor(actorName,proc)
    
    def stopActor(self,appName,actorName,proc):
        self.appMap[appName].stopActor(actorName,proc)
    
    def reclaimApp(self,appName):
        if appName not in self.appMap:
            raise BuildError("appName '%s' is unknown" % (appName))
        else:
            self.appMap[appName].reclaimApp()
            
    def cleanupApp(self,appName):
        if appName not in self.appMap:
            raise BuildError("appName '%s' is unknown" % (appName))
        else:
            self.appMap[appName].cleanupApp()
            del self.appMap[appName]
            # Flag an error
            pass
        
    def cleanupNet(self):
        _res = riaps_sudo('tc qdisc del dev %s root' % (Config.NIC_NAME))   # Cleanup
        
    def cleanupApps(self):
        '''
        Cleanup all apps: remove the cgroup of the apps
        '''
        for appName, _appValue in list(self.appMap.items()):
            self.cleanupApp(appName)

    def terminate(self):
        self.logger.info("terminating")
        self.cleanupNet()
        self.spcMonitor.terminate()
        self.spcMonitor.join()
        if self.netMonitor:
            self.netMonitor.terminate()
            self.netMonitor.join()
        self.logger.info("terminated")
