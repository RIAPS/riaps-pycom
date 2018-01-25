'''
Part class
Created on Oct 9, 2016

@author: run
'''
import importlib
import threading
import zmq
import time

from enum import Enum

from .pubPort import PubPort
from .subPort import SubPort
from .cltPort import CltPort
from .srvPort import SrvPort
from .reqPort import ReqPort
from .repPort import RepPort
from .qryPort import QryPort
from .ansPort import AnsPort
from .timPort import TimPort
from .insPort import InsPort
from .exc import StateError
from .comp import ComponentThread
from .exc import SetupError
from .exc import ControlError
from .exc import BuildError
import logging

class Part(object):
    '''
    Part class to encapsulate and manage component (and its thread)
    '''
    class State(Enum):          # Component state codes
        Starting = 0
        Initial = 1
        Ready = 2
        Active = 3
        Checkpointing = 4
        Inactive = 5
        Passive = 6
        Destroyed = 7
        
    _mods = {}
    @property
    def mods(self):
        return self._mods
    @mods.setter
    def mods(self,val):
        self._mods = val

    def __init__(self, parentActor, iTypeDef, iName, iTypeName, iArgs):
        '''
        Construct the Part object, load the component implementation and construct its object
        '''
        self.logger = logging.getLogger(__name__)
        self.state = Part.State.Starting
        self.name = iName
        self.parent = parentActor
        self.type = iTypeDef
        self.typeName = self.type['name']
        self.args = iArgs
        self.load()
        self.class_ = getattr(self.module_, self.typeName)
        self.class_.OWNER = self            # Trick to set the OWNER of the component 
        self.logger.info('Constructing %s of type %s' % (iName,self.typeName))
        self.instance = self.class_(**self.args)    # Run the component constructor
        self.class_.OWNER = None
        self.context = parentActor.context
        self.control = None
        self.thread = None
        self.buildAllPorts(self.type["ports"])      # Build all the ports of the component
        self.state = Part.State.Initial
        
    def getName(self):
        return self.name
    
    def getTypeName(self):
        return self.typeName
    
    def getActorName(self):
        return self.parent.getActorName()

    def getAppName(self):
        return self.parent.getAppName()

    def getActorID(self):
        return self.parent.getActorID()
        
    def load(self):
        '''
        Load the component implementation code
        '''
        if self.typeName not in self.mods:          # If not loaded yet
            try:
                self.module_ = importlib.import_module(self.typeName)   # Execute the loader
                self.mods[self.typeName] = self.module_ 
            except Exception as e:
                print ("%s: %s" % (type(e),e))
                raise
        else:
            self.module_ = self.mods[self.typeName] 

    def buildPorts(self,res,key,ports,class_):
        '''
        Build the port objects of a kind of this part
        '''
        portDict = ports[key]
        for port in portDict:
            portName = port
            portSpec = portDict[portName]
            res[portName] = class_(self,portName,portSpec)
        
    def buildAllPorts(self,portSpecs):
        '''
        Build all the ports of the part
        '''
        self.ports = {}
        self.buildPorts(self.ports,'pubs',portSpecs,PubPort)
        self.buildPorts(self.ports,'subs',portSpecs,SubPort)
        self.buildPorts(self.ports,'clts',portSpecs,CltPort)
        self.buildPorts(self.ports,'srvs',portSpecs,SrvPort)
        self.buildPorts(self.ports,'reqs',portSpecs,ReqPort)
        self.buildPorts(self.ports,'reps',portSpecs,RepPort)
        self.buildPorts(self.ports,'qrys',portSpecs,QryPort)
        self.buildPorts(self.ports,'anss',portSpecs,AnsPort)
        self.buildPorts(self.ports,'tims',portSpecs,TimPort)
        self.buildPorts(self.ports,'inss',portSpecs,InsPort)
        for portName in self.ports:
            # The port will be accessible in the component instance under its own name 
            setattr(self.instance,portName,self.ports[portName]) 
         
    def setupPorts(self,ports):
        '''
        Set up all the ports of this part
        '''
        for portName in ports:
            ports[portName].setup()
            
    def sendControl(self,cmd,timeOut):
        '''
        Send a control message to component thread
        '''
        if self.control != None:
            self.control.setsockopt(zmq.SNDTIMEO,timeOut) 
            self.control.send_pyobj(cmd)
        
    def setup(self):
        '''
        Set up the part and change its state to Ready
        '''
        if self.state != Part.State.Initial:
            raise StateError("Invalid state %s in setup()" % self.state)
        
        # Create the control socket for communicating with the component thread
        self.control = self.context.socket(zmq.PAIR)
        self.control.bind('inproc://part_' + self.name + '_control')
       
        self.setupPorts(self.ports)
        
        self.thread = ComponentThread(self)         # Create and launch the component thread
        self.thread.start() 
        time.sleep(0.001)                          # Hack to yield to the component thread
        self.sendControl("build",-1)                # Command the component thread to build itself
        prefix = (self.name,self.typeName)
        queue = []
        while 1:                                    # Wait for a response from the component thread
            msg = self.control.recv_pyobj()
            if msg == "done":                       # OK, we are done
                break;
            res = msg                               # Otherwise append the response to the queue
            if res[0] == 'pub' or res[0] == 'sub' or \
                    res[0] == 'clt' or res[0] == 'srv' or \
                    res[0] == 'req' or res[0] == 'rep' or \
                    res[0] == 'qry' or res[0] == 'ans' :
                queue.append(prefix + res)
            else:
                raise BuildError("invalid response from ComponentThread %s" % msg)
        # Process all component thread responses 
        for elt in queue:
            self.parent.registerEndpoint(elt) 
        self.state = Part.State.Ready
        
    def handlePortUpdate(self,portName,host,port):
        '''
        Handle a port update message coming from the discovery service
        '''
        self.logger.info("handlePortUpdate %s %s %s" % (portName,str(host),str(port)))
        msg = ("portUpdate",portName,host,port)
        # print(msg)
        self.control.send_pyobj(msg)        # Relay message to component thread
        rep = self.control.recv_pyobj()     # Wait for an OK response
        if rep == "ok" :
            pass
        else:
            pass

    def activatePorts(self,ports):
        '''
        Activate all ports of this part
        '''
        for portName in ports:
            ports[portName].activate()
        
    def activate(self):
        '''
        Activate this part
        '''
        if not self.state in (Part.State.Ready,Part.State.Passive,Part.State.Inactive):
            raise StateError("Invalid state %s in activate()" % self.state)
        self.activatePorts(self.ports)          # Activate parts
        self.sendControl("activate",-1)         # Send activation command to component thread
        self.state = Part.State.Active

    def deactivatePorts(self,ports):
        '''
        Deactivate all ports
        '''
        for portName in ports:
            ports[portName].deactivate()
            
    def deactivate(self):
        if self.state != Part.State.Active:
            raise StateError("Invalid state %s in deactivate()" % self.state)
        self.deactivatePorts(self.ports)
