'''
Created on Mar 14, 2017
Modified in November 2017

@author: riaps

The device will read or write bits, input registers, or holding registers (one or many).
When a command to read or write is received (QUERY_MODBUS) by the request port (on_modbusRepPort),
a command is sent to the inner device thread to request communication with the serial
Modbus using the serialModbusLib.  If the Modbus is ready, the requester will receive an 
'ACK' message to indicate the request has been accepted and the Modbus is available.
If the Modbus is not available, the requester will receive a 'ERROR' message.

In addition to direct queries to read/write registers, polling can be configured to read 
or write any grouping of these registers (multiple commands).  The 'SETUP_POLLER' command
is used to pass a list of Modbus commands (same available in QUERY_MODBUS) that will be 
executed when polling begins.  The requester would then start the polling ('START_POLLING) 
and provide a polling period desired.  A polling thread will be started and it will run the 
commands listed at the periodicity indicated when the polling was started.  When desired, 
the requester can stop polling by sending a 'STOP_POLLING' command.

Application Developer Note: When developing an application that intends to poll for a value 
or periodically write a specific value, carefully consider the system timeline of the 
application activity to make sure the desired Modbus interaction can happen during the 
specified polling periodicity.  Each Modbus command within the inner thread will take 
around 7 ms physically interact with the Modbus.

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
import zmq
from serialModbusLib.serialModbusComm import SerialModbusComm,PortConfig
from collections import namedtuple
from enum import Enum
#import pydevd

''' Enable debugging to gather timing information on the code execution'''
debugMode = True


''' Requester Commands Available'''
class ModbusRequest(Enum):
    NONE          = 0  
    QUERY_MODBUS  = 1  # Single Modbus Query 
    SETUP_POLLER  = 2  # Setup a list of Modbus commands to query during polling
    START_POLLING = 3  
    STOP_POLLING  = 4
    
class ModbusCommands(Enum):
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
    - requestType = QUERY_MODBUS  --> requestData = CommandFormat() data
    - requestType = SETUP_POLLER  --> requestData = list of CommandFormat() data
    - requestType = START_POLLING --> requestData = polling periodicity in ms
    - requestType = STOP_POLLING  --> requestData = N/A

    Note: the application user should consider system timing when determining the polling 
          frequency and list of Modbus commands to query during a polling session in order 
          to make sure that all commands can be executed within the polling frequency.
'''
RequestFormat = namedtuple('RequestFormat', ['requestType','requestData'])

''' 
This configures the register sets that the application is interested in reading/writing.  
'''
CommandFormat = namedtuple('CommandFormat', ['commandType','registerAddress','numberOfRegs','values','numberOfDecimals','signedValue'])


