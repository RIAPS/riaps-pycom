'''
Fault manager 

Created on Nov 23, 2017

@author: riaps
'''

import logging
import threading
import time
from pyroute2 import IPRSocket
from pyroute2.netlink import rtnl 

import ctypes
import parse
import os
import czmq
import zyre
from zyre import Zyre, ZyreEvent

from riaps.consts.defs import *
from riaps.run.exc import *
from riaps.utils.sudo import riaps_sudo,is_su
from riaps.utils.config import Config
import traceback

class FMMonitor(threading.Thread):
    def __init__(self,context,hostAddress,riapsHome):
        threading.Thread.__init__(self,daemon=True)
        self.logger = logging.getLogger(__name__)
        self.context = context
        self.hostAddress = hostAddress
        self.riapsHome = riapsHome
        self.control = None
        self.peers  = { }   # uuid : address - all peers
        self.groups = { }   # groupName : { peers* } - peers in group    
        self.actors = { }   # appName : { actors* }  - actors in apps
        self.uuid = None
        self.logger.info('FMMon:__inited__')
    
    def setup(self):
        self.logger.info('FMMon:setup()')
        self.control = self.context.socket(zmq.PAIR)
        self.control.bind(const.fmMonitorEndpoint)
        return self.control
    
    def getUUID(self):
        while self.uuid == None:
            time.sleep(0.1)
        return self.uuid
    
    def setupApp(self,appName):
        msg = ('setupApp',appName)
        self.control.send_pyobj(msg)

    def cleanupApp(self,appName):
        msg = ('cleanupApp', appName)
        self.control.send_pyobj(msg)
    
    def addActor(self,appName,actorName):
        msg = ('addActor', appName, actorName)
        self.control.send_pyobj(msg)
    
    def delActor(self,appName,actorName):
        msg = ('delActor', appName, actorName)
        self.control.send_pyobj(msg)
        
    def dieActor(self,appName,actorName):
        msg = ('dieActor', appName, actorName)
        self.control.send_pyobj(msg)
        
    def terminate(self):
        if self.control != None:
            self.control.send_pyobj(('stop',))
        else:
            self.setup()
            time.sleep(0.1)
            self.control.send_pyobj(('stop',))
    
    def peerHeaderKey(self,ipAddress):
        return b'riaps@' + ipAddress.encode('utf-8')
    
    PEERMARK = b'CAFE'
    
    def groupName(self,appName):
        return b'riaps.' + appName.encode('utf-8')
        
    def run(self):
        self.zyre = Zyre(None)
        if self.logger.level > 0:
            self.zyre.set_verbose()
            # Zsys.set_logsystem(1)
        else:
            # Zsys.set_logsystem(0)
            pass
        self.uuid = self.zyre.uuid()
        self.zyre.set_interface(Config.NIC_NAME.encode('utf-8'))
        if Config.SECURITY:
            certFile = os.path.join(self.riapsHome,"keys",const.zmqCertificate)
            cert = czmq.Zcert.load(ctypes.c_char_p(certFile.encode('utf-8')))
            self.zyre.set_zcert(cert) 
        self.zyre.set_evasive_timeout(const.peerEvasiveTimeout)
        self.zyre.set_expired_timeout(const.peerExpiredTimeout)
        self.zyre.set_header(self.peerHeaderKey(self.hostAddress), self.PEERMARK)
        self.command = self.context.socket(zmq.PAIR)
        self.command.connect(const.fmMonitorEndpoint)
        self.zyre.start()
        self.zyre.join(b'riaps')
        self.zyreSocket = self.zyre.socket()
        self.poller = czmq.Zpoller(zyre.c_void_p(self.command.underlying),self.zyreSocket,0)
        while True:
            reader = self.poller.wait(-1)   # Wait forever
            if self.poller.terminated():
                self.logger.warning("FMMon.run - poller terminated")
                break
            if type(reader) == zyre.c_void_p and reader.value == self.command.underlying:
                msg = self.command.recv_pyobj()
                self.logger.info('FMMon.run - command: %s' % str(msg))
                cmd = msg[0]
                if cmd == 'stop':
                    break
                elif cmd == 'setupApp':
                    appName = msg[1]
                    group = self.groupName(appName)
                    self.zyre.join(group)
                    if appName not in self.groups:
                        self.groups[appName] = set()
                        self.actors[appName] = set()
                elif cmd == 'cleanupApp':
                    appName = msg[1]
                    group = self.groupName(appName)
                    self.zyre.leave(group)
                    if appName in self.groups:
                        del self.groups[appName]
                elif cmd == 'addActor':
                    appName,actorName = msg[1:]
                    assert appName in self.groups
                    self.actors[appName].add(actorName)
                    group = self.groupName(appName)
                    arg = "+ %s.%s" % (appName,actorName)
                    self.logger.info("FMMon.addActor.shout: %s" % arg)
                    self.zyre.shouts(group,arg.encode('utf-8'))
                    for peer in self.groups[appName]:
                        self.logger.info("FMMon.addactor tell %s.%s has peer at %s" 
                                      % (appName,actorName,str(peer))) 
                        info = ('peer+', appName, actorName, peer)
                        self.command.send_pyobj(info)
                elif cmd == 'delActor':
                    appName,actorName = msg[1:]
                    assert appName in self.groups and actorName in self.actors[appName]
                    self.actors[appName].remove(actorName)
                    group = self.groupName(appName)
                    arg = "- %s.%s" % (appName,actorName)
                    self.logger.info("FMMon.delActor.shout: %s" % arg)
                    self.zyre.shouts(group,arg.encode('utf-8')) 
                elif cmd == 'dieActor':
                    appName,actorName = msg[1:]
                    assert appName in self.groups and actorName in self.actors[appName]
                    self.actors[appName].remove(actorName)
                    group = self.groupName(appName)
                    arg = "? %s.%s" % (appName,actorName)
                    self.logger.info("FMMon.dieActor.shout: %s" % arg)
                    self.zyre.shouts(group,arg.encode('utf-8')) 
                else:
                    pass                        # Should be error
            elif reader == self.zyreSocket:
                event = ZyreEvent(self.zyre)
                eType = event.type()
                _pName = event.peer_name()
                pUUID = event.peer_uuid()
                pAddr = event.peer_addr()
                group = event.group()
                _headers = event.headers()
                msg = event.get_msg()
