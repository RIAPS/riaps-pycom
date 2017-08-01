'''
Created on Jul 28, 2017
@author: Tim Krentz
'''

'''
The UART device component utilizes Adafruit_BBIO.UART to setup the device tree
overlays, to be used with pySerial. To install Adafruit_BBIO, run:
    $ sudo pip3 install Adafruit_BBIO
'''

from riaps.run.comp import Component
import logging
import os
import threading
import Adafruit_BBIO.UART as UART
import serial
#import pydevd
import zmq


class uartDeviceThread(threading.Thread):
    def __init__(self, component, trigger):
        threading.Thread.__init__(self)
        self.terminated = threading.Event()
        self.terminated.clear()
        self.active = threading.Event()
        self.component = component
        self.trigger = trigger
        self.uartAvailable = False
        self.pid = os.getpid()
        self.component.logger.info("uartDeviceThread [%s]: init",self.pid)

        # Convert input configurations into enums that represent the requests
        if self.component.uart_port_name == 'UART1':
            self.serial_port = '/dev/tty01'
        elif self.component.uart_port_name == 'UART2':
            self.serial_port = '/dev/tty02'
        elif self.component.uart_port_name == 'UART3':
            self.serial_port = '/dev/tty03'
        elif self.component.uart_port_name == 'UART4':
            self.serial_port = '/dev/tty04'
        elif self.component.uart_port_name == 'UART5':
            self.serial_port = '/dev/tty05'
        else:
            self.component.logger.error('''uartDeviceThread [%s]: Invalid UART
                                        argument, used UART1..5''', self.pid)
            self.terminated.set()

    def run(self):
        # Ask parent port to make a plug for this end
        self.plug = self.trigger.setupPlug(self)
        self.poller = zmq.Poller()
        self.poller.register(self.plug, zmq.POLLIN)
        if self.terminated.is_set(): return
        self.enableUart()  # setup the requested GPIO

        while True:
            self.active.wait(None)
            if self.terminated.is_set():
                self.disableGpio()
                break
            if self.active.is_set():
                socks = dict(self.poller.poll())
                if self.plug in socks and socks[self.plug] == zmq.POLLIN:
                    msgType, msgVal = self.plug.recv_pyobj()

                    if msgType == 'open':
                        self.component.logger.info(
                            'uartDeviceThread - Opening %s on %s',
                            self.component.uart_port_name, self.serial_port)
                        openUart()
                        self.plug.send_pyobj(msgType)

                    elif msgType == 'close':
                        self.component.logger.info(
                            'uartDeviceThread - Closing %s on %s',
                            self.component.uart_port_name, self.serial_port)
                        closeUart()
                        self.plug.send_pyobj(msgType)

                    elif msgType == 'read':
                        self.component.logger.info(
                            'uartDeviceThread - Reading %s bytes on %s...',
                            str(msgVal), self.component.uart_port_name)
                        inputBytes = readUart(int(msgVal))
                        self.plug.send_pyobj((msgType,inputBytes))

                    elif msgType == 'write':
                        self.component.logger.info(
                            'uartDeviceThread - Writing on %s...',
                            self.component.uart_port_name)
                        returnVal = writeUart(msgVal)
                        self.plug.send_pyobj((msgType,returnVal))

                    elif msgType == 'get_in_waiting':
                        self.plug.send_pyobj((msgType,getInWaiting()))

                    elif msgType == 'get_out_waiting':
                        self.plug.send_pyobj((msgType,getOutWaiting()))

                    elif msgType == 'send_break':
                        self.component.logger.info(
                            'uartDeviceThread - Sending break on %s...',
                            self.component.uart_port_name)
                        sendUartBreak()
                        self.plug.send_pyobj(msgType)

                    elif msgType == 'get_break_condition':
                        self.plug.send_pyobj((msgType,getUartBreak()))

                    elif msgType == 'set_break_condition':
                        setUartBreak(msgVal)
                        self.plug.send_pyobj(msgType)

                    else:
                        self.component.logger.warning(
                            'uartDeviceThread - LOCAL MESSAGE ERROR'
                            ' RECEIVED: %s',
                            msgType)
                        self.plug.send_pyobj(msgType)


    def openUart(self):
        self.ser.open()

    def closeUart(self):
        self.ser.close()

    def readUart(self,numBytes):
        return self.ser.read(numBytes)

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
        self.component.logger.info('''uartDeviceThread setting up UART=%s:
            baudrate=%s [%d]''', self.component.uart_port_name,
            self.component.baud_rate, self.pid)
        UART.setup(self.component.uart_port_name)
        self.ser = serial.Serial(port = self.serial_port,
                                 baudrate = self.baud_rate)
        self.component.logger.info('''uartDeviceThread %s setup and
            available for use''', self.component.uart_port_name)
        self.uartAvailable = True

    def disableUart(self):
        self.ser.close()
        self.uartAvailable = False
        self.component.logger.info(
            "uartDeviceThread: closed %s",
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
    def __init__(self, uart_port_name='UART1', baud_rate=9600):
        super().__init__()
        self.logger.setLevel(logging.DEBUG)
        self.pid = os.getpid()
        self.uart_port_name = uart_port_name
        self.baud_rate = baud_rate

#        pydevd.settrace(host='192.168.1.102',port=5678)
        self.logger.info("UartDeviceComponent @%s: baudrate=%s delay=%d [%d]", self.uart_port_name, self.baud_rate, self.pid)
        self.uartDeviceThread = None                    # Cannot manipulate GPIOs in constructor or start threads


    def on_clock(self):
        now = self.clock.recv_pyobj()   # Receive time (as float)
        self.logger.info("on_clock()[%s]: %s",str(self.pid),now)

        if self.uartDeviceThread == None:
            self.uartDeviceThread = uartDeviceThread(self,self.trigger)
            self.uartDeviceThread.start()
            self.trigger.activate()

        self.clock.halt()

    def __destroy__(self):
        self.logger.info("__destroy__")
        if self.uartDeviceThread != None:
            self.uartDeviceThread.deactivate()
            self.uartDeviceThread.terminate()

    def on_uartRepPort(self):
        msg = self.uartRepPort.recv_pyobj()
        self.logger.info("on_uartRepPort")
        if self.uartDeviceThread == None:
            self.logger.info("on_uartRepPort()[%s]: uartDeviceThread not available yet",str(self.pid))
            msg = ('ERROR',-1)
            self.uartRepPort.send_pyobj(msg)
        else:
            if self.uartDeviceThread.isUartAvailable() == True:
                msgType, msgVal = msg
                self.logger.info("on_uartRepPort()[%s]: %s",str(self.pid),repr(msg))

                if msgType == 'open':
                    self.trigger.send_pyobj(('open',0))
                    response = self.trigger.recv_pyobj()
                    self.uartRepPort.send_pyobj(('open',response))

                if msgType == 'close':
                    self.trigger.send_pyobj(('close',0))
                    response = self.trigger.recv_pyobj()
                    self.uartRepPort.send_pyobj(('close',response))

                elif msgType == 'read':
                    self.trigger.send_pyobj(('read',msgVal))
                    readBytes = self.trigger.recv_pyobj()
                    self.uartRepPort.send_pyobj((msgType,readBytes))

                elif msgType == 'write':
                    self.trigger.send_pyobj(('write',msgVal))
                    numBytesWritten = self.trigger.recv_pyobj()
                    self.uartRepPort.send_pyobj((msgType,numBytesWritten))

                elif msgType == 'get_in_waiting':
                    self.trigger.send_pyobj(('get_in_waiting',0))
                    numInWaiting = self.trigger.recv_pyobj()
                    self.uartRepPort.send_pyobj((msgType,numInWaiting))

                elif msgType == 'get_out_waiting':
                    self.trigger.send_pyobj(('get_out_waiting',0))
                    numOutWaiting = self.trigger.recv_pyobj()
                    self.uartRepPort.send_pyobj((msgType,numOutWaiting))

                elif msgType == 'send_break':
                    self.trigger.send_pyobj(('send_break',0))
                    response = self.trigger.recv_pyobj()
                    self.uartRepPort.send_pyobj((msgType,response))

                elif msgType == 'get_break_condition':
                    self.trigger.send_pyobj(('get_break_condition',0))
                    response = self.trigger.recv_pyobj()
                    self.uartRepPort.send_pyobj((msgType,response))

                elif msgType == 'set_break_condition':
                    self.trigger.send_pyobj(('set_break_condition',msgVal))
                    response = self.trigger.recv_pyobj()
                    self.uartRepPort.send_pyobj((msgType,response))

                else:
                    self.component.logger.warning(
                        'uartDevice - COMMAND NOT FOUND: %s',
                        msgType)
                    self.plug.send_pyobj(('ERROR',-1))

            else:
                self.logger.info("on_uartRepPort()[%s]: UART not available yet",str(self.pid))
                msg = ('ERROR',-1)
                self.uartRepPort.send_pyobj(msg)
