'''
Component class
Created on Oct 15, 2016

@author: riaps
'''

import threading
import zmq
import time
import logging
import traceback
from .exc import BuildError
from riaps.utils import spdlog_setup
import spdlog

class ComponentThread(threading.Thread):
    '''
    Component execution thread. Runs the component's code, and communicates with the parent actor.
    '''
    def __init__(self,parent):
        threading.Thread.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.name = parent.name
        self.parent = parent
        self.context = parent.context
        self.instance = parent.instance
    
    def setupControl(self):
        '''
        Create the control socket and connect it to the socket in the parent part
        '''
        self.control = self.context.socket(zmq.PAIR)
        self.control.connect('inproc://part_' + self.name + '_control')
    
    def setupSockets(self):
        msg = self.control.recv_pyobj()
        if msg != "build":
            raise BuildError 
        for portName in self.parent.ports:
            res = self.parent.ports[portName].setupSocket(self)
            if res[0] == 'tim' or res[0] == 'ins':
                continue
            elif res[0] == 'pub' or res[0] == 'sub' or \
                    res[0] == 'clt' or res[0] == 'srv' or \
                    res[0] == 'req' or res[0] == 'rep' or \
                    res[0] == 'qry' or res[0] == 'ans' :
                self.control.send_pyobj(res)
            else:
                raise BuildError
        self.control.send_pyobj("done")

    def setupPoller(self):
        self.poller  = zmq.Poller()
        self.sock2NameMap = {}
        self.sock2PortMap = {}
        self.poller.register(self.control,zmq.POLLIN)
        self.sock2NameMap[self.control] = ""
        for portName in self.parent.ports:
            portObj = self.parent.ports[portName]
            portSocket = portObj.getSocket()
            portIsInput = portObj.inSocket()
            if portSocket != None:
                self.sock2PortMap[portSocket] = portObj
                if portIsInput:
                    self.poller.register(portSocket,zmq.POLLIN)
                    self.sock2NameMap[portSocket] = portName
    
    def replaceSocket(self,portObj,newSocket):
        portName = portObj.name
        oldSocket = portObj.getSocket()
        del self.sock2PortMap[oldSocket]
        if portObj.inSocket():
            self.poller.register(oldSocket, 0)
            del self.sock2NameMap[oldSocket]
        oldSocket.close()
        self.sock2PortMap[newSocket] = portObj
        if portObj.inSocket():
            self.poller.register(newSocket,zmq.POLLIN)
            self.sock2NameMap[newSocket] = portName
            
    def runCommand(self):
        res = False
        msg = self.control.recv_pyobj()
        if msg == "kill":
            self.logger.info("kill")
            res = True
        elif msg == "activate":
            self.logger.info("activate")
            self.instance.handleActivate()  
        elif msg == "deactivate":
            self.logger.info("deactivate")
            self.instance.handleDeactivate()     
        elif msg == "passivate":
            self.logger.info("passivate")
            self.instance.handlePassivate()                
        else: 
            cmd = msg[0]
            if cmd == "portUpdate":
                self.logger.info("portUpdate")
                (_ignore,portName,host,port) = msg
                portObj = self.parent.ports[portName]
                res = portObj.update(host,port)
                self.control.send_pyobj("ok")
            elif cmd == "limitCPU":
                self.logger.info("limitCPU")
                self.instance.handleCPULimit()
                self.control.send_pyobj("ok")
            elif cmd == "limitMem":
                self.logger.info("limitMem")
                self.instance.handleMemLimit()
                self.control.send_pyobj("ok")
            elif cmd == "limitSpc":
                self.logger.info("limitSpc")
                self.instance.handleSpcLimit()
                self.control.send_pyobj("ok")
            elif cmd == "limitNet":
                self.logger.info("limitNet")
                self.instance.handleNetLimit()
                self.control.send_pyobj("ok")
            elif cmd == "nicState":
                state = msg[1]
                self.logger.info("nicState %s" % state)
                self.instance.handleNICStateChange(state)
                self.control.send_pyobj("ok")
            elif cmd == "peerState":
                state,uuid = msg[1], msg[2]
                self.logger.info("peerState %s at %s" % (state,uuid))
                self.instance.handlePeerStateChange(state,uuid)
                self.control.send_pyobj("ok")
            else:
                self.logger.info("unknown command %s" % cmd)
                pass            # Should report an error
        return res
    
    def getInfo(self):
        info = []
        for (_portName,portObj) in self.parent.ports:
            res = portObj.getInfo()
            info.append(res)
        return info
    
    def logEvent(self,msg):
        self.control.send_pyobj(msg)
        
    def run(self):
        self.setupControl()
        self.setupSockets()
        self.setupPoller()
        toStop = False
        while True:
            sockets = dict(self.poller.poll())
            if self.control in sockets:
                toStop = self.runCommand()
                del sockets[self.control]
            if toStop: break
            for socket in sockets:
                portName = self.sock2NameMap[socket]
                portObj = self.sock2PortMap[socket]
                deadline = portObj.getDeadline()
                try:
                    funcName = 'on_' + portName
                    func_ = getattr(self.instance, funcName)
                    if deadline != 0:
                        start = time.perf_counter()
                    func_()
                    if deadline != 0:
                        finish = time.perf_counter()
                        spent = finish-start
                        if spent > deadline:
                            self.logger.error('Deadline violation in %s.%s()' 
                                              % (self.name,funcName))
                            msg = ('deadline',)
                            self.control.send_pyobj(msg)
                            self.instance.handleDeadline(funcName)
                except:
                    traceback.print_exc()
                    msg = ('exception',)
                    self.control.send_pyobj(msg)
        self.logger.info("stopping")
        if hasattr(self.instance,'__destroy__'):
            destroy_ = getattr(self.instance,'__destroy__')
            destroy_()
        self.logger.info("stopped")

                   
