'''
Created on Jul 28, 2017
@author: Tim Krentz


The UART Device Component assumes the BBB has the appropriate device tree
overlay installed.

Add the below line to /boot/uEnv.txt and restart (for UART2 only)
cape_enable=bone_capemgr.enable_partno=BB-UART2
'''

from riaps.run.comp import Component
import logging
import os
import threading
import serial
import zmq
from enum import Enum


class UartDeviceThread(threading.Thread):
    def __init__(self, component, command, data):
        threading.Thread.__init__(self)
        self.terminated = threading.Event()
        self.terminated.clear()
        self.active = threading.Event()
        self.component = component
        self.command = command
        self.data = data
        self.uartAvailable = False
        self.pid = os.getpid()
        self.pollerTimeout = None

        self.readingActive = False
        self.readBuffer = bytes(0)

        self.component.logger.info("UartDeviceThread [%s]: init",self.pid)

        # Convert input configurations into enums that represent the requests
        if self.component.uart_port_name == 'UART1':
            self.serial_port = '/dev/ttyO1'
        elif self.component.uart_port_name == 'UART2':
            self.serial_port = '/dev/ttyO2'
        elif self.component.uart_port_name == 'UART3':
            self.serial_port = '/dev/ttyO3'
        elif self.component.uart_port_name == 'UART4':
            self.serial_port = '/dev/ttyO4'
        elif self.component.uart_port_name == 'UART5':
            self.serial_port = '/dev/ttyO5'
        else:
            self.component.logger.error('UartDeviceThread [%s]: Invalid UART'
                                        ' argument, use UART1..5', self.pid)
            self.terminated.set()

    def run(self):
        self.plug = self.command.setupPlug(self)
        self.dataPlug = self.data.setupPlug(self)
        self.poller = zmq.Poller()
        self.poller.register(self.plug, zmq.POLLIN)
        if self.terminated.is_set(): return
        self.enableUart()

        while True:
            self.active.wait(None)
            if self.terminated.is_set():
                self.disableUart()
                break
            if self.active.is_set():
                socks = dict(self.poller.poll(timeout = self.pollerTimeout))
                if self.plug in socks and socks[self.plug] == zmq.POLLIN:
                    msgType, msgVal = self.plug.recv_pyobj()

                    if msgType == UartDeviceComponent.Message.open:
                        self.component.logger.info(
                            'UartDeviceThread - Opening %s on %s',
                            self.component.uart_port_name, self.serial_port)
                        self.openUart()
                        self.plug.send_pyobj((msgType,1))

                    elif msgType == UartDeviceComponent.Message.close:
                        self.component.logger.info(
                            'UartDeviceThread - Closing %s on %s',
                            self.component.uart_port_name, self.serial_port)
                        self.closeUart()
                        self.plug.send_pyobj((msgType,1))

                    elif msgType == UartDeviceComponent.Message.read:
                        if self.readingActive == False:
                            self.readingActive = True
                            self.readSize = msgVal
                            self.plug.send_pyobj((msgType,1))
                            self.readUart()

                    elif msgType == UartDeviceComponent.Message.write:
                        self.component.logger.info(
                            'UartDeviceThread - Writing on %s...',
                            self.component.uart_port_name)
                        returnVal = self.writeUart(msgVal)
                        self.plug.send_pyobj((msgType,returnVal))

                    elif msgType == UartDeviceComponent.Message.get_in_waiting:
                        self.plug.send_pyobj((msgType,getInWaiting()))

                    elif msgType == UartDeviceComponent.Message.get_out_waiting:
                        self.plug.send_pyobj((msgType,getOutWaiting()))

                    elif msgType == UartDeviceComponent.Message.send_break:
                        self.component.logger.info(
                            'UartDeviceThread - Sending break on %s...',
                            self.component.uart_port_name)
                        self.sendUartBreak()
                        self.plug.send_pyobj((msgType,1))

                    elif msgType == UartDeviceComponent.Message.get_break_condition:
                        self.plug.send_pyobj((msgType,getUartBreak()))

                    elif msgType == UartDeviceComponent.Message.set_break_condition:
                        self.setUartBreak(msgVal)
                        self.plug.send_pyobj((msgType,1))

                    else:
                        self.component.logger.warning(
                            'UartDeviceThread - LOCAL MESSAGE ERROR'
                            ' RECEIVED: %s',msgType)
                        self.plug.send_pyobj((msgType,0))

                elif self.readingActive == True:
                    self.readUart()



    def openUart(self):
        self.ser.open()

    def closeUart(self):
        self.ser.close()

    def readUart(self):
        if self.ser.is_open == True:
            self.readBuffer = self.readBuffer+self.ser.read(self.readSize)
            self.component.logger.info('UartDeviceThread: Attempting to read...')

            # Limit buffer size to 16KB, more than the maximum number of bytes
            # one could expect to receive in 1s at 115200/8N1
            self.readBuffer = self.readBuffer[-16384:]

            if len(self.readBuffer) < self.readSize:
                # self.localZmqPublisher.send_string('localTopic')
                self.pollerTimeout = 0
            else:
                self.component.logger.info('UartDeviceThread: DONE READING')
                bytesOut = self.readBuffer[0:self.readSize]
                self.readBuffer = self.readBuffer[self.readSize:]
                self.readingActive = False
                self.readSize = 0
                self.pollerTimeout = None
                self.dataPlug.send_pyobj(('read',bytesOut))
        else:
            self.component.logger.warning(
                    'UartDeviceThread - TRYING TO READ ON CLOSED PORT')

    def writeUart(self, data):
        return self.ser.write(data)

    def getInWaiting(self):
        return self.ser.in_waiting()

    def getOutWaiting(self):
        return self.ser.out_waiting()

    def sendUartBreak(self):
        self.ser.send_break()

    def getUartBreak(self):
        return self.ser.break_condition

    def setUartBreak(self,value):
        self.ser.break_condition = value

    def isUartAvailable(self):
        return self.uartAvailable

    def enableUart(self):
        self.component.logger.info('UartDeviceThread setting up UART=%s:'
            ' baudrate=%s [%d]', self.component.uart_port_name,
            self.component.baud_rate, self.pid)
        self.ser = serial.Serial(port = self.serial_port,
                                 baudrate = self.component.baud_rate,
                                 timeout = 1)
        self.component.logger.info('UartDeviceThread %s setup and'
            ' available for use', self.component.uart_port_name)
        self.uartAvailable = True

    def disableUart(self):
        self.ser.close()
        self.uartAvailable = False
        self.component.logger.info(
            'UartDeviceThread: closed %s',
            self.component.uart_port_name)

    def activate(self):
        self.active.set()

    def deactivate(self):
        self.active.clear()

    def terminate(self):
        self.terminated.set()

