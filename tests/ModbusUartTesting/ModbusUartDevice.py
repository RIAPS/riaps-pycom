'''
Created on Mar 14, 2017

@author: riaps

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
import serial
from serialModbusLib.serialModbusComm import SerialModbusComm,PortConfig
from collections import namedtuple
from enum import Enum
#import pydevd


class ModbusCommands(Enum):
    NONE = 0
    READ_BIT = 1
    READ_INPUTREG = 2
    READ_HOLDINGREG = 3
    READMULTI_INPUTREGS = 4
    READMULTI_HOLDINGREGS = 5
    WRITE_BIT = 6
    WRITE_HOLDINGREG = 7
    WRITEMULTI_HOLDINGREGS = 8
    START_POLLING = 9
    STOP_POLLING = 10
    
# Modbus Command can be either read/write a bit/registers or it could be a request to start/stop polling of bit/registers.  
# The commands types possible are identified in the ModbusCommands enum.
CommandFormat = namedtuple('CommandFormat', ['commandType','commandData'])

# This configures the register sets with which the application is interested in reading/writing together.  
# Each register set configured with a 'pollingRequested = true' will be added to a list of polling commands that will be sent to the Modbus sequentially once the polling has been started.
# The component developer needs to make sure that the desired register set can be read or written within the period specified by the polling configuration, otherwise data may become lost or a later command not sent.
RegisterConfig = namedtuple('RegisterConfig', ['registerAddress','numberOfRegs','values','numberOfDecimals','signedValue', 'pollRequested'])

# The polling sleep period indicates how long the polling thread will sleep after executing the polling register set of commands.  This value is specified in ms.
PollConfig = namedtuple('PollConfig',['sleepPeriod'])

class ModbusUartPollingThread(threading.Thread):
    def __init__(self, component):
        threading.Thread.__init__(self)
        self.active = threading.Event()
        self.active.clear()
        self.waiting = threading.Event()
        self.terminated = threading.Event()
        self.terminated.clear()
        self.component = component

    def run(self):
        self.data_plug = self.component.data_queue.setupPlug(self)

        while True:
            if self.terminated.is_set():
                break
# MM TODO:  need to update the thread code - this is from the C37 work
# want to periodically send a command to modbus
            if not self.active.is_set():
                if self.pdc.is_connected():
                    self.pdc.stop()
                    self.active.wait()
                    self.pdc.start()
                else:
                    self.active.wait()

            if self.pdc.is_connected():
                data = self.pdc.get()
                self.data_plug.send_pyobj(data)

            else:
                self.pdc.run()
                if self.pdc.is_connected():
                    header = self.pdc.get_header()
                    self.header_plug.send_pyobj(header)
                    config = self.pdc.get_config()
                    self.config_plug.send_pyobj(config)
                    self.pdc.start()
                else:
                    # TODO: wait some?
                    pass


        self.pdc.quit()

    def activate(self):
        self.active.set()

    def deactivate(self):
        self.active.clear()

    def terminate(self):
        self.terminated.set()

    
class ModbusUartDevice(Component):
    def __init__(self,slaveaddress=0,port="ttyO1",baudrate=19200,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,serialTimeout=0.05): # defaults for Modbus spec
        super().__init__()
        self.logger.setLevel(logging.DEBUG)
        self.pid = os.getpid()
        self.port_config = PortConfig("/dev/" + port, baudrate, bytesize, parity, stopbits, serialTimeout)        
        self.slaveAddressDecimal = slaveaddress
        self.modbus = SerialModbusComm(self,self.slaveAddressDecimal,self.port_config)
        self.modbusReady = False
        self.pollCmdList = []
        self.pollingEnabled = False
        self.sleepPeriod = 0
        self.logger.info("Modbus settings %d @%s:%d %d%s%d [%d]", self.slaveAddressDecimal,self.port_config.portname,self.port_config.baudrate,self.port_config.bytesize,self.port_config.parity,self.port_config.stopbits,self.pid)       
        self.ModbusUartPollingThread = None

    def on_clock(self):
        now = self.clock.recv_pyobj()   # Receive time (as float)
        self.logger.info("on_clock()[%s]: %s",str(self.pid),now)        
        
        if self.modbusReady == False:
            self.modbus.startModbus()
#            pydevd.settrace(host='192.168.1.102',port=5678)
            self.modbusReady = True
            
            # Stop clock once Modbus is running
            self.clock.halt()
                    
    def __destroy__(self):
        self.logger.info("__destroy__")
        self.modbus.stopModbus()
        
        if self.ModbusUartPollingThread != None:
            self.ModbusUartPollingThread.deactivate()
            self.ModbusUartPollingThread.terminate()
   
    '''    
    Receive a Modbus command request.  Process command and send back response.
    '''
    def on_modbusRepPort(self):                
        '''Request Received'''         
        commandRequest = self.modbusRepPort.recv_pyobj()     
        self.logger.info("on_modbusRepPort()[%s]: %s",str(self.pid),commandRequest) 

        self.commandRequested = commandRequest.commandType

        if self.commandRequested == ModbusCommands.START_POLLING or self.commandRequested == ModbusCommands.STOP_POLLING
            self.unpackPollCommand(commandRequest.commandData)
        else
            self.unpackRegisterCommand(commandRequest.commandData)
            # if command has 'pollRequest=True', save the command in the polling command list which is used when polling is started
            if self.pollRequested
                self.pollCmdList.append(commandRequest)  # MM TODO:  should I check if the command is already in the list?
                self.logger.info("on_modbusReqPort()[%s]: Added command to pollCmdList - %s",str(self.pid),commandRequest)
        
        responseValue = -1  # invalid response 
        if self.modbusReady == True:
            responseValue = self.sendModbusCommand()
            
            '''Send Results'''
            self.modbusRepPort.send_pyobj(responseValue)
#           pydevd.settrace(host='192.168.1.102',port=5678)
            self.logger.info("on_modbusRepPort()[%s]: %s,",str(self.pid),responseValue)        
            
                    
    def unpackRegisterCommand(self,rxCommandData):
        self.registerAddress = rxCommandData.registerAddress
        self.numberOfRegs = rxCommandData.numberOfRegs
        self.numberOfDecimals = rxCommandData.numberOfDecimals
        self.signedValue = rxCommandData.signedValue
        self.values = rxCommandData.values
        self.pollRequested = rxCommandData.pollRequested
        
    def unpackPollCommand(self,rxCommandData):
        self.sleepPeriod = rxCommandData.sleepPeriod

    def sendModbusCommand(self):
        value = 999  # large invalid value
        
        if self.commmandRequested == ModbusCommands.READ_INPUTREG:
            value = self.modbus.readInputRegValue(self.registerAddress, self.numberOfDecimals, self.signedValue)
            self.logger.info("ModbusUartDevice: sent command %s, register=%d, numOfDecimals=%d, signed=%s", ModbusCommands.READ_INPUTREG.name,self.registerAddress,self.numberOfDecimals,str(self.signedValue))
        elif self.commmandRequested == ModbusCommands.READ_HOLDINGREG:
            value = self.modbus.readHoldingRegValue(self.registerAddress, self.numberOfDecimals, self.signedValue)
            self.logger.info("ModbusUartDevice: sent command %s, register=%d, numOfDecimals=%d, signed=%s", ModbusCommands.READ_HOLDINGREG.name,self.registerAddress,self.numberOfDecimals,str(self.signedValue))
        elif self.commmandRequested == ModbusCommands.READMULTI_INPUTREGS:
            value = self.modbus.readMultiInputRegValues(self.registerAddress, self.numberOfRegs)
            self.logger.info("ModbusUartDevice: sent command %s, register=%d, numOfRegs=%d", ModbusCommands.READMULTI_INPUTREGS.name,self.registerAddress,self.numberOfRegs)
        elif self.commmandRequested == ModbusCommands.READMULTI_HOLDINGREGS:
            value = self.modbus.readMultiHoldingRegValues(self.registerAddress, self.numberOfRegs)
            self.logger.info("ModbusUartDevice: sent command %s, register=%d, numOfRegs=%d", ModbusCommands.READMULTI_HOLDINGREGS.name,self.registerAddress,self.numberOfRegs)
        elif self.commmandRequested == ModbusCommands.WRITE_HOLDINGREG:
            self.modbus.writeHoldingRegister(self.registerAddress, self.values[0], self.numberOfDecimals, self.signedValue)
            self.logger.info("ModbusUartDevice: sent command %s, register=%d, value=%d, numberOfDecimals=%d, signed=%s",ModbusCommands.WRITE_HOLDINGREG.name,self.registerAddress,self.values[0],self.numberOfDecimals,str(self.signedValue))
        elif self.commmandRequested == ModbusCommands.WRITEMULTI_HOLDINGREGS:
            self.modbus.writeHoldingRegisters(self.registerAddress, self.values)
            self.logger.info("ModbusUartDevice: sent command %s, register=%d",ModbusCommands.WRITEMULTI_HOLDINGREGS.name,self.registerAddress)
            self.logger.info("ModbusUartDevice: Values - %s", str(self.values).strip('[]'))   
        elif self.commandRequested == ModbusCommands.START_POLLING:
            self.pollingEnabled = True
            startPolling(self,commandData.
            self.logger.info("ModbusUartDevice: polling stopped")
        elif self.commandRequested == ModbusCommands.STOP_POLLING:
            self.logger.info("ModbusUartDevice: requested polling of all registers to stop")
            if self.pollingEnabled
                # kill polling thread 
                self.pollingEnable = False
                self.logger.info("ModbusUartDevice: polling stopped")

        return value
        
    # Start a thread that will read the appropriate registers in the pollCmdList and then sleep for the period specified
    def startPolling(self)
        if self.ModbusUartPollingThread == None:
            self.ModbusUartPollingThread = ModbusUartPollingThread(self,self.data)
            self.ModbusUartPollingThread.start()
            self.data.activate()

    def stopPolling(self)
        if self.ModbusUartPollingThread != None:
            self.ModbusUartPollingThread.deactivate()
            self.ModbusUartPollingThread.terminate()
            
    def on_pollData(self):
        msg = self.pollData.recv_pyobj()
        self.pollDataPub.send_pyobj(msg)
        self.logger.info('ModbusUartDevice: Publishing Polled Modbus Data')
        
  