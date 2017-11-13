'''
Created on Mar 14, 2017
Modified in November 2017

@author: riaps

The Modbus polling device can either execute a single read or write command or poll a read/write
command set.  The polling can to read only, write only or write then read a set of registers on a
periodic bases.  Commands arrive on the ModbusRequest port and the data goes out the modbusDataPub
port.  Dummy data is sent back for a write to indicate the action was complete.  The write then
read will only send back the read data.

To setup polling, the application component should send the following sequence of requests:
    1) Setup polling (ModbusCommand to read, ModbusCommand to write, frequency of polling)
    4) Start polling
    5) Optionally, update the write value before the next polling period
    6) Stop polling

Application Developer Note: When developing an application that intends to poll, carefully 
consider the system timeline of the application activity to make sure the desired Modbus 
interaction can happen during the specified polling periodicity.  Each Modbus command 
within the inner thread will take around 7 ms physically interact with the Modbus.

****** MM TODO - update 7 ms to reflect effect of this code ******

Installation Note:  
This module utilizes the MinimalModbus (which utilizes pySerial).
Both need to be installed in the development environment.
    $ sudo pip3 install minimalmodbus  (which should install pySerial)
'''

from riaps.run.comp import Component
import logging
import os
import sys
import serial
import time
import threading
import queue
import zmq
from serialModbusLib.serialModbusComm import SerialModbusComm,PortConfig
from collections import namedtuple
from enum import Enum
#import pydevd

''' Enable debugging to gather timing information on the code execution'''
debugMode = True


''' 
Requester Commands Available
'''
class ModbusRequest(Enum):
    NONE                   = 0
    SINGLE_RW_CMD          = 1
    SETUP_POLLING          = 2
    SET_POLL_WRITE_VALUE   = 3
    START_POLLING          = 4
    STOP_POLLING           = 5
    
class ModbusCommand(Enum):
    NONE                   = 0
    READ_BIT               = 1
    READ_INPUTREG          = 2
    READ_HOLDINGREG        = 3
    READMULTI_INPUTREGS    = 4
    READMULTI_HOLDINGREGS  = 5
    WRITE_BIT              = 6
    WRITE_HOLDINGREG       = 7
    WRITEMULTI_HOLDINGREGS = 8

'''
An application component can either request a single query of the modbus using the 
ModbusCommands or poll any set of ModbusCommands (controlling the start and stop)

The 'requestType' possible are identified in the ModbusRequest enum
The 'requestData' is dependent on the requestType with the following expectations:
    - requestType = SINGLE_RW_CMD --> requestData = CommandFormat() for read or write request
    - requestType = SETUP_POLLING --> requestData = SamplingRequest() data with read command, 
                                                    write command and frequency
    - requestType = SET_POLL_WRITE_VALUE --> requestData = value to be written in write command,
                                             this value is expected to be updated during each poll period
    - requestType = START_POLLING  --> requestData = N/A
    - requestType = STOP_POLLING   --> requestData = N/A
'''
RequestFormat = namedtuple('RequestFormat', ['requestType','requestData'])

SamplingRequest = namedtuple('SamplingRequest', ['readCmd','writeCmd','pollFreq'])

''' 
This configures the register sets (a Modbus command) that the application is interested in 
reading/writing.  
'''
CommandFormat = namedtuple('CommandFormat', ['commandType','registerAddress','numberOfRegs','values',
                                             'numberOfDecimals','signedValue'])


