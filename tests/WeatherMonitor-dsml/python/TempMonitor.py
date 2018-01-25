#TempMonitor.py
from riaps.run.comp import Component
import os
import logging
import time


class TempMonitor(Component):
    def __init__(self):
       super(TempMonitor, self).__init__()	        
       self.pid = os.getpid()
       now = time.ctime(int(time.time()))
       self.logger.info("(PID %s) - starting TempMonitor, %s",str(self.pid),str(now))
        
    
    def on_tempupdate(self):
       msg = self.tempupdate.recv_pyobj()
       now = time.ctime(int(time.time())) 
       temperatureTime, temperatureValue = msg # Example
       self.logger.info("on_tempupdate(): Temperature:%s, PID %s, Timestamp:%s", temperatureValue, str(now), temperatureTime) # Example
       self.logger.info("PID (%s) - on_tempupdate():%s",str(self.pid),str(msg))
    
    def __destroy__(self):
        now = time.time()
        self.logger.info("(PID %s) - stopping TempMonitor, %s",str(self.pid),now)   	        	        
