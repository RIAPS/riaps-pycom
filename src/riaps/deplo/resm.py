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
import threading
from threading import RLock
import logging
from riaps.run.exc import *
from riaps.utils.sudo import riaps_sudo
from riaps.utils.config import Config
from butter.eventfd import Eventfd
import traceback
from pwd import getpwnam  
from riaps.deplo.resmon import CPUMonitorThread,MemMonitorThread,SpcMonitorThread

class ActorResourceManager(object):
    '''
    Resource manager for an actor
    '''
    def __init__(self,parent,actorName,actorDef):
        self.logger = logging.getLogger(__name__)
        self.parent = parent
        self.actorName = actorName
        self.cpuCGroup = None
        self.memCGroup = None
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
            # TODO: add other cgroups
        # Setup resource monitors
        self.hasCPU = self.setupCPU()
        self.hasMem = self.setupMem()
        self.hasSpace = self.setupSpace()
        if self.hasSpace:
            self.parent.addQuota(self.spcUsage)
        # TODO: Add other resource monitors
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
            self.cpuMonitor = CPUMonitorThread(self.cpuInterval/1000.0,self.cpuUsage)
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
                self.memController.limit_in_bytes = self.memUsage * 1024 # Value is in kBytes
                efd = Eventfd()
                mem = self.memCGroup
                mpl = mem.full_path.decode('utf-8') + '/memory.pressure_level'
                os.chmod(mpl,stat.S_IRUSR) #  | stat.S_IWUSR)
                mpl_file = open(mpl,'rb')
        
                cgc = mem.full_path.decode('utf-8') + '/cgroup.event_control'
                # os.chmod(cgc,stat.S_IRUSR | stat.S_IWUSR)
                cgc_file = open(cgc,'ab',buffering=0)
        
                buf = '%d %d %s' % (efd.fileno(),mpl_file.fileno(),'low')
                buf = buf.encode('utf-8')
        
                _wrl = cgc_file.write(buf)
                assert (_wrl == len(buf))
                os.close(cgc_file.fileno())
                os.close(mpl_file.fileno())
            except:
                traceback.print_exc() 
                return False
            self.memMonitor = MemMonitorThread(efd,self.memUsage)
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
                    self.cpuController.tasks = proc.pid
        if self.hasMem:
            self.memController.tasks = proc.pid
            self.memMonitor.setup(proc)
            if self.memMonitor.is_running():
                self.memMonitor.restart()
            else:
                self.memMonitor.start()
        self.started = True

    
    def stopActor(self,_proc):
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
        self.started = False
    
    def cleanupActor(self):
        # Get rid of monitoring setup
        if self.hasCPU:
            if self.cpuMax:
                if self.started:
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
            if self.started:
                self.memMonitor.terminate()
                self.memMonitor.join()
            self.memMonitor = None
            if self.parent.memCGroup:
                try:
                    self.parent.memCGroup.delete_cgroup(self.actorName)
                except:
                    pass
        # TODO: delete other monitor types
                
        