#                 if eType != b'EVASIVE':
#                     print("# %s %s %s %s %s %s %s" 
#                           % (str(eType),str(_pName),str(pUUID),str(pAddr),
#                              str(group),str(_headers),str(msg)))
                if eType == b'ENTER':
                    self.logger.info("FMMon.ENTER %s from %s" % (str(pUUID),str(pAddr)))
                    try:
                        pAddrStr = pAddr.decode('UTF-8')
                        (peerIp,_peerPort) = parse.parse("tcp://{}:{}",pAddrStr)
                        peerHeaderKey =  self.peerHeaderKey(peerIp)
                        _value = _headers.lookup(peerHeaderKey)
                        if (_value):
                            try:
                                value = ctypes.cast(_value,ctypes.c_char_p).value
                                assert value == self.PEERMARK
                                self.peers[pUUID] = pAddr
                                self.logger.info("FMMon.ENTER valid peer")
                            except:
                                self.logger.info("FMMon.ENTER header value mismatch")
                        else:
                            self.logger.info("FMMon.ENTER header key mismatch")
                    except:
                        self.logger.info("FMMon.ENTER peer addr parsing error")
                elif pUUID not in self.peers:   # Skip the rest if this is not a peer
                    continue
                elif eType == b'JOIN':
                    groupName = group.decode()
                    self.logger.info("FMMon.JOIN %s from %s" % (str(groupName), str(pUUID)))
                    if groupName == 'riaps':
                        continue                # Joined riaps group - should be validated
                    else:
                        _head,appName = groupName.split('.')
                        if _head == 'riaps':
                            if appName not in self.groups:
                                self.groups[appName] = { pUUID }
                                if appName not in self.actors:
                                    self.actors[appName] = set()
                            else:
                                self.groups[appName].add(pUUID) 
                            if appName in self.actors:
                                peer = pUUID
                                for actorName in self.actors[appName]:
                                    arg = "+ %s.%s" % (appName,actorName)
                                    self.logger.info("FMMon.JOIN.whisper: %s to %s " % (arg, str(peer)))
                                    self.zyre.whispers(peer,arg.encode('utf-8'))
                                    self.logger.info("FMMon.JOIN tell %s.%s has peer at %s" 
                                          % (appName,actorName,str(peer))) 
                                    info = ('peer+', appName, actorName, peer)
                                    self.command.send_pyobj(info)
                        else:
                            pass
                elif eType == b'LEAVE':
                    groupName = group.decode()
                    self.logger.info("FMMon.LEAVE %s from %s" % (str(pUUID),str(group)))
                    if groupName == 'riaps':
                        continue                # Left riaps group - should be validated
                    else:
                        _head,appName = groupName.split('.')
                        if _head == 'riaps':
                            if appName in self.groups:
                                self.groups[appName].remove(pUUID)
                            if appName in self.actors:
                                for actorName in self.actors[appName]:
                                    peer = pUUID
                                    self.logger.info("FMMon.LEAVE tell %s.%s lost peer at %s" 
                                          % (appName,actorName,str(peer))) 
                                    info = ('peer-', appName, actorName, peer)
                                    self.command.send_pyobj(info)
                        else:
                            pass
                elif eType == b'EXIT':
                    self.logger.info("FMMon.EXIT %s " % (str(pUUID)))
                    for appName,group in self.groups.items():
                        if pUUID in group:
                            if appName in self.actors:
                                for actorName in self.actors[appName]:
                                    peer = pUUID
                                    self.logger.info("FMMon.EXIT tell %s.%s lost peer at %s" 
                                                     % (appName,actorName,str(peer))) 
                                    info = ('peer-', appName, actorName, peer)
                                    self.command.send_pyobj(info)
                    if pUUID in self.peers: del self.peers[pUUID]
                elif eType == b'SHOUT' or eType == b'WHISPER':
                    # IF SHOUT, verify that this is for us
                    arg = msg.popstr().decode()
                    self.logger.info("FMMon.SHOUT %s = %s " % (str(pUUID), arg))
                    peer = pUUID
                    cmd,pair = arg.split(' ')
                    appName,actorName = pair.split('.',1)
                    head, cast = '?','?'
                    if cmd == '+': 
                        head,cast = 'peer+',' has peer '
                    elif cmd == '-':
                        head,cast = 'peer-',' lost peer '
                    elif cmd == '?':
                        head,cast = 'peer-',' lost peer '
                    if appName not in self.groups:
                        self.groups[appName] = { pUUID }
                    if appName in self.actors:
                        for actorName in self.actors[appName]:
                            self.logger.info("FMMon.%s: tell %s.%s %s %s" 
                                             % (eType.decode(),appName,actorName,cast,str(peer))) 
                            info = (head, appName, actorName, peer)
                            self.command.send_pyobj(info)       
                else:
                    pass
        self.command.close()
        for appName in self.actors:
            if appName in self.groups:
                group = self.groupName(appName) 
                arg = "- %s.%s" % (appName,actorName)
                self.logger.info("FMMon.terminate.shout: %s" % arg)
                self.zyre.shouts(group,arg.encode('utf-8')) 
        self.zyre.leave(b'riaps')
        self.zyre.stop()

        