'''
This thread will be the interface between the minimalmodbus library communication with the 
hardware and the RIAPS ModbusUartPollDevice component.  It will run handle incoming commands and 
polling (if started).

ModbusRequests will be passed from the ModbusUartPollDevice component to this thread using the command inside port.
Queries will be executed by calling into the minimalmodbus library with a blocking call, 
then data will be published out the data inside port.  

Polling is setup as indicated above.  Polling begins when a request to start poll is received 
through the command inside port, along with the polling frequency desired (in Hz).  Polling 
will continue until a stop polling is received. 
'''
class ModbusUartPollThread(threading.Thread):
    def __init__(self, component, cmds, data):
        threading.Thread.__init__(self)
        self.terminated = threading.Event()
        self.active = threading.Event()
        
        self.component = component
        self.data = data
        self.cmds = cmds
        self.pid = os.getpid()
        
        self.modbusReady = False
        self.modbus = SerialModbusComm(self,self.component.slaveAddressDecimal,self.component.port_config)
        
        self.dummyValue = [0]
        self.pollReadCmd = CommandFormat(ModbusCommand.NONE,0,0,self.dummyValue,0,False)
        self.pollWriteCmd = CommandFormat(ModbusCommand.NONE,0,0,self.dummyValue,0,False)
        self.pollWriteValue = self.dummyValue
        self.pollFreq = 0     # units are ms
        
        self.component.logger.info("thread __init__ [%s]: init thread",self.pid)

    def run(self):
        self.dataPlug = self.data.setupPlug(self)
        t_last_sample = 0

        if self.terminated.is_set(): 
            return
        
        if not self.modbusReady:
            self.enableModbus()
                        
        while True:
            self.active.wait(None)
            if self.terminated.is_set():
                self.disableModbus()
                break
            if self.active.is_set():
                if self.pollFreq > 0:
                    t_wait = t_last_sample + 1 / self.pollFreq - time.time()
                    if t_wait < 0:
                        self.component.logger.warning('thread run()[%s]: Sampling overrun by: %f s',str(self.pid),t_wait)
                        t_wait %= t_wait
                        # optional: send last sample value as many times as 
                        # needed to catch-up
                else:
                    t_wait = None
            
                try:
                    cmd = self.cmds.get(timeout=t_wait)
                    if debugMode:
                        self.cmdRxByThreadTime = time.perf_counter()
                        self.component.logger.debug("thread run()[%s]: Received requested Modbus command request=%s, data=%s, at %f",
                                                    str(self.pid),cmd.requestType.name,cmd.requestData,self.cmdRxByThreadTime)

                    if cmd.requestType == ModbusRequest.SINGLE_RW_CMD:
                        self.processModbusCommand(cmd.requestData)

                    elif cmd.requestType == ModbusRequest.SETUP_POLLING:
                        self.pollReadCmd = cmd.requestData.readCmd
                        self.pollWriteCmd = cmd.requestData.writeCmd
                        self.pollFreq = cmd.requestData.pollFreq
                        if debugMode:
                            self.component.logger.info("thread run()[%s]: Polling setup - readCmd=%s, writeCmd=%, freq=%s",
                                                       str(self.pid),repr(self.pollReadCmd),repr(self.pollWriteCmd),
                                                       repr(self.pollFreq))

                    elif cmd.requestType == ModbusRequest.SET_POLL_WRITE_VALUE:
                        self.pollWriteValue = cmd.requestData
                        if debugMode:
                            self.component.logger.info("thread run()[%s]: Polling write value setup - value=%s",
                                                       str(self.pid),repr(self.pollWriteValue))

                    elif cmd.requestType == ModbusRequest.START_POLLING:
                        t_last_sample = time.time()
                        if debugMode:
                            self.pollStartTime = time.perf_counter()
                            if debugMode:
                                self.component.logger.info("thread run()[%s]: Polling started at %f",
                                                           str(self.pid), repr(self.pollStartTime))

                    elif cmd.requestType == ModbusRequest.STOP_POLLING:
                        t_last_sample = 0
                        if debugMode:
                            self.pollStopTime = time.perf_counter()
                            if debugMode:
                                self.component.logger.info("thread run()[%s]: Polling stopped at %f",
                                                           str(self.pid), repr(self.pollStopTime))

                except queue.Empty:
                    t_last_sample = time.time()
                    if debugMode:
                        self.pollPeriodStartTime = time.perf_counter()
                        self.component.logger.debug("thread run()[%s]: Polling period reached at %f",
                                                    str(self.pid), self.pollPeriodStartTime)
                    self.do_polling()


    def processModbusCommand(self,rxCommandData):
        self.unpackRegisterCommand(rxCommandData)
        if debugMode:
            self.component.logger.info("thread run()[%s]: Sending single R/W command to Modbus", str(self.pid))
        responseValue = self.sendModbusCommand()

        if debugMode:
            self.dataRxModbusTime = time.perf_counter()
            self.component.logger.debug("thread run()[%s]: Sending data back to ModbusUartDevice responseValue=%s at %f, time from cmd to data sent is %f ms",
                                        str(self.pid), responseValue, self.dataRxModbusTime,
                                        (self.dataRxModbusTime - self.cmdRxByThreadTime) * 1000)

        # Publish Modbus read results (999 sent if a write was performed - see sendModbusCommand return value)
        self.dataPlug.send_pyobj(responseValue)
        if debugMode:
            self.component.logger.info("thread run()[%s]: Sending data back to ModbusUartDevice",str(self.pid))
            # pydevd.settrace(host='192.168.1.102',port=5678)


    def unpackRegisterCommand(self,rxCommandData):
        self.commandType = rxCommandData.commandType
        self.registerAddress = rxCommandData.registerAddress
        self.numberOfRegs = rxCommandData.numberOfRegs
        self.numberOfDecimals = rxCommandData.numberOfDecimals
        self.signedValue = rxCommandData.signedValue
        self.values = rxCommandData.values
       
        
    def sendModbusCommand(self):
        if debugMode:
            t0 = time.perf_counter()     
            #self.component.logger.debug("thread sendModbusCommand()[%s]: Sending command to Modbus library at %f",str(self.pid),t0)

        value = 999  # large invalid value
        
        if self.commandType == ModbusCommand.READ_INPUTREG:
            value = self.modbus.readInputRegValue(self.registerAddress, self.numberOfDecimals, self.signedValue)
            '''self.component.logger.info("thread sendModbusCommand()[%s]: Sent command %s, register=%d, numOfDecimals=%d, signed=%s",
                                       str(self.pid),ModbusCommand.READ_INPUTREG.name,self.registerAddress,
                                       self.numberOfDecimals,str(self.signedValue))'''
        elif self.commandType == ModbusCommand.READ_HOLDINGREG:
            value = self.modbus.readHoldingRegValue(self.registerAddress, self.numberOfDecimals, self.signedValue)
            '''self.component.logger.info("thread sendModbusCommand()[%s]: Sent command %s, register=%d, numOfDecimals=%d, signed=%s",
                                       str(self.pid),ModbusCommand.READ_HOLDINGREG.name,self.registerAddress,
                                       self.numberOfDecimals,str(self.signedValue))'''
        elif self.commandType == ModbusCommand.READMULTI_INPUTREGS:
            value = self.modbus.readMultiInputRegValues(self.registerAddress, self.numberOfRegs)
            '''self.component.logger.info("thread sendModbusCommand()[%s]: Sent command %s, register=%d, numOfRegs=%d",
                                       str(self.pid),ModbusCommand.READMULTI_INPUTREGS.name,self.registerAddress,
                                       self.numberOfRegs)'''
        elif self.commandType == ModbusCommand.READMULTI_HOLDINGREGS:
            value = self.modbus.readMultiHoldingRegValues(self.registerAddress, self.numberOfRegs)
            '''self.component.logger.info("thread sendModbusCommand()[%s]: Sent command %s, register=%d, numOfRegs=%d",
                                       str(self.pid),ModbusCommand.READMULTI_HOLDINGREGS.name,self.registerAddress,self.numberOfRegs)'''
        elif self.commandType == ModbusCommand.WRITE_HOLDINGREG:
            self.modbus.writeHoldingRegister(self.registerAddress, self.values[0], self.numberOfDecimals, self.signedValue)
            '''self.component.logger.info("thread sendModbusCommand()[%s]: Sent command %s, register=%d, value=%d, numberOfDecimals=%d, signed=%s",
                                       str(self.pid),ModbusCommand.WRITE_HOLDINGREG.name,self.registerAddress,self.values[0],self.numberOfDecimals,str(self.signedValue))'''
        elif self.commandType == ModbusCommand.WRITEMULTI_HOLDINGREGS:
            self.modbus.writeHoldingRegisters(self.registerAddress, self.values)
            '''self.component.logger.info("thread sendModbusCommand()[%s]: Sent command %s, register=%d",
                                       str(self.pid),ModbusCommand.WRITEMULTI_HOLDINGREGS.name,self.registerAddress)
            self.component.logger.info("thread sendModbusCommand()[%s]: Values - %s",
                                       str(self.pid),str(self.values).strip('[]'))'''
        else:
            self.component.logger.info("thread sendModbusCommand()[%s]: Invalid query command sent: command=%s",
                                       str(self.pid),self.commandtype.name)
        
        if debugMode:
            t1 = time.perf_counter()
            self.component.logger.debug("thread sendModbusCommand()[%s]: Modbus library command complete at %f, time to interact with Modbus library is %f ms",
                                        str(self.pid),t1,(t1-t0)*1000)

        return value
 

        def do_polling(self):
            if self.pollWriteCmd.commandType == ModbusCommand.NONE:
                self.component.logger.debug("thread run()[%s]: No polling write Modbus command available",str(self.pid))
            else:
                if debugMode:
                    self.cmdRxByThreadTime = time.perf_counter()
                    self.component.logger.debug("thread run()[%s]: Send polling write Modbus command at %f",
                                                str(self.pid), self.cmdRxByThreadTime)
                self.processModbusCommand(self.pollWriteCmd)

            if self.pollReadCmd.commandType == ModbusCommand.NONE:
                self.component.logger.debug("thread run()[%s]: No polling read Modbus command available",str(self.pid))
            else:
                if debugMode:
                    self.cmdRxByThreadTime = time.perf_counter()
                    self.component.logger.debug("thread run()[%s]: Send polling read Modbus command at %f",
                                                str(self.pid), self.cmdRxByThreadTime)
                self.processModbusCommand(self.pollReadCmd)

        
    def enableModbus(self):
        if debugMode:
            t0 = time.perf_counter()     
            self.component.logger.debug("thread enableModbus()[%s]: Request Modbus start at %f",str(self.pid),t0)

        self.modbus.startModbus()
        # pydevd.settrace(host='192.168.1.102',port=5678)
        self.modbusReady = True

        if debugMode:
            t1 = time.perf_counter()     
            self.component.logger.debug("thread enableModbus()[%s]: Modbus opened portname=%s, slaveaddress=%s ready at %f, time to start Modbus is %f ms",
                                        str(self.pid),self.component.port_config.portname,self.component.slaveAddressDecimal,
                                        t1,(t1-t0)*1000)


    def disableModbus(self):
        if debugMode:
            t0 = time.perf_counter()     
            self.component.logger.debug("thread disableModbus()[%s]: Request Modbus be disabled at %f",str(self.pid),t0)

        self.modbus.stopModbus()
        self.modbusReady = False

        if debugMode:
            t1 = time.perf_counter()     
            self.component.logger.debug("thread disableModbus()[%s]: Modbus closed portname=%s, slaveaddress=%s, disabled at %f, time to stop Modbus is %f ms",
                                        str(self.pid),self.component.port_config.portname,self.component.slaveAddressDecimal,
                                        t1,(t1-t0)*1000)


    def activate(self):
        self.active.set()


    def deactivate(self):
        self.active.clear()


    def terminate(self):
        self.terminated.set()

    