class Component(object):
    '''
    Base class for RIAPS application components
    '''
    def __init__(self):
        '''
        Constructor
        Logger attributes
        logger: logger for this class
        loghandler: handler for the logger (defaults to a StreamHandler)
        logformatter: formatter assigned to the handler (default: Level:Time:Process:Class:Message)
        '''
        class_ = getattr(self,'__class__')
        className = getattr(class_,'__name__')
        self.owner = class_.OWNER                   # This is set in the parent part (temporarily)
        #
#         self.logger = logging.getLogger(className)
#         self.logger.setLevel(logging.INFO)
#         self.logger.propagate=False
#         self.loghandler = logging.StreamHandler()
#         self.loghandler.setLevel(logging.INFO)
#         self.logformatter = logging.Formatter('%(levelname)s:%(asctime)s:[%(process)d]:%(name)s:%(message)s')
#         self.loghandler.setFormatter(self.logformatter)
#         self.logger.addHandler(self.loghandler)
        #
        loggerName = self.owner.getActorName() + '.' + self.owner.getName()
        self.logger = spdlog_setup.get_logger(loggerName)
        if self.logger == None:
            self.logger = spdlog.ConsoleLogger(loggerName,True,True,False)
            self.logger.set_pattern("[%l]:%H:%M:%S,%e:[%P]:%n:%v")
#        print  ( "Component() : '%s'" % self )
 
    def getName(self):
        '''
        Return the name of the component (as in model)
        '''
        return self.owner.getName()
    
    def getTypeName(self):
        '''
        Return the name of the type of the component (as in model) 
        '''
        return self.owner.getTypeName()
    
    def getLocalID(self):
        '''
        Return a locally unique ID (int) of the component. The ID is unique within the actor.
        '''
        return id(self)

    def getActorName(self):
        '''
        Return the name of the parent actor (as in model)
        '''
        return self.owner.getActorName()
    
    def getAppName(self):
        '''
        Return the name of the parent application (as in model)
        '''
        return self.owner.getAppName()
    
    def getActorID(self):
        '''
        Return a globally unique ID (8 bytes) for the parent actor. 
        '''
        return self.owner.getActorID()
    
    def getUUID(self):
        '''
        Return the network unique ID for the parent actor
        '''
        return self.owner.getUUID()
    
    def handleActivate(self):
        '''
        Default activation handler
        '''
        pass
    
    def handleDectivate(self):
        '''
        Default activation handler
        '''
        pass
    
    def handlePassivate(self):
        '''
        Default activation handler
        '''
        pass
    
    def handleCPULimit(self):
        ''' 
        Default handler for CPU limit exceed
        '''
        pass
    
    def handleMemLimit(self):
        ''' 
        Default handler for memory limit exceed
        '''
        pass
    
    def handleSpcLimit(self):
        ''' 
        Default handler for space limit exceed
        '''
        pass
        
    def handleNetLimit(self):
        ''' 
        Default handler for space limit exceed
        '''
        pass
    
    def handleNICStateChange(self,state):
        ''' 
        Default handler for NIC state change
        '''
        pass
    
    def handlePeerStateChange(self,state,uuid):
        ''' 
        Default handler for peer state change
        '''
        pass
    
    def handleDeadline(self,_funcName):
        '''
        Default handler for deadline violation
        '''
        pass
    