'''
This thread will be the interface between the minimalmodbus library communication with the 
hardware and the RIAPS ModbusUartDevice component.  It will run all modbus queries, single 
command or polling operations.

ModbusRequests will be passed from the ModbusUartDevice component to this thread using the command inside port.
Queries will be executed by calling into the minimalmodbus library with a blocking call, 
then data will be published out the data inside port.  

Polling is first setup by providing a list of modbus queries to execute.  Polling begins when 
a request to start poll is received through the command inside port, along with the polling frequency 
desired (in ms).  Polling will continue until a stop polling is received. 

Since multiple modbus queries can be setup for each polling period, the timeout between queries will be
calculated based on the sampling frequency requested and the length of time it took to execute the list 
of modbus queries.
'''
class ModbusUartThread(threading.Thread):
    def __init__(self, component, command, data):
        threading.Thread.__init__(self)
        self.terminated = threading.Event()
        self.active = threading.Event()
        
        self.component = component
        self.command = command
        self.data = data
        self.pid = os.getpid()
        self.modbusReady = False
        self.modbus = SerialModbusComm(self,self.component.slaveAddressDecimal,self.component.port_config)
        self.pollingActive = False
        self.pollerTimeout = None
        self.pollCmdList = []
        self.pollPeriod = 0     # units are ms
        self.component.logger.info("thread __init__ [%s]: init thread",self.pid)

    def run(self):
        self.plug = self.command.setupPlug(self)
        self.dataPlug = self.data.setupPlug(self)
        self.poller = zmq.Poller()
        self.poller.register(self.plug, zmq.POLLIN)
        if self.terminated.is_set(): 
            return
        
        if self.modbusReady == False:
            self.enableModbus()
                        
        while True:
            self.active.wait(None)
            if self.terminated.is_set():
                self.disableModbus()
                break
            if self.active.is_set():
                socks = dict(self.poller.poll(timeout = self.pollerTimeout))
                if self.plug in socks and socks[self.plug] == zmq.POLLIN:
                    requestType, requestData = self.plug.recv_pyobj()                    
                    self.component.logger.info("thread run()[%s]: Thread receives a command request=%s, data=%s",str(self.pid),requestType.name,requestData)
                    
                    if debugMode:
                        self.cmdRxByThreadTime = time.perf_counter()     
                        self.component.logger.debug("thread run()[%s]: Received requested Modbus command at %f",str(self.pid),self.cmdRxByThreadTime)
                                        
                    # Acknowledge receipt of a command request
                    msg = ('ACK')
                    self.plug.send_pyobj(msg)
                    self.component.logger.info("thread run()[%s]: Sending ACK back to ModbusUartDevice",str(self.pid))
                    
                    if debugMode:
                        self.ackTxByThreadTime = time.perf_counter()
                        self.component.logger.debug("thread run()[%s]: Sent ACK back at %f, time from cmd to ACK send is %f ms",str(self.pid),self.ackTxByThreadTime,(self.ackTxByThreadTime-self.cmdRxByThreadTime)*1000)

                    # Single Modbus Query
                    if requestType == ModbusRequest.QUERY_MODBUS:
                        self.unpackRegisterCommand(requestData)
                        self.component.logger.info("thread run()[%s]: Sending Query Cmd to Modbus",str(self.pid))                        
                        responseValue = self.sendModbusCommand()    
                        self.component.logger.info("thread run()[%s]: responseValue=%s",str(self.pid),responseValue)

                        if debugMode:
                            self.dataRxModbusTime = time.perf_counter()     
                            self.component.logger.debug("thread run()[%s]: Sending data back to ModbusUartDevice at %f, time from cmd to data sent is %f ms",str(self.pid),self.dataRxModbusTime,(self.dataRxModbusTime-self.cmdRxByThreadTime)*1000)
                        
                        # Publish Modbus read results (999 sent if a write was performed - see sendModbusCommand return value)
                        self.dataPlug.send_pyobj(responseValue)
                        self.component.logger.info("thread run()[%s]: Sending data back to ModbusUartDevice",str(self.pid))
                        # pydevd.settrace(host='192.168.1.102',port=5678)   
                           
                    # Setup a list of Modbus commands to query during polling
                    elif requestType == ModbusRequest.SETUP_POLLER:
                        self.component.logger.info("thread run()[%s]: Poller Setup requested",str(self.pid))  
                        # MM TODO:  figure out how to pass this list and reinstate it.
                        
                    
                    # MM TODO:  stopped here to test query first   
                    # Start Polling
                    elif requestType == ModbusRequest.START_POLLING:
                        self.component.logger.info("thread run()[%s]: Poller Start requested",str(self.pid))  
                        self.startPolling(requestData) 
                    
                    # MM TODO:  stopped here to test query first   
                    # Stop Polling
                    elif requestType == ModbusRequest.STOP_POLLING:
                        self.component.logger.info("thread run()[%s]: Poller Stop requested",str(self.pid)) 
                        self.stopPolling()
                    
                # MM TODO:  stopped here to test query first   
                # In polling mode
                elif self.pollingActive == True:  # MM TODO:  is this an if or elif?
                    self.component.logger.info("thread run()[%s]: Polling Active",str(self.pid))
                    
                    if debugMode:
                        self.pollPeriodStartTime = time.perf_counter()     
                        self.component.logger.debug("thread run()[%s]: Poller timeout reached, begin Poll period at %f",str(self.pid),self.pollPeriodStartTime)
                        
                    '''   MM TODO:  still considering best way to do this                 
                    for cmd in self.pollCmdList:
                        self.unpackRegisterCommand(requestData)
                        self.component.logger.info("thread run()[%s]: Sending Polling Cmd to Modbus",str(self.pid))                        
                        responseValue = self.sendModbusCommand()    
                        self.component.logger.info("thread run()[%s]: responseValue=%s",str(self.pid),responseValue)

                        # Publish Modbus read results (999 sent if a write was performed - see sendModbusCommand return value)
                        self.dataPlug.send_pyobj(responseValue)
                        self.component.logger.info("thread run()[%s]: Sending data back to ModbusUartDevice",str(self.pid))
                        # pydevd.settrace(host='192.168.1.102',port=5678)   
                        
                        self.pollExecTime = time.perf_counter() 

                        # MM TODO:  calculate new timeout value - open questions:
                        # 1) How do I determine current timeout value in poller?
                        # 2) How do this get instantiated so the poller uses the new time?
                        if debugMode:
                            self.component.logger.debug("thread run()[%s]: Poll activity finished at %f, time spent polling command list is %f ms",str(self.pid),self.pollExecTime,(self.pollExecTime-self.pollPeriodStartTime)*1000)
                    '''
                    # MM TODO:  do polling, calculate new timeout period, print out new timeout and debug time of completion

                    
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
            self.component.logger.debug("thread sendModbusCommand()[%s]: Sending command to Modbus library at %f",str(self.pid),t0)

        value = 999  # large invalid value
        
        if self.commandType == ModbusCommands.READ_INPUTREG:
            value = self.modbus.readInputRegValue(self.registerAddress, self.numberOfDecimals, self.signedValue)
            self.component.logger.info("thread sendModbusCommand()[%s]: sent command %s, register=%d, numOfDecimals=%d, signed=%s",str(self.pid),ModbusCommands.READ_INPUTREG.name,self.registerAddress,self.numberOfDecimals,str(self.signedValue))
        elif self.commandType == ModbusCommands.READ_HOLDINGREG:
            value = self.modbus.readHoldingRegValue(self.registerAddress, self.numberOfDecimals, self.signedValue)
            self.component.logger.info("thread sendModbusCommand()[%s]: sent command %s, register=%d, numOfDecimals=%d, signed=%s",str(self.pid),ModbusCommands.READ_HOLDINGREG.name,self.registerAddress,self.numberOfDecimals,str(self.signedValue))
        elif self.commandType == ModbusCommands.READMULTI_INPUTREGS:
            value = self.modbus.readMultiInputRegValues(self.registerAddress, self.numberOfRegs)
            self.component.logger.info("thread sendModbusCommand()[%s]: sent command %s, register=%d, numOfRegs=%d",str(self.pid),ModbusCommands.READMULTI_INPUTREGS.name,self.registerAddress,self.numberOfRegs)
        elif self.commandType == ModbusCommands.READMULTI_HOLDINGREGS:
            value = self.modbus.readMultiHoldingRegValues(self.registerAddress, self.numberOfRegs)
            self.component.logger.info("thread sendModbusCommand()[%s]: sent command %s, register=%d, numOfRegs=%d",str(self.pid),ModbusCommands.READMULTI_HOLDINGREGS.name,self.registerAddress,self.numberOfRegs)
        elif self.commandType == ModbusCommands.WRITE_HOLDINGREG:
            self.modbus.writeHoldingRegister(self.registerAddress, self.values[0], self.numberOfDecimals, self.signedValue)
            self.component.logger.info("thread sendModbusCommand()[%s]: sent command %s, register=%d, value=%d, numberOfDecimals=%d, signed=%s",str(self.pid),ModbusCommands.WRITE_HOLDINGREG.name,self.registerAddress,self.values[0],self.numberOfDecimals,str(self.signedValue))
        elif self.commandType == ModbusCommands.WRITEMULTI_HOLDINGREGS:
            self.modbus.writeHoldingRegisters(self.registerAddress, self.values)
            self.component.logger.info("thread sendModbusCommand()[%s]: sent command %s, register=%d",str(self.pid),ModbusCommands.WRITEMULTI_HOLDINGREGS.name,self.registerAddress)
            self.component.logger.info("thread sendModbusCommand()[%s]: Values - %s",str(self.pid),str(self.values).strip('[]'))   
        else: # MM TODO:  invalid query command
            self.component.logger.info("thread sendModbusCommand()[%s]: Invalid query command sent: command=%s",str(self.pid),self.commandtype.name)  
        
        if debugMode:
            t1 = time.perf_counter()
            self.component.logger.debug("thread sendModbusCommand()[%s]: Modbus library command complete at %f, time to interact with Modbus library is %f ms",str(self.pid),t1,(t1-t0)*1000)

        return value
 
        
    ''' 
    Start a thread that will read the appropriate registers in the pollCmdList and then 
    sleep for the period specified. Start command includes the periodicity of the polled 
    command set (list).
    '''
    # MM TODO:  stopped here to test query first
    def startPolling(self, period):
        if debugMode:
            t0 = time.perf_counter()     
            self.component.logger.debug("thread startPolling()[%s]: Start polling requested at %f",str(self.pid),t0)

        self.pollingActive = True
        self.component.logger.info("thread startPolling()[%s]: Polling started",str(self.pid))
        self.pollPeriod = period
        self.pollerTimeout = self.pollPeriod


    def stopPolling(self):
        if debugMode:
            t0 = time.perf_counter()     
            self.component.logger.debug("thread stopPolling()[%s]: Stop polling requested at %f",str(self.pid),t0)  

        if self.pollingActive:
            self.pollingActive = False
            self.pollerTimeout = None
            
        self.component.logger.info("thread stopPolling[%s]: Polling stopped",str(self.pid))
        
        
    def enableModbus(self):
        if debugMode:
            t0 = time.perf_counter()     
            self.component.logger.debug("thread enableModbus()[%s]: Request Modbus start at %f",str(self.pid),t0)

        self.modbus.startModbus()
        # pydevd.settrace(host='192.168.1.102',port=5678)
        self.modbusReady = True
        self.component.logger.info("thread enableModbus()[%s]: Modbus opened portname=%s, slaveaddress=%s",str(self.pid),self.component.port_config.portname,self.component.slaveAddressDecimal)
        
        if debugMode:
            t1 = time.perf_counter()     
            self.component.logger.debug("thread enableModbus()[%s]: Modbus ready at %f, time to start Modbus is %f ms",str(self.pid),t1,(t1-t0)*1000)


    def disableModbus(self):
        if debugMode:
            t0 = time.perf_counter()     
            self.component.logger.debug("thread disableModbus()[%s]: Request Modbus be disabled at %f",str(self.pid),t0)

        self.modbus.stopModbus()
        self.modbusReady = False
        self.component.logger.info("thread disableModbus()[%s]: Modbus closed portname=%s, slaveaddress=%s",str(self.pid),self.component.port_config.portname,self.component.slaveAddressDecimal)
        
        if debugMode:
            t1 = time.perf_counter()     
            self.component.logger.debug("thread disableModbus()[%s]: Modbus disabled at %f, time to stop Modbus is %f ms",str(self.pid),t1,(t1-t0)*1000)


    def activate(self):
        self.active.set()


    def deactivate(self):
        self.active.clear()


    def terminate(self):
        self.terminated.set()

    
