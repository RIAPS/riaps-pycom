'''
Created on Jun 5, 2018

@author: jeholliday
'''
# import riaps
from riaps.run.comp import Component
from riaps.utils.logging import NetLogHandler
import logging
import time
import os
import socket

class TempMonitor(Component):
    def __init__(self):
        super(TempMonitor, self).__init__()
        self.netLog = NetLogHandler()
        self.logger.addHandler(self.netLog)
        self.pid = os.getpid()
        self.hostname = socket.gethostname()
        self.logger.info("["+self.hostname +"]("+str(self.pid)+")-starting TempMonitor")
        
    def on_tempupdate(self):
        # Receive: timestamp,temperature
        temperatureTime, temperatureValue = self.tempupdate.recv_pyobj() 
        self.logger.info("["+self.hostname +"]on_tempupdate(): Temperature: "+ str(temperatureValue)+", Timestamp: "+ str(temperatureTime))
        
    def __destroy__(self):
        self.logger.info("["+self.hostname +"]("+str(self.pid)+")-stoping TempMonitor")