#        self.sendControl("deactivate",-1)         # Send deactivation command to component thread
        self.state = Part.State.Inactive
    
    def passivate(self):
        if self.state != Part.State.Active:
            raise StateError("Invalid state %s in passivate()" % self.state)
#        self.sendControl("passivate",-1)         # Send passivate command to component thread
        self.state = Part.State.Passive
    
    def reactivate(self):
        if self.state != Part.State.Ready:
            raise StateError("Invalid state %s in reactivate()" % self.state)
        self.state = Part.State.Active
        
    def checkpoint(self):
        if self.state != Part.State.Active:
            raise StateError("Invalid state %s in checkpoint()" % self.state)
        # Checkpoint
    
    def destroy(self):
        if self.state == Part.State.Destroyed:
            raise StateError("Invalid state %s in destroy()" % self.state)
        # Destroy thread
    
    def handleCPULimit(self):
        self.logger.info("handleCPULimit - %s:%s" % (self.name,self.typeName))
        msg = ("limitCPU",)
        # print(msg)
        self.control.send_pyobj(msg)        # Relay message to component thread
        rep = self.control.recv_pyobj()     # Wait for an OK response
        if rep == "ok" :
            pass
        else:
            pass
        
    def handleMemLimit(self):
        self.logger.info("handleMemLimit - %s:%s" % (self.name,self.typeName))
        msg = ("limitMem",)
        # print(msg)
        self.control.send_pyobj(msg)        # Relay message to component thread
        rep = self.control.recv_pyobj()     # Wait for an OK response
        if rep == "ok" :
            pass
        else:
            pass
    
    def handleSpcLimit(self):
        self.logger.info("handleSpcLimit - %s:%s" % (self.name,self.typeName))
        msg = ("limitSpc",)
        # print(msg)
        self.control.send_pyobj(msg)        # Relay message to component thread
        rep = self.control.recv_pyobj()     # Wait for an OK response
        if rep == "ok" :
            pass
        else:
            pass
        
    def terminate(self):
        self.logger.info("terminating")
        self.sendControl("kill",-1)         # Send message to the thread to kill itself
        time.sleep(0.001)
        if self.thread != None:
            self.thread.join()
        for portObj in self.ports.values():
            portObj.terminate()
        self.logger.info("terminated")
        
