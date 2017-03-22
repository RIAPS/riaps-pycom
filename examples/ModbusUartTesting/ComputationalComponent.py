'''
Created on Mar 14, 2017

@author: riaps
'''

from riaps.run.comp import Component
import uuid
import os
from collections import namedtuple
from ModbusUartDevice import CommandFormat,ModbusCommands
import pydevd


InputRegs = namedtuple('InputRegs', ['currentAC','voltageAC','power','time','reg_extra1','reg_extra2'])

'''For Inverter control'''
HoldingRegs = namedtuple('HoldingRegs',['unused', 'startCmd', 'stopCmd', 'power'])
'''For RIAPS future
1.start/stop, 2.power command, 3. frequency shift from secondary control, 4. voltage magnitude shift from secondary control.
HoldingRegs = namedtuple('HoldingRegs',['startStopCmd', 'powerCmd', 'freqShift', 'voltMagShift']) 
'''
 
class ComputationalComponent(Component):
    def __init__(self):
        super().__init__()
#        pydevd.settrace(host='192.168.1.103',port=5678)
        self.uuid = uuid.uuid4().int
        self.pid = os.getpid()
        self.inputRegs = InputRegs(0,1,2,3,4,5)
        self.holdingRegs = HoldingRegs(0,1,2,3)
        
        '''Setup Commands'''
        # MM TODO: setup list later after getting commands to work - 
        #CommandList = [CommandFormat(CommandFormat.command=ModbusCommands.READ_INPUTREG,CommandFormat.registerAddress=InputRegs.currentAC,CommandFormat.numberOfBytes=1,CommandFormat.values=0,CommandFormat.numberOfDecimals=1,CommandFormat.signedValue=False)]
        
        self.logger.info("ComputationalComponent: %s - starting",str(self.pid)) 
               

    def on_clock(self):
        now = self.clock.recv_pyobj() 
        self.logger.info("on_clock()[%s]: %s",str(self.pid),str(now))

        '''Request:  Commands to send over Modbus'''
        self.command = CommandFormat(ModbusCommands.READ_INPUTREG,1,0,1,1,False) # values, numberOfBytes are not necessary for this command
        
        msg = self.command
        self.logger.info('[%d] send req: %s' % (self.pid,msg))
        self.modbusReqPort.send_pyobj(msg)
              
        '''Receive Response'''
        msg = self.modbusReqPort.recv_pyobj()
        self.logger.info("on_modbusReqPort()[%s]: %s",str(self.pid),repr(msg))
        pydevd.settrace(host='192.168.1.102',port=5678)  
        
        if self.command.commandType == ModbusCommands.READ_INPUTREG:
            logMsg = "Register " + str(self.command.registerAddress) + " value is " + str(msg)
        elif self.command.commandType == ModbusCommands.WRITE_HOLDINGREG:
            logMsg = "Wrote Register " + str(self.command.registerAddress)
        self.tx_modbusData.send_pyobj(logMsg)  # Send log data
        
    def __destroy__(self):
        self.logger.info("[%d] destroyed" % self.pid)
        
        
        