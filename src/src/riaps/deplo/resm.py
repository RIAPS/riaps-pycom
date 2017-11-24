'''
Created on Nov 23, 2017

@author: riaps
'''
from cgroupspy import trees
import os
import time
import signal
import subprocess
import psutil
import threading
import logging
from riaps.run.exc import *

class MonitorThread(threading.Thread):
    '''
    Thread for monitoring an actor and enforcing resource limits.
    '''
    def __init__(self,interval,usage):
        threading.Thread.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.interval = interval    # sec
        self.usage = usage          # % INT
    
    def setup(self,proc):
        self.proc = proc
        self.mon = psutil.Process(proc.pid)
        self.terminated = threading.Event()
        self.terminated.clear()

    def run(self):
        current = self.mon.cpu_percent(self.interval)
        time.sleep(0.001)
        while True:
            if self.terminated.is_set(): break
            current = self.mon.cpu_percent(self.interval)
            if self.terminated.is_set(): break
            if current == 0: continue
            self.logger.info("SIGXCPU to [%d]? %d > %d in %f" % (self.proc.pid,current,self.usage,self.interval))
            if current > self.usage:
                # print ("SIGXCPU sent")
                self.proc.send_signal(signal.SIGXCPU)
                time.sleep(1.0)
                # self.mon = psutil.Process(self.proc.pid)
                # current = self.mon.cpu_percent(self.interval)           
        
    def terminate(self):
        self.terminated.set()
   
        
class ActorResourceManager(object):
    '''
    Resource manager for an actor
    '''
    def __init__(self,parent,actorName,actorDef):
        self.logger = logging.getLogger(__name__)
        self.parent = parent
        self.managed = 'usage' in actorDef 
        # If no usage spec, ignore
        if not self.managed: return
        self.settings = actorDef['usage']
        # Setup cgroup
        if parent.hasCGroup:
            cpuPath = self.parent.cpuCGroup.path + ('/' + actorName).encode('utf-8')
            cpuNode = self.parent.cgroupTree.get_node_by_path(cpuPath)
            self.cpuCGroup = cpuNode if (cpuNode != None) else self.parent.cpuCGroup.create_cgroup(actorName)            
            # TODO: add other cgroups
        # Setup resource monitors
        self.hasCPU = self.setupCPU()
        # TODO: Add other resource monitors
    
    def setupCPU(self):
        self.started = False
        if 'cpu' not in self.settings: return False
        self.cpuSettings = self.settings['cpu']
        try:
            self.cpuUsage = self.cpuSettings['use']         # %
            self.cpuInterval = self.cpuSettings['interval'] # msec
            self.cpuMax = self.cpuSettings['max']
        except KeyError:
            return False
        if (self.cpuMax):
            self.cpuMonitor = MonitorThread(self.cpuInterval/1000.0,self.cpuUsage)
        else:
            if self.parent.hasCGroup:
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

    def startActor(self,proc):
        # Setup CPU resource monitor
        if self.hasCPU:
            if self.cpuMax:
                self.cpuMonitor.setup(proc)
                self.cpuMonitor.start()
            else:
                if self.parent.hasCGroup:
                    self.cpuController.tasks = proc.pid
        self.started = True
    
    def stopActor(self,proc):
        # Stop CPU resource monitor
        if self.hasCPU:
            if self.cpuMax:
                self.cpuMonitor.terminate()
                self.cpuMonitor.join()
            else:
                if self.parent.hasCGroup:
                    pass # 
        self.started = False
    
    def cleanupActor(self):
        #
        if self.started: self.stopActor(None) 
        # Get rid of monitoring setup
        if self.hasCPU:
            if self.cpuMax:
                self.cpuMonitor = None
            else:
                if self.parent.hasCGroup:
                    self.parent.cpuCGroup.delete_cgroup(self.cpuCGroup)
                    # TODO: delete other cgroup types
                
        
class AppResourceManager(object):
    '''
    Resource manager for an app
    '''
    def __init__(self,parent,appName):
        self.logger = logging.getLogger(__name__)
        self.parent = parent
        self.appName = appName
        self.actors = { }
        self.cgroupTree = parent.cgroupTree
        self.hasCGroup = parent.hasCGroup
        if self.hasCGroup:
            # Check if cgroup already exist, use it or create a new one. 
            cpuPath = self.parent.riapsCPU.path + ('/' + appName).encode('utf-8')
            cpuNode = self.parent.cgroupTree.get_node_by_path(cpuPath)
            self.cpuCGroup = cpuNode if (cpuNode != None) else self.parent.riapsCPU.create_cgroup(appName)
            # TODO: Add other cgroup types
    
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
            
    def stopActor(self,actorName,proc):
        if actorName not in self.actors:
            raise SetupError("actor '%s' is unknown" % (actorName))
        else:
            self.actors[actorName].stopActor(proc)
    
    def cleanupApp(self):
        for actor in self.actors.values():
            actor.cleanupActor()
        # 
        if self.hasCGroup:
            # Delete app cgroups
            self.parent.riapsCPU.delete_cgroup(self.cpuCGroup)
            # TODO: Delete other cgroup types
            

class ResourceManager(object):
    '''
    Resource manager 
    '''
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # Map of apps
        self.appMap = { } 
        # Cgroups
        self.cgroupTree = trees.Tree()
        self.riapsCPU = self.cgroupTree.get_node_by_path('/cpu/riaps/')  # CPU scheduling
        # TODO: Add other cgroup types
        self.hasCGroup = (self.riapsCPU is not None) # and ....
        if not self.hasCGroup:
            self.logger.error("No cgroup for 'riaps' - no soft-limit resource management")
        #

    def startApp(self,appName):
        '''
        Start an app: create an app resource manager for this app if it has not been created yet
        '''
        if appName not in self.appMap:
            self.appMap[appName] = AppResourceManager(self,appName)
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
            # Flag an error
            pass
    
    def cleanupApps(self):
        '''
        Cleanup all apps: remove the cgroup of the apps
        '''
        for appName in self.appMap.keys():
            self.cleanupApp(appName)
            