class ModbusUartDevice(Component):
    def __init__(self,slaveaddress=0,port="UART1",baudrate=19200,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,serialTimeout=0.05): # defaults for Modbus spec
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
        self.logger.info("__init__[%s]: Modbus settings %d @%s:%d %d%s%d",str(self.pid),self.slaveAddressDecimal,self.port_config.portname,self.port_config.baudrate,self.port_config.bytesize,self.port_config.parity,self.port_config.stopbits)       
        self.ModbusUartThread = None
        

    def on_clock(self):
        now = self.clock.recv_pyobj()   # Receive time (as float)
        self.logger.info("on_clock()[%s]: eventTime=%s",str(self.pid),now)    
        
        if debugMode:
            t0 = time.perf_counter()     
            self.logger.debug("on_clock()[%s]: functionStartTime=%f",str(self.pid),t0)
        
        if self.ModbusUartThread == None:
            self.ModbusUartThread = ModbusUartThread(self,self.command,self.data)
            self.ModbusUartThread.start()
            self.command.activate()
            self.data.activate()

        self.clock.halt()
        
        if debugMode:
            t1 = time.perf_counter()
            self.logger.debug("on_clock()[%s]: functionStopTime=%f, timeInFunction=%f ms",str(self.pid),t1,(t1-t0)*1000)
                    
    def __destroy__(self):
        self.logger.info("__destroy__[%s]: __destroy__",str(self.pid))
        if self.ModbusUartThread != None:
            self.ModbusUartThread.deactivate()
            self.ModbusUartThread.terminate()
    
    '''    
    Receive a Modbus command request and send to device thread on inside command port.
    Once device thread receives the command, an ACK will be sent back to the requester from the on_command function. 
    An 'ERROR' will be sent to the requester if the device thread is not yet present.
    '''
    def on_modbusRepPort(self):             
        commandRequest = self.modbusRepPort.recv_pyobj()    

        if debugMode:
            self.modbusReqRxTime = time.perf_counter()     
            self.logger.debug("on_modbusRepPort()[%s]: Request Received at %f",str(self.pid),self.modbusReqRxTime)

        if self.ModbusUartThread == None:
            self.logger.info("on_modbusRepPort()[%s]: ModbusUartThread not available yet, send ERROR msg",str(self.pid))
            msg = ('ERROR')
            self.modbusRepPort.send_pyobj(msg)
        else:  
            if debugMode:
                t1 = time.perf_counter()
                self.logger.debug("on_modbusRepPort()[%s]: Send command to Thread at %f",str(self.pid),t1)
     
            self.logger.info("on_modbusRepPort()[%s]: request=%s, sending command to device thread",str(self.pid),commandRequest.requestType.name) 
            self.command.send_pyobj(commandRequest)  # send inside command to Modbus thread, results will come back on inside data plug 
            
                        
    def on_data(self):
        msg = self.data.recv_pyobj()
        
        if debugMode:
            self.dataRxFromThreadTime = time.perf_counter()     
            self.logger.debug("on_data()[%s]: Data received from internal device thread at %f, time from request to data is %f ms",str(self.pid),self.dataRxFromThreadTime,(self.dataRxFromThreadTime-self.modbusReqRxTime)*1000)
        
        self.modbusDataPub.send_pyobj(msg)  # publish results for calling component to subscribe
        self.logger.info("on_data[%s]: Publishing Data, msg=%s",str(self.pid),msg)

    ''' 
    Receive an 'ACK' from ModbusDeviceThread when command is received and send reply back to requester
    '''
    def on_command(self):
        msg = self.command.recv_pyobj()
        
        if debugMode:
            self.cmdAckRxFromThreadTime = time.perf_counter()     
            self.logger.debug("on_command()[%s]: Command ACK received from internal device thread at %f, time to get ACK back is %f ms",str(self.pid),self.cmdAckRxFromThreadTime,(self.cmdAckRxFromThreadTime-self.modbusReqRxTime)*1000)

        self.logger.info("on_command[%s]: Receive ACK from device thread, sending ACK to requester, msg=%s",str(self.pid),msg)
        self.modbusRepPort.send_pyobj(msg)      
                                     

        
  