#TempSensor.py
from riaps.run.comp import Component
import os
import logging
import time

class TempSensor(Component):
    def __init__(self):
       super(TempSensor, self).__init__()	        
       self.pid = os.getpid()
       self.temperature = 65 # Example
       now = time.ctime(int(time.time())) # Manually added 
       self.logger.info("(PID %s) - starting TempSensor, %s",str(self.pid),str(now)) #Generated, but now is not defined... 
        
    
    def on_clock(self):
       now = self.clock.recv_pyobj()
       self.logger.info('PID(%s) - on_clock(): %s',str(self.pid),str(now))
       self.temperature = self.temperature + 1 #Example
       msg = (now, str(self.temperature)) #Example
       self.logger.info("on_clock(): Temperature - %s, PID %s, %s",str(msg[1]),str(self.pid),str(now)) #Example
       self.ready.send_pyobj(msg) #Example
    
    def __destroy__(self):			
       self.logger.info("(PID %s) - stopping TempSensor, %s",str(self.pid),now)   	        	        
