'''
Component class
Created on Oct 15, 2016

@author: riaps
'''

import threading
import zmq
import logging
from .exc import BuildError

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
        Create the control socket and connect it to the socket in the parent part part
        '''
        self.control = self.context.socket(zmq.PAIR)
        self.control.connect('inproc://part_' + self.name + '_control')
    
    def setupSockets(self):
        msg = self.control.recv_pyobj()
        if msg != "build":
            raise BuildError 
        for portName in self.parent.ports:
            res = self.parent.ports[portName].setupSocket()
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
        self.portMap = {}
        self.poller.register(self.control,zmq.POLLIN)
        self.portMap[self.control] = ""
        for portName in self.parent.ports:
            portObj = self.parent.ports[portName]
            portSocket = portObj.getSocket()
            portIsInput = portObj.inSocket()
            if portSocket != None:
                if portIsInput:
                    self.poller.register(portSocket,zmq.POLLIN)
                    self.portMap[portSocket] = portName
            
    def runCommand(self):
        res = False
        msg = self.control.recv_pyobj()
        if msg == "kill":
            self.logger.info("kill")
            res = True
        elif msg == "activate":
            self.logger.info("activate")
            pass                            
        else: 
            cmd = msg[0]
            if cmd == "portUpdate":
                self.logger.info("portUpdate")
                (_,portName,host,port) = msg
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
                portName = self.portMap[socket]
                func_ = getattr(self.instance, 'on_' + portName)
                func_()
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
        '''
        class_ = getattr(self,'__class__')
        className = getattr(class_,'__name__')
        self.owner = class_.OWNER                   # This is set in the parent part (temporarily)
        self.logger = logging.getLogger(className)
        self.logger.setLevel(logging.INFO)
        self.logger.propagate=False
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('%(levelname)s:%(asctime)s:%(name)s:%(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
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
        

    