'''
Created on Mar 14, 2017

@author: riaps
'''

from riaps.run.comp import Component
import uuid
import os
from ModbusUartDevice import CommandFormat,ModbusCommands
#import pydevd


InputRegs = {'currentAC':2, 'voltageAC':120, 'power':40, 'time':'12:00 am', 'reg_extra1':'extra1', 'reg_extra2':'extra2'}
'''For Inverter control'''
HoldingRegs = {'unused':0, 'startCmd':1, 'stopCmd':1, 'power':1}
'''For RIAPS future
1.start/stop, 2.power command, 3. frequency shift from secondary control, 4. voltage magnitude shift from secondary control.
HoldingRegs = {'startStopCmd':0, 'powerCmd':1, 'freqShift':2, 'voltMagShift':4) 
'''

class ComputationalComponent(Component):
    def __init__(self):
        super().__init__()
#        pydevd.settrace(host='192.168.1.103',port=5678)
        self.uuid = uuid.uuid4().int
        self.pid = os.getpid()
        
        '''Setup Commands'''
        # MM TODO: setup list later after getting commands to work - 
        #CommandList = [CommandFormat(CommandFormat.command=ModbusCommands.READ_INPUTREG,CommandFormat.registerAddress=InputRegs.currentAC,CommandFormat.numberOfBytes=1,CommandFormat.values=0,CommandFormat.numberOfDecimals=1,CommandFormat.signedValue=False)]
        
        self.logger.info("ComputationalComponent: %s - starting",str(self.pid)) 
               

    def on_clock(self):
        now = self.clock.recv_pyobj() 
        self.logger.info("on_clock()[%s]: %s",str(self.pid),str(now))
        self.command.commandType = ModbusCommands.READ_INPUTREG
        self.command.registerAddress = InputRegs.currentAC
        self.command.values = 0 # not necessary for a read - placeholder
        self.command.numberOfBytes = 1 # not necessary for read one register
        self.command.numberOfDecimals = 1 # for data interpretation
        self.command.signedValue = False
        self.command = CommandFormat(self.command.commandType,self.command.registerAddress,self.command.values,self.command.numberOfBytes,self.command.numberOfDecimals,self.command.signedValue)
        
        msg = self.command
        self.logger.info('[%d] send req: %s' % (self.pid,msg))
        self.modbusReqPort.send_pyobj(msg)
        
    def on_modbusReqPort(self):
        msg = self.modbusReqPort.recv_pyobj()
        self.logger.info("on_modbusReqPort()[%s]: %s",str(self.pid),repr(msg))
        if self.command.commandType == ModbusCommands.READ_INPUTREG:
            logMsg = "Register " + str(self.command.registerAddress) + " value is " + str(msg)
        elif self.command.commandType == ModbusCommands.WRITE_HOLDINGREG:
            logMsg = "Wrote Register " + str(self.command.registerAddress)
        self.tx_modbusData.send_pyobj(logMsg)  # Send log data
        
    def __destroy__(self):
        self.logger.info("[%d] destroyed" % self.pid)
        
        
        