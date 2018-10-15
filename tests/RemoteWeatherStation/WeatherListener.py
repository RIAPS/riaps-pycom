'''
Created on Feb 12, 2017

@author: riaps
'''
#
from riaps.run.comp import Component
#import logging
import uuid
#import time
import os
import pydevd


class WeatherListener(Component):
    def __init__(self):
        super().__init__()
#        pydevd.settrace(host='192.168.1.103',port=5678)
        self.uuid = uuid.uuid4().int
        self.pid = os.getpid()
        self.logger.info("WeatherListener: %s - starting",str(self.pid))

    def on_weatherDataReady(self):
        msg = self.weatherDataReady.recv_pyobj() # Receive DataFrame
        self.logger.info("on_weatherDataReady()[%s]: %s",str(self.pid),repr(msg))
        dataAck = "OKAY, Got it!\n"
        self.weatherDataAck.send_pyobj(dataAck)
        self.logger.info("on_weatherDataReady()[%s]: send ACK",str(self.pid))
        
    def on_display(self):
        msg = self.display.recv_pyobj()
        self.logger.info("on_display()[%s]: %s",str(self.pid),repr(msg))
        
        