class AppResourceManager(object):
    '''
    Resource manager for an app
    '''
    def __init__(self,parent,appName,appFolder,userName):
        self.logger = logging.getLogger(__name__)
        self.parent = parent
        self.appName = appName
        self.userName = userName
        self.appFolder = appFolder
        self.actors = { }
        self.cgroupTree = parent.cgroupTree
        self.cpuCGroup = None
        self.memCGroup = None
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
        # TODO: Add other cgroup types
        # Set up the data space for the actor
        try:
            _res = riaps_sudo('adduser --disabled-login --gecos GECOS --no-create-home %s' % self.userName)
            self.uid = getpwnam(self.userName).pw_uid
            _res = riaps_sudo('chown -R %s:%s %s' % (self.userName,self.userName,self.appFolder))
            _res = riaps_sudo('chmod o-rwx %s' % self.appFolder)
        except:
            traceback.print_exc()
            self.logger.warning('creating app user %s failed' % (self.userName))
            self.uid = os.getuid()
        self.spcUsage = 0
        
    def addQuota(self,usage):
        self.spcUsage += usage
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
        
    def addActor(self,actorName,actorDef):
        if actorName in self.actors:
            return
        else:
            actor = ActorResourceManager(self,actorName,actorDef)
            self.actors[actorName] = actor
            
    def startActor(self,actorName,proc):
        if actorName not in self.actors:
            raise SetupError("actor '%s' is unknown" % (actorName))
        else:
            self.actors[actorName].startActor(proc)
            self.parent.spcMonitor.addProc(proc)
            
    def stopActor(self,actorName,proc):
        if actorName not in self.actors:
            raise SetupError("actor '%s' is unknown" % (actorName))
        else:
            self.actors[actorName].stopActor(proc)
            self.parent.spcMonitor.delProc(proc)
    
    def cleanupApp(self):
        for actor in self.actors.values():
            actor.cleanupActor()
            # Delete app cgroups
        if self.cpuCGroup is not None:
            self.cpuCGroup.delete_empty_children()
            self.parent.riapsCPU.delete_cgroup(self.appName)
        if self.memCGroup is not None:
            self.memCGroup.delete_empty_children()
            self.parent.riapsMem.delete_cgroup(self.appName)
        # TODO: Delete other cgroup types
        try:
            _res = riaps_sudo('deluser %s' % self.userName)
            riaps_user = Config.TARGET_USER
            _res = riaps_sudo('chown -R %s:%s %s' % (riaps_user,riaps_user,self.appFolder))
        except:
            traceback.print_exc()
            pass
            

class ResourceManager(object):
    '''
    Resource manager 
    '''
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.appID = 1      # App ID counter
        # Map of apps
        self.appMap = { } 
        # Cgroups
        self.cgroupTree = trees.Tree()
        if self.cgroupTree.get_node_by_path('/cpu/riaps/') == None:
            self.logger.info("attempting to create cgroup 'riaps'")
            _res = riaps_sudo('user_cgroups %s' % (Config.TARGET_USER))
            self.cgroupTree = trees.Tree()      
        self.riapsCPU = self.cgroupTree.get_node_by_path('/cpu/riaps/')     # CPU scheduling
        self.riapsMem = self.cgroupTree.get_node_by_path('/memory/riaps/')  # Memory usage
        # TODO: Add other cgroup types
        self.hasCGroup = (self.riapsCPU is not None) and (self.riapsMem is not None)
        if not self.hasCGroup:
            self.logger.warning("cgroup 'riaps' missing - limited resource management.")
        # File space is handled through the quota system
        self.spcMonitor = SpcMonitorThread()
        self.spcMonitor.start()
    
    def setupApp(self,appName,appFolder,userName):
        '''
        Start an app: create an app resource manager for this app if it has not been created yet
        '''
        if appName not in self.appMap:
            self.appMap[appName] = AppResourceManager(self,appName,appFolder,userName)
        else:
            pass
        # print(self.appMap)
    
    def addActor(self,appName,actorName,actorDef):
        if appName not in self.appMap:
            raise BuildError("appName '%s' is unknown" % (appName))
        else:
            appRM = self.appMap[appName]
            appRM.addActor(actorName,actorDef)

    def startActor(self,appName,actorName,proc):
        self.appMap[appName].startActor(actorName,proc)
    
    def stopActor(self,appName,actorName,proc):
        self.appMap[appName].stopActor(actorName,proc)
        
    def cleanupApp(self,appName):
        if appName not in self.appMap:
            raise BuildError("appName '%s' is unknown" % (appName))
        else:
            self.appMap[appName].cleanupApp()
            del self.appMap[appName]
            # Flag an error
            pass
    
    def cleanupApps(self):
        '''
        Cleanup all apps: remove the cgroup of the apps
        '''
        for appName, _appValue in list(self.appMap.items()):
            self.cleanupApp(appName)

            