class ModbusUartPollDevice(Component):
    def __init__(self,slaveaddress=0,port="UART1",baudrate=19200,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,
                 stopbits=serial.STOPBITS_ONE,serialTimeout=0.05): # defaults for Modbus spec
        super().__init__()
        if debugMode:
            self.logger.setLevel(logging.DEBUG)
            self.logger.handlers[0].setLevel(logging.DEBUG) # a workaround for hardcoded INFO level of StreamHandler logger
        else:
            self.logger.setLevel(logging.INFO)
            
        self.pid = os.getpid()
        
        if port == 'UART1':
            self.port = '/dev/ttyO1'
        elif port == 'UART2':
            self.port = '/dev/ttyO2'
        elif port == 'UART3':
            self.port = '/dev/ttyO3'
        elif port == 'UART4':
            self.port = '/dev/ttyO4'
        elif port == 'UART5':
            self.port = '/dev/ttyO5'
        else:
            self.logger.error('__init__[%s]: Invalid UART argument, use UART1..5', self.pid)
            sys.exit(-1)
        
        self.port_config = PortConfig(self.port, baudrate, bytesize, parity, stopbits, serialTimeout)        
        self.slaveAddressDecimal = slaveaddress
        if debugMode:
            self.logger.info("__init__[%s]: Modbus settings %d @%s:%d %d%s%d",str(self.pid),self.slaveAddressDecimal,
                             self.port_config.portname,self.port_config.baudrate,self.port_config.bytesize,
                             self.port_config.parity,self.port_config.stopbits)

        self.cmds = queue.Queue()
        self.ModbusUartPollThread = None

    def on_clock(self):
        now = self.clock.recv_pyobj()  # Receive time (as float)
        if debugMode:
            self.logger.info("on_clock()[%s]: eventTime=%s", str(self.pid), now)
            t0 = time.perf_counter()
            self.logger.debug("on_clock()[%s]: functionStartTime=%f", str(self.pid), t0)

        if self.ModbusUartPollThread == None:
            self.ModbusUartPollThread = ModbusUartPollThread(self, self.cmds, self.data)  # data is an inside port
            self.ModbusUartPollThread.start()
            self.data.activate()

        self.clock.halt()

        if debugMode:
            t1 = time.perf_counter()
            self.logger.debug("on_clock()[%s]: functionStopTime=%f, timeInFunction=%f ms", str(self.pid), t1,
                              (t1 - t0) * 1000)

                    
    def __destroy__(self):
        self.logger.info("__destroy__[%s]",str(self.pid))
        if self.ModbusUartPollThread != None:
            self.ModbusUartPollThread.deactivate()
            self.ModbusUartPollThread.terminate()


    '''    
    Receive a Modbus command request and send to device thread using command queue. An 'ERROR' will be sent to the 
    requester if the device thread is not yet present.  If the Modbus does not start, the application will exit.  If a 
    device thread is available, an ACK will be sent back to the requester to let them know the command is being processed.
    '''
    def on_modbusRepPort(self):             
        commandRequest = self.modbusRepPort.recv_pyobj()    

        if debugMode:
            self.modbusReqRxTime = time.perf_counter()     
            self.logger.debug("on_modbusRepPort()[%s]: Request Received at %f",str(self.pid),self.modbusReqRxTime)

        if self.ModbusUartPollThread == None:
            self.logger.info("on_modbusRepPort()[%s]: ModbusUartThread not available yet, send ERROR msg",str(self.pid))
            msg = ('ERROR')
            self.modbusRepPort.send_pyobj(msg)
        else:  
            if debugMode:
                t0 = time.perf_counter()
                self.logger.debug("on_modbusRepPort()[%s]: Send command request=%s to Thread at %f",str(self.pid),
                                  commandRequest.requestType.name,t0)
     
            self.cmds.put(commandRequest)  # send using command queue to Modbus thread, results will come back on inside data plug

            if debugMode:
                self.sendAckTime = time.perf_counter()
                self.logger.debug("on_modbusRepPort()[%s]: Send ACK back to requester at %f, time from request to ACK back is %f ms",
                                  str(self.pid), self.sendAckTime,
                                  (self.sendAckTime - self.modbusReqRxTime) * 1000)
            msg = ('ACK')
            self.modbusRepPort.send_pyobj(msg)


    def on_data(self):
        msg = self.data.recv_pyobj()
        
        if debugMode:
            self.dataRxFromThreadTime = time.perf_counter()     
            self.logger.debug("on_data()[%s]: Data=%s received from internal device thread at %f",
                              str(self.pid),msg,self.dataRxFromThreadTime)
        
        self.modbusDataPub.send_pyobj(msg)  # publish results for calling component to subscribe


        
  