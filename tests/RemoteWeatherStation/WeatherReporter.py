'''
Created on Feb 12, 2017

@author: riaps
'''

'''
The UART device component utilizes pySerial for communications
Need to install it in the development environment 
    $ sudo pip3 install pyserial
'''

# import riaps
from riaps.run.comp import Component
import logging
import os
import threading
#import zmq
#import time
import serial
import pydevd
import sys

    
class WReporterThread(threading.Thread):
    def __init__(self, component):
        threading.Thread.__init__(self)     
        self.terminated = threading.Event()
        self.terminated.clear()
        self.component = component
        self.wrserial = None
        self.writeRequest = False
        self.pid = os.getpid()
        self.component.logger.info("WReporterThread [%s]: init",self.pid)
    
    def run(self):
        # Ask parent port to make a plug for this end
        self.dataIn_plug = self.component.dataIn_queue.setupPlug(self)  
        self.dataOut_plug = self.component.dataOut_queue.setupPlug(self)
        
        if self.terminated.is_set(): return
        
        self.openPort()  # open serial port
        self.ser.flushInput()
        self.ser.flushOutput()
   
        # for debugging
#        data = self.ser.write(b'Hello World\n')   
        
        while True:
            if self.terminated.is_set():
                self.ser.close() 
                self.component.logger.info("WReporterThread - close serial port: %s",self.component.port)
                break
            
            if self.writeRequest:
                dataOut = self.dataOut_plug.recv_pyobj()
                
                try:
                    numBytesWritten = self.ser.write(str.encode(dataOut))   
                    self.component.logger.info("WReporterThread - written to UART %s bytes", numBytesWritten)            
                    self.writeRequest = False
                    
                except serial.SerialTimeoutException:
                    self.component.logger.error("WReporterThread - writing timeout error: %s",serial.SerialTimeoutException.strerror)           
                    self.ser.close()
                    break                   
                   
            else:  
                bytesToRead = self.ser.inWaiting()
#                pydevd.settrace(host="192.168.1.103",port=5678) #MM TODO:  for debugging
                if bytesToRead != 0:
                    try:
                        self.component.logger.info("WReporterThread - read UART1, %d bytes",bytesToRead)
                        data = self.ser.read(bytesToRead) 
                    except serial.SerialException:
                        self.component.logger.error("WReporterThread - UART1 reading error: %s",serial.SerialException.strerror)           
                        self.ser.close()
                        break                   
                                        
                    dataStr = data.decode('utf-8')   #MM TODO:  error is UnicodError, default was 'strict'
                    if dataStr != '':   # in other words, not empty
                        self.dataIn_plug.send_pyobj(dataStr) 
                        self.component.logger.info("WReporterThread - read data: %s",dataStr)                    
    
    def requestWrite(self):
        self.writeRequest = True
        self.component.logger.info("WReporterThread - write request received")
        
    def openPort(self):
        try:
            self.ser = serial.Serial(self.component.port, self.component.baudrate, self.component.bytesize, self.component.parity, self.component.stopbits, self.component.timeout)
            self.component.logger.info("WReporterThread - openPort: %s, %d, %d, %s, %d, %d",self.component.port,self.component.baudrate,self.component.bytesize,self.component.parity,self.component.stopbits,self.component.timeout)

        except serial.SerialException:
            self.component.logger.error("WReporterThread - unable to openPort: %s, %d, %d, %s, %d, %d",self.component.port,self.component.baudrate,self.component.bytesize,self.component.parity,self.component.stopbits,self.component.timeout)           
            sys.exit(-1)
            
    def terminate(self):
        self.terminated.set()

class WeatherReporter(Component):
    def __init__(self, port="ttyO1", baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, serialTimeout=0):
        super().__init__()
        self.logger.setLevel(logging.DEBUG)
        self.pid = os.getpid()
        self.port = "/dev/" + port        
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = serialTimeout  # non-blocking mode, return immediately in any case, returning zero or more, up to the requested number of bytes
        self.logger.info("WeatherReporter @%s:%d %d%s%d [%d]", self.port, self.baudrate, self.bytesize, self.parity, self.stopbits, self.pid)
        self.reportThread = None                    # Cannot manipulate ports in constructor or start threads 
        

    def on_clock(self):
        now = self.clock.recv_pyobj()   # Receive time (as float)
        self.logger.info("on_clock()[%s]: %s",str(self.pid),now)
        
        # for debugging
#        self.ser = serial.Serial(self.port, self.baudrate, self.bytesize, self.parity, self.stopbits)
#        data = self.ser.write(b'Hello RIAPS UART\n')
#        self.logger.info("WeatherReporter on_clock [%s]: %d", str(self.pid), data)

        if self.reportThread == None:
            self.reportThread = WReporterThread(self)           
            self.reportThread.start()
            self.dataIn_queue.activate()
            self.dataOut_queue.activate()
        
    def __destroy__(self):
        self.logger.info("__destroy__")
        
    #MM TODO: format error with dataFrame in logger
    def on_dataIn_queue(self):                         # Internally triggered op
        dataFrame = self.dataIn_queue.recv_pyobj()     # Receive in component data queue
        self.logger.info("on_queue()[%s]: %s",str(self.pid),dataFrame) 
        self.reportedData.send_pyobj(dataFrame)
        
    def on_listenerAck(self):
        dataAck = self.listenerAck.recv_pyobj()
        self.logger.info("on_listenerAck()[%s]: %s",str(self.pid),repr(dataAck))
        self.dataOut_queue.send_pyobj(dataAck)
        self.logger.info("on_listenerAck()[%s]: sent data to UART device")
        self.reportThread.requestWrite()
        
