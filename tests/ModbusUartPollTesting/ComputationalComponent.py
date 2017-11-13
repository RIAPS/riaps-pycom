'''
Created on Mar 14, 2017

@author: riaps
'''

from riaps.run.comp import Component
import uuid
import os
from collections import namedtuple
from ModbusUartPollDevice import ModbusRequest,ModbusCommand,RequestFormat,CommandFormat
import pydevd
import time
import logging

''' Enable debugging to gather timing information on the code execution'''
debugMode = True

RegSet = namedtuple('RegSet', ['idx', 'value'])
InputRegs = namedtuple('InputRegs', ['outputCurrent','outputVolt','voltPhase','time'])

'''For Inverter control'''
HoldingRegs = namedtuple('HoldingRegs',['unused', 'startStopCmd', 'power'])
# MM TODO:  add 'reactive_power' after initial measurement comparison - HoldingRegs = namedtuple('HoldingRegs',['unused', 'startStopCmd', 'power','reactive_power'])
'''For RIAPS future
1.start/stop, 2.power command, 3. frequency shift from secondary control, 4. voltage magnitude shift from secondary control.
HoldingRegs = namedtuple('HoldingRegs',['startStopCmd', 'powerCmd', 'freqShift', 'voltMagShift']) 
'''

class ComputationalComponent(Component):
    def __init__(self):
        super().__init__()
        if debugMode:
            self.logger.setLevel(logging.DEBUG)
            self.logger.handlers[0].setLevel(logging.DEBUG) # a workaround for hardcoded INFO level of StreamHandler logger
        else:
            self.logger.setLevel(logging.INFO)

        # pydevd.settrace(host='192.168.1.103',port=5678)
        self.uuid = uuid.uuid4().int
        self.pid = os.getpid()
        self.inputRegs = InputRegs(RegSet(0,45),RegSet(1,56),RegSet(2,78),RegSet(3,91))
        self.holdingRegs = HoldingRegs(RegSet(0,0),RegSet(1,55),RegSet(2,66))

        '''Setup Commands'''
        self.defaultNumOfRegs = 1
        self.dummyValue = [0]
        self.defaultNumOfDecimals = 0
        self.signedDefault = False
        self.modbusPending = 0
        self.pollRequested = False
        self.pollFreq = 0
        self.noData = None

        self.logger.info("__init__[%s]: starting",str(self.pid))

    def on_clock(self):
        now = self.clock.recv_pyobj()
        if debugMode:
            self.logger.info("on_clock()[%s]: %s",str(self.pid),str(now))
        
        '''Request:  Query Commands to send over Modbus - one command used at a time, options to test below'''

        '''Read/Write (holding only) a single register'''
        #Option1: self.command = CommandFormat(ModbusCommand.READ_INPUTREG,self.inputRegs.time.idx,self.defaultNumOfRegs,self.dummyValue,self.defaultNumOfDecimals,self.signedDefault)
        #Option2: self.command = CommandFormat(ModbusCommand.READ_HOLDINGREG,self.holdingRegs.startStopCmd.idx,self.defaultNumOfRegs,self.dummyValue,self.defaultNumOfDecimals,self.signedDefault)
        #Option3: self.values = [83]
        #         self.command = CommandFormat(ModbusCommand.WRITE_HOLDINGREG,self.holdingRegs.power.idx,self.defaultNumOfRegs,self.values,self.defaultNumOfDecimals,self.signedDefault)

        '''Read/Write all input registers'''
        #Option4: numRegsToRead = len(self.inputRegs)
        #         self.command = CommandFormat(ModbusCommand.READMULTI_INPUTREGS,self.inputRegs.outputCurrent.idx,numRegsToRead,self.dummyValue,self.defaultNumOfDecimals,self.signedDefault)

        '''Read/Write all holding registers'''
        #Option5:
        self.command = CommandFormat(ModbusCommand.READMULTI_HOLDINGREGS,self.holdingRegs.unused.idx,len(self.holdingRegs),self.dummyValue,self.defaultNumOfDecimals,self.signedDefault)

        #Option6: self.values = [75,67]
        #         self.command = CommandFormat(ModbusCommand.WRITEMULTI_HOLDINGREGS,self.holdingRegs.startStopCmd.idx,2,self.values,self.defaultNumOfDecimals,self.signedDefault)

        '''Setup Request - requestType and requestData '''
        self.requestCommand = RequestFormat(ModbusRequest.SINGLE_RW_CMD,self.command)

        self.sendModbusRequest()

        '''Polling Setup Command'''
        #readCommand = CommandFormat(ModbusCommand.READMULTI_INPUTREGS,self.inputRegs.outputCurrent.idx,numRegsToRead,self.dummyValue,self.defaultNumOfDecimals,self.signedDefault)
        #writeCommand = CommandFormat(ModbusCommand.WRITE_HOLDINGREG,self.holdingRegs.power.idx,self.defaultNumOfRegs,value,self.defaultNumOfDecimals,self.signedDefault)
        #self.pollFreq = 25 # 25 Hz
        #self.requestCommand = RequestFormat(ModbusRequest.SETUP_POLLING,SamplingRequest(readCommand,writeCommand,self.pollFreq))

        '''Setup Polling Write Value'''
        #value = [83]
        #self.requestCommand = RequestFormat(ModbusRequest.SET_POLL_WRITE_VALUE,value)

        '''Start Polling Command'''
        # self.requestCommand = RequestFormat(ModbusRequest.START_POLLING,self.noData)

        '''Stop Polling Command'''
        #self.requestCommand = RequestFormat(ModbusRequest.STOP_POLLING,self.noData)


    def sendModbusRequest(self):
        if debugMode:
            self.cmdSendStartTime = time.perf_counter()  
            self.logger.debug("sendModbusRequest()[%s]: Send command=%s to ModbusUartDevice at %f",str(self.pid),msg,self.cmdSendStartTime)

        msg = self.requestCommand
        if self.modbusReqPort.send_pyobj(msg):
            self.modbusPending += 1

        '''Receive Response - ACK or ERROR'''
        if self.modbusPending > 0:
            msg = self.modbusReqPort.recv_pyobj()
            if debugMode:
                self.logger.info("sendModbusRequest()[%s] receive response: %s",str(self.pid),repr(msg))
            self.modbusPending -= 1
            # pydevd.settrace(host='192.168.1.102',port=5678)
            if msg=='ACK':
                if debugMode:
                    self.cmdAckRxTime = time.perf_counter()
                    self.logger.debug("sendModbusRequest()[%s]: Received ACK from ModbusUartDevice at %f, time from cmd to get ACK back is %f ms",
                                      str(self.pid),self.cmdAckRxTime,(self.cmdAckRxTime-self.cmdSendStartTime)*1000)


    def on_rx_modbusData(self):
        msg = self.rx_modbusData.recv_pyobj()
        self.logger.info("on_rx_modbusData()[%s]: %s",str(self.pid),repr(msg))
        # pydevd.settrace(host='192.168.1.102',port=5678)

        if debugMode:
            self.cmdResultsRxTime = time.perf_counter()     
            self.logger.debug("on_rx_modbusData()[%s]: Received Modbus data=%s from ModbusUartDevice at %f, time from cmd to data is %f ms",
                              str(self.pid),repr(msg),self.cmdResultsRxTime,(self.cmdResultsRxTime-self.cmdSendStartTime)*1000)

        if self.command.commandType == ModbusCommand.READ_INPUTREG or self.command.commandType == ModbusCommand.READ_HOLDINGREG:
            logMsg = "Register " + str(self.command.registerAddress) + " value is " + str(msg)
        elif self.command.commandType == ModbusCommand.READMULTI_INPUTREGS or self.command.commandType == ModbusCommand.READMULTI_HOLDINGREGS:
            logMsg = "Register " + str(self.command.registerAddress) + " values are " + str(msg)
        elif self.command.commandType == ModbusCommand.WRITE_HOLDINGREG:
            logMsg = "Wrote Register " + str(self.command.registerAddress)
        elif self.command.commandType == ModbusCommand.WRITEMULTI_HOLDINGREGS:
            logMsg = "Wrote Registers " + str(self.command.registerAddress) + " to " + str(self.command.registerAddress + self.command.numberOfRegs - 1)

        self.tx_modbusData.send_pyobj(logMsg)  # Send log data
        if debugMode:
            self.logger.info("on_rx_modbusData()[%s]: Sent log message - %s",str(self.pid),repr(logMsg))


    def __destroy__(self):
        self.logger.info("__destroy__[%s]",str(self.pid))