class NICMonitor(threading.Thread):
    def __init__(self,context):
        threading.Thread.__init__(self,daemon=True)
        self.logger = logging.getLogger(__name__)
        self.context = context
        self.ip = IPRSocket()
        self.ip.bind(rtnl.RTNLGRP_LINK | rtnl.RTNLGRP_NOTIFY)
        self.control = None
        self.state = ''
        self.carrier = -1
        
    def setup(self):
        self.logger.info('NICMon:setup()')
        self.control = self.context.socket(zmq.PAIR)
        self.control.bind(const.fmNICMonitorEndpoint)
        return self.control
        
    def run(self):
        self.command = self.context.socket(zmq.PAIR)
        self.command.connect(const.fmNICMonitorEndpoint)
        self.poller = zmq.Poller()
        self.poller.register(self.ip._sock,zmq.POLLIN)
        self.poller.register(self.command,zmq.POLLIN)
        while True:
            sockets = dict(self.poller.poll())
            if self.ip._sock.fileno() in sockets:
                infos = self.ip.get()
                for info in infos:
                    attrs = dict(info['attrs'])
                    ifname = attrs['IFLA_IFNAME']
                    state = attrs['IFLA_OPERSTATE']
                    carrier = attrs['IFLA_CARRIER']
                    if ifname == Config.NIC_NAME and state != self.state and carrier != self.carrier:
                        self.logger.info("NICMonitor: state has changed (%s,%d)" % (state,carrier))
                        if state != 'UP' or carrier != 1:       # NIC down and/or carrier lost
                            info = ('nic-',)
                            self.command.send_pyobj(info)
                        elif state == 'UP' and carrier == 1:    # NIC UP and carrier is on
                            info = ('nic+',)
                            self.command.send_pyobj(info)       
                        self.state,self.carrier = state, carrier
                del sockets[self.ip._sock.fileno()]
            elif self.command in sockets:
                msg = self.command.recv_pyobj()
                if msg == 'stop':
                    break
                del sockets[self.command]
        self.command.close()
        self.ip.close()

    def terminate(self):
        self.control.send_pyobj('stop')


