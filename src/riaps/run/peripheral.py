'''
Peripheral class - encapsulates a device, used in an app actor
Created on Jan 6, 2017

@author: riaps
'''
'''
Part class
Created on Oct 9, 2016

@author: run
'''

from enum import Enum

from .exc import StateError
from .exc import SetupError
from .exc import ControlError
from .exc import BuildError
import logging

class Peripheral(object):
    '''
    Peripheral class to encapsulate access to a device component
    Note: implements a public interface compatible with a part 
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
        Construct the Peripheral object
        '''
        self.logger = logging.getLogger(__name__)
        self.logger.info("building device component %s:%s" % (iName,iTypeName))
        self.state = Peripheral.State.Starting
        self.name = iName
        self.parent = parentActor
        self.type = iTypeDef
        self.typeName = self.type['name']
        self.args = iArgs
        self.state = Peripheral.State.Initial
        
    def getControl(self):
        return None
    
    def setup(self):
        '''
        Set up the peripheral and change its state to Ready
        '''
        if self.state != Peripheral.State.Initial:
            raise StateError("Invalid state %s in setup()" % self.state)
        self.logger.info("setting up device component")
        # Ask parent actor to contact devm to start our dca
        msg = (self.typeName,self.args)
        _resp = self.parent.registerDevice(msg)

        self.state = Peripheral.State.Ready
        
    def handleUpdate(self,msg):
        '''
        Handle an update message coming from the devm service
        '''
        # print(msg)
        pass
      
    def activate(self):
        '''
        Activate this peripheral
        '''
        if not self.state in (Peripheral.State.Ready,Peripheral.State.Passive,Peripheral.State.Inactive):
            raise StateError("Invalid state %s in activate()" % self.state)
        # Now we are active
 
        self.state = Peripheral.State.Active

    def deactivate(self):
        if self.state != Peripheral.State.Active:
            raise StateError("Invalid state %s in deactivate()" % self.state)

        # Now we are inactive
        self.state = Peripheral.State.Inactive
    
    def passivate(self):
        if self.state != Peripheral.State.Active:
            raise StateError("Invalid state %s in passivate()" % self.state)
#        self.sendControl("passivate",-1)         # Send passivate command to component thread
        self.state = Peripheral.State.Passive
    
    def reactivate(self):
        if self.state != Peripheral.State.Ready:
            raise StateError("Invalid state %s in reactivate()" % self.state)
        self.state = Peripheral.State.Active
        
    def checkpoint(self):
        if self.state != Peripheral.State.Active:
            raise StateError("Invalid state %s in checkpoint()" % self.state)
        # Checkpoint
    
    def destroy(self):
        if self.state == Peripheral.State.Destroyed:
            raise StateError("Invalid state %s in destroy()" % self.state)
        # Destroy thread
        
    def handleReinstate(self):
        pass
    
    def handleCPULimit(self):
        # Peripheral devices are just placeholders 
        # for the device components that live inside
        # device actors. 
        pass 
        
    def handleMemLimit(self):
        pass

    def handleSpcLimit(self):
        pass
        
    def handleNetLimit(self):
        pass

    def handleNICStateChange(self,state):
        pass
        
    def handlePeerStateChange(self,state,uuid):
        pass
    
    def terminate(self):
        self.logger.info("terminating %s" % self.typeName)
        msg = (self.typeName,)
        resp = self.parent.unregisterDevice(msg)
        self.logger.info("terminating %s" % self.typeName)
    
