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


class UartDeviceThread(threading.Thread):
    def __init__(self, component, trigger):
        threading.Thread.__init__(self)
        self.terminated = threading.Event()
        self.terminated.clear()
        self.active = threading.Event()
        self.component = component
        self.trigger = trigger
        self.uartAvailable = False
        self.pid = os.getpid()

        self.readingActive = False
        self.readBuffer = bytes(0)

        self.localZmqContext = zmq.Context()
        self.localZmqPublisher = self.localZmqContext.socket(zmq.PUB)
        self.localZmqSubscriber = self.localZmqContext.socket(zmq.SUB)
        self.localZmqPublisher.bind('tcp://*:6789')
        self.localZmqSubscriber.connect('tcp://localhost:6798')
        self.localZmqSubscriber.setsockopt_string(zmq.SUBSCRIBE,'localTopic')


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
        self.plug = self.trigger.setupPlug(self)
        self.poller = zmq.Poller()
        self.poller.register(self.plug, zmq.POLLIN)
        self.poller.register(self.localZmqSubscriber, zmq.POLLIN)
        if self.terminated.is_set(): return
        self.enableUart()

        while True:
            self.active.wait(None)
            if self.terminated.is_set():
                self.disableUart()
                break
            if self.active.is_set():
                socks = dict(self.poller.poll())
                if self.plug in socks and socks[self.plug] == zmq.POLLIN:
                    msgType, msgVal = self.plug.recv_pyobj()


                    if msgType == 0:
                        self.component.logger.info(
                            'UartDeviceThread - Opening %s on %s',
                            self.component.uart_port_name, self.serial_port)
                        self.openUart()
                        self.plug.send_pyobj((msgType,1))

                    elif msgType == 1:
                        self.component.logger.info(
                            'UartDeviceThread - Closing %s on %s',
                            self.component.uart_port_name, self.serial_port)
                        self.closeUart()
                        self.plug.send_pyobj((msgType,1))

                    elif msgType == 2:
                        # self.component.logger.info(
                        #     'UartDeviceThread - Reading %s bytes on %s...',
                        #     str(msgVal), self.component.uart_port_name)
                        # inputBytes = self.readUart(int(msgVal))
                        # self.plug.send_pyobj((msgType,inputBytes))

                        if self.readingActive == False:
                            self.readingActive = True
                            self.readSize = msgVal
                            self.readUart()
                            self.plug.send_pyobj((msgType,1))

                    elif msgType == 3:
                        self.component.logger.info(
                            'UartDeviceThread - Writing on %s...',
                            self.component.uart_port_name)
                        returnVal = self.writeUart(msgVal)
                        self.plug.send_pyobj((msgType,returnVal))

                    elif msgType == 4:
                        self.plug.send_pyobj((msgType,getInWaiting()))

                    elif msgType == 5:
                        self.plug.send_pyobj((msgType,getOutWaiting()))

                    elif msgType == 6:
                        self.component.logger.info(
                            'UartDeviceThread - Sending break on %s...',
                            self.component.uart_port_name)
                        self.sendUartBreak()
                        self.plug.send_pyobj((msgType,1))

                    elif msgType == 7:
                        self.plug.send_pyobj((msgType,getUartBreak()))

                    elif msgType == 8:
                        self.setUartBreak(msgVal)
                        self.plug.send_pyobj((msgType,1))

                    else:
                        self.component.logger.warning(
                            'UartDeviceThread - LOCAL MESSAGE ERROR'
                            ' RECEIVED: %s',msgType)
                        self.plug.send_pyobj((msgType,0))

                elif self.localZmqSubscriber in socks and socks[self.localZmqSubscriber] == zmq.POLLIN:
                    msg = self.localZmqSubscriber.recv_string()
                    self.readUart()



    def openUart(self):
        self.ser.open()

    def closeUart(self):
        self.ser.close()

    def readUart(self):
        self.readBuffer = self.readBuffer+self.ser.read(128)
        if len(self.readBuffer < self.readSize):
            self.localZmqPublisher.send_string('localTopic')
        else:
            bytesOut = self.readBuffer[0:self.readSize]
            self.readBuffer = self.readBuffer[self.readSize:]
            self.readingActive = False
            self.readSize = 0
            self.uartReadPub.send_pyobj(('read',bytesOut))

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
                                 timeout = 0)
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


    def on_clock(self):
        now = self.clock.recv_pyobj()   # Receive time (as float)
        self.logger.info("on_clock()[%s]: %s",str(self.pid),now)

        if self.UartDeviceThread == None:
            self.UartDeviceThread = UartDeviceThread(self,self.trigger)
            self.UartDeviceThread.start()
            self.trigger.activate()

        self.clock.halt()

    def __destroy__(self):
        self.logger.info("__destroy__")
        if self.UartDeviceThread != None:
            self.UartDeviceThread.deactivate()
            self.UartDeviceThread.terminate()

    def on_trigger(self):
        msg = self.trigger.recv_pyobj()
        self.uartRepPort.send_pyobj(msg)

    def on_uartRepPort(self):
        msg = self.uartRepPort.recv_pyobj()
        self.logger.info("on_uartRepPort")
        if self.UartDeviceThread == None:
            self.logger.info("on_uartRepPort()[%s]: UartDeviceThread not available yet",str(self.pid))
            msg = ('ERROR',-1)
            self.uartRepPort.send_pyobj(msg)
        else:
            if self.UartDeviceThread.isUartAvailable() == True:
                msgType, msgVal = msg
                self.logger.info("on_uartRepPort()[%s]: %s",str(self.pid),repr(msg))

                if msgType == 'open':
                    self.trigger.send_pyobj((0,0))

                if msgType == 'close':
                    self.trigger.send_pyobj((1,0))

                elif msgType == 'read':
                    self.trigger.send_pyobj((2,msgVal))

                elif msgType == 'write':
                    self.trigger.send_pyobj((3,msgVal))

                elif msgType == 'get_in_waiting':
                    self.trigger.send_pyobj((4,0))

                elif msgType == 'get_out_waiting':
                    self.trigger.send_pyobj((5,0))

                elif msgType == 'send_break':
                    self.trigger.send_pyobj((6,0))

                elif msgType == 'get_break_condition':
                    self.trigger.send_pyobj((7,0))

                elif msgType == 'set_break_condition':
                    self.trigger.send_pyobj((8,msgVal))

            else:
                self.logger.info("on_uartRepPort()[%s]: UART not available yet",str(self.pid))
                msg = ('ERROR',-1)
                self.uartRepPort.send_pyobj(msg)
