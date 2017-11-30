'''
Created on Mar 14, 2017

@author: riaps
'''

from riaps.run.comp import Component
import uuid
import os
from collections import namedtuple
from riapsmodbusuartpy import ModbusCommands
import pydevd
import time
import logging
import capnp
import CommandFormat_capnp
import ResponseFormat_capnp
import LogData_capnp


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
        self.dummyInputRegValues = [0,1,2,3]
        self.dummyHoldingRegValues = [0,1,2]
        self.successfulWrite = 1

        self.logger.info("ComputationalComponent: %s - starting",str(self.pid)) 


    def on_clock(self):
        now = self.clock.recv_pyobj()
        '''if debugMode:
            self.logger.info("on_clock()[%s]: %s",str(self.pid),str(now))'''
        
        '''Setup a Capnp Message'''
        command = CommandFormat_capnp.CommandFormat.new_message()

        '''Request:  Commands to send over Modbus - one command used at a time'''

        '''Read all input registers'''
        #command.commandType = ModbusCommands.READ_INPUTREGS
        #command.registerAddress = self.inputRegs.outputCurrent.idx
        #command.numberOfRegs = len(self.inputRegs)
        
        '''Read a single holding register'''
        #command.commandType = ModbusCommands.READ_HOLDINGREGS
        #command.registerAddress = self.holdingRegs.startStopCmd.idx
        #command.numberOfRegs = self.defaultNumOfRegs
        
        '''Write a single holding register'''
        #self.values = [83]
        #command.commandType = ModbusCommands.WRITE_HOLDINGREG
        #command.registerAddress = self.holdingRegs.startStopCmd.idx
        #command.numberOfRegs = self.defaultNumOfRegs
        #command.values = self.values
        
        '''Read all holding registers'''
        command.commandType = ModbusCommands.READ_HOLDINGREGS
        command.registerAddress = self.holdingRegs.unused.idx
        command.numberOfRegs = len(self.holdingRegs)
        
        '''Write multiple holding registers'''
        #self.values = [75,67]
        #command.commandType = ModbusCommands.WRITEMULTI_HOLDINGREGS
        #command.registerAddress = self.holdingRegs.startStopCmd.idx
        #command.numberOfRegs = len(self.values)
        #command.values = self.values

        '''Write/Read multiple holding registers'''
        #self.values = [57,76]
        #command.commandType = ModbusCommands.WRITEREAD_HOLDINGREGS
        #command.registerAddress = self.holdingRegs.startStopCmd.idx
        #command.numberOfRegs = len(self.values)
        #command.values = self.values
        #command.wreadRegAddress = self.holdingRegs.unused.idx
        #command.wreadNumOfRegs = len(self.holdingRegs)

        if debugMode:
            self.cmdSendStartTime = time.perf_counter()
            #self.logger.debug("on_clock()[%s]: Send command to ModbusUartDevice at %f",str(self.pid),self.cmdSendStartTime)

        '''Send Command'''
        cmdBytes = command.to_bytes()
        self.modbusReqPort.send_capnp(cmdBytes)

    def on_modbusReqPort(self):
        '''Receive Response'''
        bytes = self.modbusReqPort.recv_capnp()
        response = ResponseFormat_capnp.ResponseFormat.from_bytes(bytes)
#       pydevd.settrace(host='192.168.1.102',port=5678)

        if debugMode:
            self.cmdResultsRxTime = time.perf_counter()
            self.logger.debug("on_modbusReqPort()[%s]: Received Modbus data=%s from ModbusUartDevice at %f, time from cmd to data is %f ms",str(self.pid),repr(msg),self.cmdResultsRxTime,(self.cmdResultsRxTime-self.cmdSendStartTime)*1000)

        if response.commandType == ModbusCommands.READ_INPUTREGS or response.commandType == ModbusCommands.READ_HOLDINGREGS:
            valuesStr = " ".join(response.values)
            logMsg = "Register starting at " + str(response.registerAddress) + "has values of " + valuesStr
        elif response.commandType == ModbusCommands.WRITE_HOLDINGREG:
            if response.numberOfRegs == self.successfulWrite:
                logMsg = "Successfully wrote Register " + str(response.registerAddress)
            else:
                logMsg = "Failed to write Register " + str(response.registerAddress)
        elif response.commandType == ModbusCommands.WRITEMULTI_HOLDINGREGS:
            if response.numberOfRegs == self.successfulWrite:
                logMsg = "Successfully wrote Registers starting at " + str(response.registerAddress)
            else:
                logMsg = "Failed to write Registers starting at " + str(response.registerAddress)
        elif response.commandType == ModbusCommands.WRITEREAD_HOLDINGREGS:
            valuesStr = " ".join(response.values)
            logMsg = "Wrote Registers, then read " + response.numberOfRegs + " registers starting at Register " + str(response.registerAddress) + " which had values of " + valuesStr

        self.tx_modbusData.send_pyobj(logMsg)  # Send log data"""


    def __destroy__(self):
        self.logger.info("[%d] destroyed" % self.pid)
