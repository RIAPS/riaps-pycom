'''
Component class
Created on Oct 15, 2016

@author: riaps
'''

import threading
import zmq
import time
import logging
import heapq
import itertools
from collections import deque
import traceback
from .exc import BuildError
from riaps.utils import spdlog_setup
import spdlog
from .dc import Coordinator

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
        self.schedulerType = parent.scheduler
        self.control = None
    
    def setupControl(self):
        '''
        Create the control socket and connect it to the socket in the parent part
        '''
        self.control = self.context.socket(zmq.PAIR)
        self.control.connect('inproc://part_' + self.name + '_control')
    
    def sendControl(self,msg):
        assert self.control != None
        self.control.send_pyobj(msg)

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
        self.sock2GroupMap = {}
        self.portName2GroupMap = {}
        self.poller.register(self.control,zmq.POLLIN)
        self.sock2NameMap[self.control] = ""
        self.sock2PrioMap = {}
        for portName in self.parent.ports:
            portObj = self.parent.ports[portName]
            portSocket = portObj.getSocket()
            portIsInput = portObj.inSocket()
            if portSocket != None:
                self.sock2PortMap[portSocket] = portObj
                if portIsInput:
                    self.poller.register(portSocket,zmq.POLLIN)
                    self.sock2NameMap[portSocket] = portName
                    self.sock2PrioMap[portSocket] = portObj.getIndex()

    def replaceSocket(self,portObj,newSocket):
        portName = portObj.name
        oldSocket = portObj.getSocket() 
        del self.sock2PortMap[oldSocket]
        if portObj.inSocket():
            self.poller.register(oldSocket, 0)
            del self.sock2NameMap[oldSocket]
            del self.sock2PrioMap[oldSocket]
        oldSocket.close()
        self.sock2PortMap[newSocket] = portObj
        if portObj.inSocket():
            self.poller.register(newSocket,zmq.POLLIN)
            self.sock2NameMap[newSocket] = portName
            self.sock2PrioMap[newSocket] = portObj.getIndex()
            
    def addGroupSocket(self,group,groupPriority):
        groupSocket = group.getSocket()
        groupId = group.getGroupName()
        self.poller.register(groupSocket,zmq.POLLIN)
        self.sock2GroupMap[groupSocket] = group
        self.portName2GroupMap[groupId] = group
        self.sock2PrioMap[groupSocket] = groupPriority      # TODO: better solution for group message priority  
        
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
                self.logger.info("portUpdate: %s" % str(msg))
                (_ignore,portName,host,port) = msg
                ports = self.parent.ports
                groups = self.portName2GroupMap
                if portName in ports:
                    portObj = ports[portName]
                    res = portObj.update(host,port)
                elif portName in groups:
                    groupObj = groups[portName]
                    res = groupObj.update(host,port)
                else:
                    pass
                # self.control.send_pyobj("ok")
            elif cmd == "groupUpdate":
                # handle it in coordinator
                pass
            elif cmd == "limitCPU":
                self.logger.info("limitCPU")
                self.instance.handleCPULimit()
                # self.control.send_pyobj("ok")
            elif cmd == "limitMem":
                self.logger.info("limitMem")
                self.instance.handleMemLimit()
                # self.control.send_pyobj("ok")
            elif cmd == "limitSpc":
                self.logger.info("limitSpc")
                self.instance.handleSpcLimit()
                # self.control.send_pyobj("ok")
            elif cmd == "limitNet":
                self.logger.info("limitNet")
                self.instance.handleNetLimit()
                # self.control.send_pyobj("ok")
            elif cmd == "nicState":
                state = msg[1]
                self.logger.info("nicState %s" % state)
                self.instance.handleNICStateChange(state)
                # self.control.send_pyobj("ok")
            elif cmd == "peerState":
                state,uuid = msg[1], msg[2]
                self.logger.info("peerState %s at %s" % (state,uuid))
                self.instance.handlePeerStateChange(state,uuid)
                # self.control.send_pyobj("ok")
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
    
    def executeHandlerFor(self,socket):
        '''
        Execute the handler for the socket
        
        The handler is always allowed to run to completion, the operation is never preempted. 
        '''
        if socket in self.sock2PortMap:
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
                msg = ('exception',traceback.format_exc())
                self.control.send_pyobj(msg)
        elif socket in self.sock2GroupMap:
            group = self.sock2GroupMap[socket]
            try:
                group.handleMessage()
            except:
                traceback.print_exc()
                msg = ('exception',traceback.format_exc())
                self.control.send_pyobj(msg)
        else:
            self.logger.error('Unbound port')
        
    def batchScheduler(self,sockets):
        '''
        Batch scheduler for the component message processing.
        
        The dictionary containing the active sockets is scanned and the associated handler is invoked. 
        
        '''
        for socket in sockets:
            self.executeHandlerFor(socket)
            
    def rrScheduler(self,sockets):
        '''
        Round-robin scheduler for the component message processing. 
        
        The round-robin order is determined by the order of component ports. The dictionary of active sockets is scanned, and the \
        associated handlers are invoked in round-robin order. After each invocation, the inputs are polled (in a no-wait operation) \
        and the round-robin queue is updated. 
        '''
        while True:
            jobs = []
            for socket in sockets:
                if socket in self.sock2PortMap:
                    tag = self.sock2PrioMap[socket]
                elif socket in self.sock2GroupMap:
                    tag = self.sock2PrioMap[socket]             # TODO: better solution for group message priority  
                jobs += [(tag,socket)]
            jobs = sorted(jobs)                 # Sort jobs by tag
            if len(jobs) != 1:                  # More than one job
                if len(self.dq):                # If deque is not empty
                    # Find jobs whose tag is larger than the last executed tag 
                    larger = [ i for i, job in enumerate(jobs) if job[0] > self.last]
                    if len(larger):             # There is at least one such job
                        first = larger[0]       # Shuffle job list to keep rr- order
                        jobs = jobs[-first:] + jobs[0:first]
                else:
                    self.last = jobs[-1][0]     # Tag of last job to be added to deque
            self.dq.extendleft(jobs)            # Add jobs to deque   
            sockets = {}
            while True:
                try:
                    tag,socket = self.dq.pop()
                    self.last = self.dq[0][0] if len(self.dq) > 0 else tag
                    self.executeHandlerFor(socket)
                    if len(self.dq) == 0: return                # Empty queue, return               
                    sockets = dict(self.poller.poll(None))      # Check if something came in
                    if sockets:
                        if self.control in sockets:             # Handle control message
                            self.toStop = self.runCommand()
                            del sockets[self.control]
                            if self.toStop: return              # Return if we must stop
                            if len(sockets):                    # More sockets to handle
                                break                           #  break from inner loop to schedule tasks
                    else:                                       # Nothing came in
                        continue                                #  keep running inner loop
                except IndexError:                              # Queue empty, return
                    print('indexError')
                    return
                  
    def priorityScheduler(self,sockets):
        '''
        priority scheduler for the component message processing. 
        
        The priority order is determined by the order of component ports. The dictionary of active sockets is scanned, and the \
        they are inserted into a priority queue (according to their priority value). The queue is processed (in order of \
        priority). After each invocation, the inputs are polled (in a no-wait operation) and the priority queue is updated. 
        '''
        while True:
            for socket in sockets:
                if socket in self.sock2PortMap:
                    pri = self.sock2PrioMap[socket]
                elif socket in self.sock2GroupMap:
                    pri = self.sock2PrioMap[socket]             # TODO: better solution for group message priority  
                cnt = next(self.tc)
                entry = (pri,cnt,socket)
                heapq.heappush(self.pq,entry)
            sockets = {}
            while True:
                try:
                    pri,cnt,socket = heapq.heappop(self.pq)     # Execute one task
                    self.executeHandlerFor(socket)
                    if len(self.pq) == 0:                       # Empty queue, return
                        return
                    sockets = dict(self.poller.poll(None))      # Poll to check if something came in
                    if sockets:
                        if self.control in sockets:             # Handle control message
                            self.toStop = self.runCommand()
                            del sockets[self.control]
                            if self.toStop: return              # Return if we must stop
                        if len(sockets):                        # More sockets to handle,
                            break                               #  break from inner loop to schedule tasks
                    else:                                       # Nothing came in
                        continue                                #  keep running inner loop
                except IndexError:                              # Queue empty, return
                    return
 
    
    def setupScheduler(self):
        '''
        Select the message scheduler algorithm based on the model. 
        '''
        if self.schedulerType == 'default':
            self.scheduler = self.batchScheduler
        elif self.schedulerType == 'priority':
            self.scheduler = self.priorityScheduler
            self.pq = []
            self.tc = itertools.count()
        elif self.schedulerType == 'rr':
            self.scheduler = self.rrScheduler
            self.dq = deque()
            self.last = -1
        else:
            self.logger.error('Unknown scheduler type: %r' % self.schedulerType)
            self.scheduler = None
            
    def run(self):
        self.setupControl()
        self.setupSockets()
        self.setupPoller()
        self.setupScheduler()
        if self.scheduler:
            self.toStop = False
            while True:
                sockets = dict(self.poller.poll())
                if self.control in sockets:
                    self.toStop = self.runCommand()
                    del sockets[self.control]
                if self.toStop: break
                if len(sockets) > 0: self.scheduler(sockets)
                if self.toStop: break
        self.logger.info("stopping")
        if hasattr(self.instance,'__destroy__'):
            destroy_ = getattr(self.instance,'__destroy__')
            destroy_()
        self.logger.info("stopped")

