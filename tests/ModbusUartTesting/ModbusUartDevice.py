'''
Created on Mar 14, 2017

@author: riaps

<--------- MM TODO:  rewrite ----------->
The device will read or write bits, input registers, or holding registers (one or many).
Polling can be configured to read or write any of these registers.  When the user first
commands a register (to read or write), they indicate if the register set should be included 
in the polling activity.  A list of pollingRequested register sets will be available when 
polling is requested to start.  A polling thread will be started and it will run the 
commands listed at the period indicated when the polling was started.  Polling
will continue until a stop polling command is issued.  Since multiple register sets can be 
identified in the list to be polled, the user must make sure that the timeline desired takes
into account the time needed to completion the list of commands to be polled.  Otherwise, the 
commands are executed and then the requested sleep period occur.   

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
    - requestType = START_POLLING --> requestData = polling frequency in ms
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
        self.component.logger.info("ModbusUartThread [%s]: init",self.pid)

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
                    self.component.logger.info("ModbusUartThread[%s]: Thread receives request=%s, data=%s",str(self.pid),requestType.name,requestData)
                    
                    # Acknowledge receipt of a command request
                    msg = ('ACK')
                    self.plug.send_pyobj(msg)

                    # Single Modbus Query
                    if requestType == ModbusRequest.QUERY_MODBUS:
                        self.unpackRegisterCommand(requestData)
                        self.component.logger.info("ModbusUartThread[%s]: Sending Query Cmd to Modbus",str(self.pid)) 
                        responseValue = self.sendModbusCommand()    
                        self.component.logger.info("ModbusUartThread[%s]: responseValue=%s",str(self.pid),responseValue)

                        # Publish Modbus read results (999 sent if a write was performed - see sendModbusCommand return value)
                        self.dataPlug.send_pyobj(responseValue)
                        # pydevd.settrace(host='192.168.1.102',port=5678)   
                        
                    # MM TODO:  stopped here to test query first    
                    # Setup a list of Modbus commands to query during polling
                    elif requestType == ModbusRequest.SETUP_POLLER:
                        self.component.logger.info("ModbusUartThread[%s]: Poller Setup requested",str(self.pid))   
                    
                    # MM TODO:  stopped here to test query first   
                    # Start Polling
                    elif requestType == ModbusRequest.START_POLLING:
                        self.component.logger.info("ModbusUartThread[%s]: Poller Start requested",str(self.pid))   
                    
                    # MM TODO:  stopped here to test query first   
                    # Stop Polling
                    elif requestType == ModbusRequest.STOP_POLLING:
                        self.pollingActive = False
                        self.pollerTimeout = None
                        self.component.logger.info("ModbusUartThread[%s]: Poller Stop requested",str(self.pid))   
                    
                # MM TODO:  stopped here to test query first   
                # In polling mode
                if self.pollingActive == True:
                    self.component.logger.info("ModbusUartThread[%s]: Polling Active",str(self.pid))
                    
         
    def unpackRegisterCommand(self,rxCommandData):
        self.commandType = rxCommandData.commandType
        self.registerAddress = rxCommandData.registerAddress
        self.numberOfRegs = rxCommandData.numberOfRegs
        self.numberOfDecimals = rxCommandData.numberOfDecimals
        self.signedValue = rxCommandData.signedValue
        self.values = rxCommandData.values
        
    def sendModbusCommand(self):
        value = 999  # large invalid value
        
        if self.commandType == ModbusCommands.READ_INPUTREG:
            value = self.modbus.readInputRegValue(self.registerAddress, self.numberOfDecimals, self.signedValue)
            self.component.logger.info("ModbusUartThread: sent command %s, register=%d, numOfDecimals=%d, signed=%s", ModbusCommands.READ_INPUTREG.name,self.registerAddress,self.numberOfDecimals,str(self.signedValue))
        elif self.commandType == ModbusCommands.READ_HOLDINGREG:
            value = self.modbus.readHoldingRegValue(self.registerAddress, self.numberOfDecimals, self.signedValue)
            self.component.logger.info("ModbusUartThread: sent command %s, register=%d, numOfDecimals=%d, signed=%s", ModbusCommands.READ_HOLDINGREG.name,self.registerAddress,self.numberOfDecimals,str(self.signedValue))
        elif self.commandType == ModbusCommands.READMULTI_INPUTREGS:
            value = self.modbus.readMultiInputRegValues(self.registerAddress, self.numberOfRegs)
            self.component.logger.info("ModbusUartThread: sent command %s, register=%d, numOfRegs=%d", ModbusCommands.READMULTI_INPUTREGS.name,self.registerAddress,self.numberOfRegs)
        elif self.commandType == ModbusCommands.READMULTI_HOLDINGREGS:
            value = self.modbus.readMultiHoldingRegValues(self.registerAddress, self.numberOfRegs)
            self.component.logger.info("ModbusUartThread: sent command %s, register=%d, numOfRegs=%d", ModbusCommands.READMULTI_HOLDINGREGS.name,self.registerAddress,self.numberOfRegs)
        elif self.commandType == ModbusCommands.WRITE_HOLDINGREG:
            self.modbus.writeHoldingRegister(self.registerAddress, self.values[0], self.numberOfDecimals, self.signedValue)
            self.component.logger.info("ModbusUartThread: sent command %s, register=%d, value=%d, numberOfDecimals=%d, signed=%s",ModbusCommands.WRITE_HOLDINGREG.name,self.registerAddress,self.values[0],self.numberOfDecimals,str(self.signedValue))
        elif self.commandType == ModbusCommands.WRITEMULTI_HOLDINGREGS:
            self.modbus.writeHoldingRegisters(self.registerAddress, self.values)
            self.component.logger.info("ModbusUartThread: sent command %s, register=%d",ModbusCommands.WRITEMULTI_HOLDINGREGS.name,self.registerAddress)
            self.component.logger.info("ModbusUartThread: Values - %s", str(self.values).strip('[]'))   
        else: # MM TODO:  invalid query command
            self.component.logger.info("ModbusUartThread: Invalid query command sent: command=%s",self.commandtype.name)  
        
        return value
        
    ''' 
    Start a thread that will read the appropriate registers in the pollCmdList and then sleep for the period specified
    '''
    # MM TODO:  stopped here to test query first
    def startPolling(self):
        self.pollingActive = True
        self.component.logger.info("ModbusUartThread[%s]: Polling started",str(self.pid))

    # MM TODO:  stopped here to test query first
    def stopPolling(self):
        if self.pollingActive:
            self.pollingActive = False
        self.component.logger.info("ModbusUartThread[%s]: Polling stopped",str(self.pid))

    def enableModbus(self):
        self.modbus.startModbus()
        # pydevd.settrace(host='192.168.1.102',port=5678)
        self.modbusReady = True
        self.component.logger.info('ModbusUartThread: Modbus opened portname=%s, slaveaddress=%s',self.component.port_config.portname,self.component.slaveAddressDecimal)

    def disableModbus(self):
        self.modbus.stopModbus()
        self.modbusReady = False
        self.component.logger.info('ModbusUartThread: Modbus closed portname=%s, slaveaddress=%s',self.component.port_config.portname,self.component.slaveAddressDecimal)
        
    def activate(self):
        self.active.set()

    def deactivate(self):
        self.active.clear()

    def terminate(self):
        self.terminated.set()

    
class ModbusUartDevice(Component):
    def __init__(self,slaveaddress=0,port="UART1",baudrate=19200,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,serialTimeout=0.05): # defaults for Modbus spec
        super().__init__()
        self.logger.setLevel(logging.DEBUG)
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
            self.component.logger.error('ModbusUartDevice [%s]: Invalid UART argument, use UART1..5', self.pid)
            sys.exit(-1)
        
        self.port_config = PortConfig(self.port, baudrate, bytesize, parity, stopbits, serialTimeout)        
        self.slaveAddressDecimal = slaveaddress
        self.logger.info("ModbusUartDevice[%s]: Modbus settings %d @%s:%d %d%s%d [%d]",str(self.pid),self.slaveAddressDecimal,self.port_config.portname,self.port_config.baudrate,self.port_config.bytesize,self.port_config.parity,self.port_config.stopbits,self.pid)       
        self.ModbusUartThread = None
        

    def on_clock(self):
        now = self.clock.recv_pyobj()   # Receive time (as float)
        self.logger.info("ModbusUartDevice - on_clock()[%s]: %s",str(self.pid),now)        
        
        if self.ModbusUartThread == None:
            self.ModbusUartThread = ModbusUartThread(self,self.command,self.data)
            self.ModbusUartThread.start()
            self.command.activate()
            self.data.activate()

        self.clock.halt()
                    
    def __destroy__(self):
        self.logger.info("ModbusUartDevice[%s]: __destroy__",str(self.pid))
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

        if self.ModbusUartThread == None:
            self.logger.info("ModbusUartDevice - on_modbusRepPort()[%s]: ModbusUartThread not available yet",str(self.pid))
            msg = ('ERROR')
            self.modbusRepPort.send_pyobj(msg)
        else:  
            self.logger.info("ModbusUartDevice - on_modbusRepPort()[%s]: request=%s",str(self.pid),commandRequest.requestType.name) 
            self.command.send_pyobj(commandRequest)  # send inside command to Modbus thread, results will come back on inside data plug 
                        
    def on_data(self):
        msg = self.data.recv_pyobj()
        self.modbusDataPub.send_pyobj(msg)  # publish results for calling component to subscribe
        self.logger.info("ModbusUartDevice - on_data[%s]: Publishing Data, msg=%s",str(self.pid),msg)

    ''' 
    Receive an 'ACK' from ModbusDeviceThread when command is received and send reply back to requester
    '''
    def on_command(self):
        msg = self.command.recv_pyobj()
        self.logger.info("ModbusUartDevice - on_command[%s]: Receive ACK from device thread, msg=%s",str(self.pid),msg)
        self.modbusRepPort.send_pyobj(msg)      
                                     

        
  