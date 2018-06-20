'''
Created on Jun 5, 2018

@author: jeholliday
'''
from riaps.run.comp import Component
from riaps.utils.logging import NetLogHandler
import logging
import time
import os
import socket

class TempSensor(Component):
    def __init__(self):
        super(TempSensor, self).__init__()
        self.netLog = NetLogHandler()
        self.logger.addHandler(self.netLog)
        self.pid = os.getpid()
        self.temperature = 65
        self.hostname = socket.gethostname()
        self.logger.info("["+self.hostname +"]("+str(self.pid)+")-starting TempSensor")
        self.logger.info("["+self.hostname +"]Initial temp:"+str(self.temperature))
        
    def on_clock(self):
        now = time.ctime(int(time.time()))
        msg = self.clock.recv_pyobj()
        self.temperature = self.temperature + 1
        msg = str(self.temperature)
        msg = (now,msg)       
        self.logger.info("["+self.hostname +"]on_clock(): Temperature - " + str(msg[1]))
        self.ready.send_pyobj(msg)
               
    def __destroy__(self):
        self.logger.info("["+self.hostname +"]("+str(self.pid)+")-stopping TempSensor")         