class ActorFaultManager(object):
    '''
    Fault manager for an actor
    '''
    def __init__(self,parent,actorName,actorDef):
        self.logger = logging.getLogger(__name__)
        self.parent = parent
        self.context  = self.parent.context
        self.actorName = actorName
        self.proc = None
        self.started = False
    
    def addClientDevice(self,_device):
        appName = self.parent.appName
        actorName = self.actorName
        self.logger.info('actor.addClientDevice %s.%s' % (appName,actorName))
    
    def startActor(self,proc):
        # Setup CPU fault monitor
        #
        self.proc = proc
        self.started = True

    def stopActor(self,_proc):
        # Stop CPU fault monitor
        if not self.started: return
        #
        self.started = False
    
    def cleanupActor(self):
        # Get rid of monitoring setup
        pass
        
class AppFaultManager(object):
    '''
    Fault manager for an app
    '''
    def __init__(self,parent,appName,appFolder):
        self.logger = logging.getLogger(__name__)
        self.parent = parent
        self.parent.fmMonitor.setupApp(appName) 
        self.context = self.parent.context
        self.appName = appName
        self.appFolder = appFolder
        self.actors = { }

    def addActor(self,actorName,actorDef):
        if actorName in self.actors:
            return
        else:
            actor = ActorFaultManager(self,actorName,actorDef)
            self.actors[actorName] = actor
            
    def addClientDevice(self,actorName,device):
        assert actorName in self.actors
        self.actors[actorName].addClientDevice(device)
            
    def startActor(self,actorName,proc):
        assert actorName in self.actors
        self.actors[actorName].startActor(proc)
        self.parent.fmMonitor.addActor(self.appName,actorName)
            
    def stopActor(self,actorName,proc):
        assert actorName in self.actors
        self.actors[actorName].stopActor(proc)
        self.parent.fmMonitor.delActor(self.appName,actorName)
            
    def cleanupApp(self):
        self.parent.fmMonitor.cleanupApp(self.appName)
        for _actorName,actor in self.actors.items():
            actor.cleanupActor()

class FaultManager(object):
    '''
    Fault manager 
    '''
    def __init__(self,parent,context):
        self.logger = logging.getLogger(__name__)
        self.parent = parent
        self.appID = 1      # App ID counter
        # Map of apps
        self.appMap = { } 
        # Context
        self.context = context
        # NIC monitoring
        self.nicMonitor = NICMonitor(context)
        self.nicMonitor.start()
        # Fault monitor
        hostAddress = self.parent.hostAddress
        # Home
        riapsHome = self.parent.riapsHome
        self.fmMonitor = FMMonitor(context,hostAddress,riapsHome)
        self.fmMonitor.start()
        # 
        self.logger.info("__init__ed")
        
    def setupFMMon(self):
        return self.fmMonitor.setup()
    
    def setupNICMon(self):
        return self.nicMonitor.setup()
    
    def getUUID(self):
        return self.fmMonitor.getUUID()
    
    def setupApp(self,appName,appFolder):
        '''
        Start an app: create an app fault manager for this app if it has not been created yet
        '''
        self.logger.info("setupApp %s" % appName)
        if appName not in self.appMap:
            self.appMap[appName] = AppFaultManager(self,appName,appFolder)
        else:
            pass
    
    def addActor(self,appName,actorName,actorDef):
        self.logger.info("addActor %s.%s" % (appName,actorName))
        if appName not in self.appMap:
            raise BuildError("appName '%s' is unknown" % (appName))
        else:
            appFM = self.appMap[appName]
            appFM.addActor(actorName,actorDef)

    def addClientDevice(self,appName,actorName,device):
        self.logger.info("addClientDevice %s.%s" % (appName,actorName))
        if appName not in self.appMap:
            raise BuildError("appName '%s' is unknown" % (appName))
        else:
            appFM = self.appMap[appName]
            appFM.addClientDevice(actorName,device)
        
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
        
    def cleanupApps(self):
        '''
        Cleanup all apps
        '''
        for appName, _appValue in list(self.appMap.items()):
            self.cleanupApp(appName)

    def terminate(self):
        self.logger.info("terminating")
        self.nicMonitor.terminate()
        self.fmMonitor.terminate()
        self.logger.info("terminated")
        
