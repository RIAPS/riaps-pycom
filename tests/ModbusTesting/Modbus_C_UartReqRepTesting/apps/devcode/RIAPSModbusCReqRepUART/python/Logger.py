#Logger.py
from riaps.run.comp import Component
import os
import logging

class Logger(Component):
    def __init__(,,,,,):
        super(Logger, self).__init__()	        
        self.pid = os.getpid()
        self.logger.info("(PID %s) - starting Logger, %s",str(self.pid),str(now))
        
    def on_rx_modbusData(self):
        msg = self.rx_modbusData.recv_pyobj()
        self.logger.info("PID (%s) - on_rx_modbusData():%s",str(self.pid), str(msg))
        
	def __destroy__(self):			
		self.logger.info("(PID %s) - stopping Logger, %s",str(self.pid),now)   	        	        
