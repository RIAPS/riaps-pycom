# import riaps
from riaps.run.comp import Component
import logging
import random
import os
import threading
import zmq
import time
import Adafruit_BBIO.GPIO as GPIO

class GPIODevice(Component):
    def __init__(self):
        super(GPIODevice, self).__init__()
        self.logger.info("GPIODevice - starting")
        ''' Enable GPIO '''
        self.pinName = 'USR3'
        self.gpioOn = GPIO.HIGH
        self.gpioOff = GPIO.LOW
        GPIO.setup(self.pinName,GPIO.OUT)

    def on_blink(self):
        msg = self.blink.recv_pyobj()            # Receive blink message
        self.logger.info('on_blink():%s' % msg)
        ''' Toggle GPIO '''
        GPIO.output(self.pinName, self.gpioOn)
        time.sleep(0.250)
        GPIO.output(self.pinName, self.gpioOff)

    def __destroy__(self):
        self.logger.info("GPIODevice - stopping")
        GPIO.output(self.pinName, self.gpioOff)
        time.sleep(0.250)
        GPIO.cleanup(self.pinName)
        
