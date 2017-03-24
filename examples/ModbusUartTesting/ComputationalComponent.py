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
        self.defaultNumOfBytes = 1
        self.dummyValue = [0]
        self.defaultNumOfDecimals = 0
        self.signedDefault = False

        # MM TODO: setup list later after getting commands to work - 
        #CommandList = [CommandFormat(CommandFormat.command=ModbusCommands.READ_INPUTREG,CommandFormat.registerAddress=InputRegs.currentAC,CommandFormat.numberOfBytes=1,CommandFormat.values=0,CommandFormat.numberOfDecimals=1,CommandFormat.signedValue=False)]
        
        self.logger.info("ComputationalComponent: %s - starting",str(self.pid)) 
               

    def on_clock(self):
        now = self.clock.recv_pyobj() 
        self.logger.info("on_clock()[%s]: %s",str(self.pid),str(now))

        '''Request:  Commands to send over Modbus - one command used at a time'''
        
        '''Read/Write (holding only) a single register'''
        #self.command = CommandFormat(ModbusCommands.READ_INPUTREG,self.inputRegs.power,self.defaultNumOfBytes,self.dummyValue,self.defaultNumOfDecimals,self.signedDefault) 
        self.command = CommandFormat(ModbusCommands.READ_HOLDINGREG,self.holdingRegs.power,self.defaultNumOfBytes,self.dummyValue,self.defaultNumOfDecimals,self.signedDefault)
        #self.values = [83]
        #self.command = CommandFormat(ModbusCommands.WRITE_HOLDINGREG,self.holdingRegs.power,self.defaultNumOfBytes,self.values,self.defaultNumOfDecimals,self.signedDefault)
       
        '''Read/Write all input registers'''
        #self.command = CommandFormat(ModbusCommands.READMULTI_INPUTREGS,self.inputRegs.currentAC,len(self.inputRegs),self.dummyValue,self.defaultNumOfDecimals,self.signedDefault)

        '''Read/Write all holding registers'''
        #self.command = CommandFormat(ModbusCommands.READMULTI_HOLDINGREGS,self.holdingRegs.unused,len(self.holdingRegs),self.dummyValue,self.defaultNumOfDecimals,self.signedDefault)
        #self.values = [34,45,56,67]
        #self.command = CommandFormat(ModbusCommands.WRITEMULTI_HOLDINGREGS,self.holdingRegs.unused,len(self.holdingRegs),self.values,self.defaultNumOfDecimals,self.signedDefault)
         
        msg = self.command
        self.logger.info('[%d] send req: %s' % (self.pid,msg))
        self.modbusReqPort.send_pyobj(msg)
              
        '''Receive Response'''
        msg = self.modbusReqPort.recv_pyobj()
        self.logger.info("on_modbusReqPort()[%s]: %s",str(self.pid),repr(msg))
#        pydevd.settrace(host='192.168.1.102',port=5678)  
        
        if self.command.commandType == ModbusCommands.READ_INPUTREG or self.command.commandType == ModbusCommands.READ_HOLDINGREG:
            logMsg = "Register " + str(self.command.registerAddress) + " value is " + str(msg)
        elif self.command.commandType == ModbusCommands.READMULTI_INPUTREGS or self.command.commandType == ModbusCommands.READMULTI_HOLDINGREGS:
            logMsg = "Register " + str(self.command.registerAddress) + " values are " + str(msg)
        elif self.command.commandType == ModbusCommands.WRITE_HOLDINGREG:
            logMsg = "Wrote Register " + str(self.command.registerAddress)
        elif self.command.commandType == ModbusCommands.WRITEMULTI_HOLDINGREGS:
            logMsg = "Wrote Registers " + str(self.command.registerAddress) + " to " + str(self.command.registerAddress + self.command.numberOfBytes)
            
        self.tx_modbusData.send_pyobj(logMsg)  # Send log data
        
    def __destroy__(self):
        self.logger.info("[%d] destroyed" % self.pid)
        
        
        