'''

UART Device Options:
    Port Name: BBB UART port (UART1, 2, 3, 4, or 5)
    Baud Rate: UART rate in bits/sec, usually specified by slave device

'''

class UartDeviceComponent(Component):
    def __init__(self, uart_port_name='UART2', baud_rate=9600):
        super().__init__()
        self.logger.setLevel(logging.DEBUG)
        self.pid = os.getpid()
        self.uart_port_name = uart_port_name
        self.baud_rate = baud_rate

        self.logger.info("UartDeviceComponent @%s: baudrate=%s [%d]",
                        self.uart_port_name, self.baud_rate, self.pid)
        self.UartDeviceThread = None

    class Message(Enum):
        open = 0
        close = 1
        read = 2
        write = 3
        get_in_waiting = 4
        get_out_waiting = 5
        send_break = 6
        get_break_condition = 7
        set_break_condition = 8

    def on_clock(self):
        now = self.clock.recv_pyobj()   # Receive time (as float)
        self.logger.info("on_clock()[%s]: %s",str(self.pid),now)

        if self.UartDeviceThread == None:
            self.UartDeviceThread = UartDeviceThread(self,self.command,self.data)
            self.UartDeviceThread.start()
            self.command.activate()
            self.data.activate()

        self.clock.halt()

    def __destroy__(self):
        self.logger.info("__destroy__")
        if self.UartDeviceThread != None:
            self.UartDeviceThread.deactivate()
            self.UartDeviceThread.terminate()

    def on_data(self):
        msg = self.data.recv_pyobj()
        self.uartReadPub.send_pyobj(msg)
        self.logger.info('UartDeviceComponent: Publishing Data')

    def on_command(self):
        msg = self.command.recv_pyobj()
        self.uartRepPort.send_pyobj(msg)

    def on_uartRepPort(self):
        msg = self.uartRepPort.recv_pyobj()
        if self.UartDeviceThread == None:
            self.logger.info("on_uartRepPort()[%s]: UartDeviceThread not available yet",str(self.pid))
            msg = ('ERROR',-1)
            self.uartRepPort.send_pyobj(msg)
        else:
            if self.UartDeviceThread.isUartAvailable() == True:
                msgType, msgVal = msg
                self.logger.info("on_uartRepPort()[%s]: %s",str(self.pid),repr(msg))

                if msgType == 'open':
                    self.command.send_pyobj((UartDeviceComponent.Message.open,0))

                if msgType == 'close':
                    self.command.send_pyobj((UartDeviceComponent.Message.close,0))

                elif msgType == 'read':
                    self.command.send_pyobj((UartDeviceComponent.Message.read,msgVal))

                elif msgType == 'write':
                    self.command.send_pyobj((UartDeviceComponent.Message.write,msgVal))

                elif msgType == 'get_in_waiting':
                    self.command.send_pyobj((UartDeviceComponent.Message.get_in_waiting,0))

                elif msgType == 'get_out_waiting':
                    self.command.send_pyobj((UartDeviceComponent.Message.get_out_waiting,0))

                elif msgType == 'send_break':
                    self.command.send_pyobj((UartDeviceComponent.Message.send_break,0))

                elif msgType == 'get_break_condition':
                    self.command.send_pyobj((UartDeviceComponent.Message.get_break_condition,0))

                elif msgType == 'set_break_condition':
                    self.command.send_pyobj((UartDeviceComponent.Message.set_break_condition,msgVal))

            else:
                self.logger.info("on_uartRepPort()[%s]: UART not available yet",str(self.pid))
                msg = ('ERROR',-1)
                self.uartRepPort.send_pyobj(msg)
