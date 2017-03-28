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


RegSet = namedtuple('RegSet', ['idx', 'value'])
InputRegs = namedtuple('InputRegs', ['outputCurrent','outputVolt','voltPhase','time'])

'''For Inverter control'''
HoldingRegs = namedtuple('HoldingRegs',['unused', 'startStopCmd', 'power'])
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
        self.inputRegs = InputRegs(RegSet(0,45),RegSet(1,56),RegSet(2,78),RegSet(3,91))
        self.holdingRegs = HoldingRegs(RegSet(0,0),RegSet(1,55),RegSet(2,66))
        
        '''Setup Commands'''
        self.defaultNumOfRegs = 1
        self.dummyValue = [0]
        self.defaultNumOfDecimals = 0
        self.signedDefault = False

        self.logger.info("ComputationalComponent: %s - starting",str(self.pid)) 
               

    def on_clock(self):
        now = self.clock.recv_pyobj() 
        self.logger.info("on_clock()[%s]: %s",str(self.pid),str(now))

        '''Request:  Commands to send over Modbus - one command used at a time'''
        
        '''Read/Write (holding only) a single register'''
        #self.command = CommandFormat(ModbusCommands.READ_INPUTREG,self.inputRegs.time.idx,self.defaultNumOfRegs,self.dummyValue,self.defaultNumOfDecimals,self.signedDefault) 
        #self.command = CommandFormat(ModbusCommands.READ_HOLDINGREG,self.holdingRegs.startStopCmd.idx,self.defaultNumOfRegs,self.dummyValue,self.defaultNumOfDecimals,self.signedDefault)
        #self.values = [83]
        #self.command = CommandFormat(ModbusCommands.WRITE_HOLDINGREG,self.holdingRegs.power.idx,self.defaultNumOfRegs,self.values,self.defaultNumOfDecimals,self.signedDefault)
       
        '''Read/Write all input registers'''
        #numRegsToRead = len(self.inputRegs)
        #self.command = CommandFormat(ModbusCommands.READMULTI_INPUTREGS,self.inputRegs.outputCurrent.idx,numRegsToRead,self.dummyValue,self.defaultNumOfDecimals,self.signedDefault)

        '''Read/Write all holding registers'''
        self.command = CommandFormat(ModbusCommands.READMULTI_HOLDINGREGS,self.holdingRegs.unused.idx,len(self.holdingRegs),self.dummyValue,self.defaultNumOfDecimals,self.signedDefault)
        #self.values = [75,67]
        #self.command = CommandFormat(ModbusCommands.WRITEMULTI_HOLDINGREGS,self.holdingRegs.startStopCmd.idx,2,self.values,self.defaultNumOfDecimals,self.signedDefault)
         
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
            logMsg = "Wrote Registers " + str(self.command.registerAddress) + " to " + str(self.command.registerAddress + self.command.numberOfRegs - 1)
            
        self.tx_modbusData.send_pyobj(logMsg)  # Send log data
        
    def __destroy__(self):
        self.logger.info("[%d] destroyed" % self.pid)
        
        
        