class Component(object):
    '''
    Base class for RIAPS application components
    '''
    GROUP_PRIORITY_MAX = 0                          # Priority 0 means highest priority
    GROUP_PRIORITY_MIN = 256                        # Priority 256 means lowest priority (>= 256 port indices are unexpected)
    
    def __init__(self):
        '''
        Constructor
       '''
        class_ = getattr(self,'__class__')
        className = getattr(class_,'__name__')
        self.owner = class_.OWNER                   # This is set in the parent part (temporarily)
        #
        # Logger attributes
        # logger: logger for this class
        # loghandler: handler for the logger (defaults to a StreamHandler)
        # logformatter: formatter assigned to the handler (default: Level:Time:Process:Class:Message)
        # self.logger = logging.getLogger(className)
        # self.logger.setLevel(logging.INFO)
        # self.logger.propagate=False
        # self.loghandler = logging.StreamHandler()
        # self.loghandler.setLevel(logging.INFO)
        # self.logformatter = logging.Formatter('%(levelname)s:%(asctime)s:[%(process)d]:%(name)s:%(message)s')
        # self.loghandler.setFormatter(self.logformatter)
        # self.logger.addHandler(self.loghandler)
        #
        loggerName = self.owner.getActorName() + '.' + self.owner.getName()
        self.logger = spdlog_setup.get_logger(loggerName)
        if self.logger == None:
            self.logger = spdlog.ConsoleLogger(loggerName,True,True,False)
            self.logger.set_pattern(spdlog_setup.global_pattern)
        # print  ( "Component() : '%s'" % self )
        self.coord = Coordinator(self)
        self.thread = None
 
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
    
    def handleGroupMessage(self,_group):
        '''
        Default handler for group messages.
        Implementation must immediately call recv/recv_pyobj on the group to obtain message. 
        '''
        pass
    
    def handleVoteRequest(self,group,rfvId):
        '''
        Default handler for vote requests (in member)
        Implementation must recv/recv_pyobj to obtain the topic. 
        '''
        pass
    
    def handleVoteResult(self,group,rfvId,vote):
        '''
        Default handler for the result of a vote (in member)
        '''
        pass
    
    def handleActionVoteRequest(self,group,rfvId,when):
        '''
        Default handler for request to vote an action in the future (in member)
        Implementation must recv/recv_pyobj to obtain the action topic. 
        '''
        pass
        
    def handleMessageToLeader(self,group):
        '''
        Default handler for messages sent to the leader (in leader)
        Leader implementation must immediately call recv/recv_pyobj on the group to obtain message. 
        '''
        pass
    
    def handleMessageFromLeader(self,group):
        '''
        Default handler for messages received from the leader (in member) 
        Member implementation must immediately call recv/recv_pyobj on the group to obtain message. 
        '''
        pass
    
    def handleMemberJoined(self,group,memberId):
        '''
        Default handler for 'member join' events
        '''  
        pass
    
    def handleMemberLeft(self,group,memberId):
        '''
        Default handler for 'member leave' events
        '''          
        pass
    
    def handleLeaderElected(self,group,leaderId):
        '''
        Default handler for 'leader elected' events
        '''  
        pass
    
    def handleLeaderExited(self,group,leaderId):
        '''
        Default handler for 'leader exited' events
        '''  
        pass
    
    def joinGroup(self,groupName,instName,groupPriority=GROUP_PRIORITY_MIN):
        if self.thread == None:
            self.thread = self.owner.thread
        group = self.coord.getGroup(groupName,instName)
        if group == None:
            group = self.coord.joinGroup(self.thread,groupName,instName,self.getLocalID())
            self.thread.addGroupSocket(group,groupPriority)
        return group

            