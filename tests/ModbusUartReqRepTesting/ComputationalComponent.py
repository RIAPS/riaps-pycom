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
import time
import logging


''' Enable debugging to gather timing information on the code execution'''
debugMode = True

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

        if debugMode:
            self.logger.setLevel(logging.DEBUG)
            self.logger.handlers[0].setLevel(logging.DEBUG) # a workaround for hardcoded INFO level of StreamHandler logger
        else:
            self.logger.setLevel(logging.INFO)

        '''Setup Commands'''
        self.defaultNumOfRegs = 1
        self.dummyValue = [0]
        self.defaultNumOfDecimals = 0
        self.signedDefault = False
        self.ModbusPending = 0

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

        if debugMode:
            self.cmdSendStartTime = time.perf_counter()
            self.logger.debug("on_clock()[%s]: Send command to ModbusUartDevice at %f",str(self.pid),self.cmdSendStartTime)

        msg = self.command
        self.logger.info('on_clock()[%d]: send req: %s' % (self.pid,msg))
        if self.modbusReqPort.send_pyobj(msg):
            self.ModbusPending += 1
              
        '''Receive Response'''
        if self.ModbusPending > 0:
            msg = self.modbusReqPort.recv_pyobj()
            self.logger.info("on_modbusReqPort()[%s]: %s",str(self.pid),repr(msg))
            self.ModbusPending -= 1
#           pydevd.settrace(host='192.168.1.102',port=5678)

            if debugMode:
                self.cmdResultsRxTime = time.perf_counter()
                self.logger.debug("on_clock()[%s]: Received Modbus data from ModbusUartDevice at %f, time from cmd to data is %f ms",str(self.pid),self.cmdResultsRxTime,(self.cmdResultsRxTime-self.cmdSendStartTime)*1000)

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
