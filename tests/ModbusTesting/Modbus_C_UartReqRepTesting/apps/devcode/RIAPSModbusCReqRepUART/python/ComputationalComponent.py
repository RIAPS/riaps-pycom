#ComputationalComponent.py
from riaps.run.comp import Component
import os
import logging

class ComputationalComponent(Component):
    def __init__():
        super(ComputationalComponent, self).__init__()	        
        self.pid = os.getpid()
        self.logger.info("(PID %s) - starting ComputationalComponent, %s",str(self.pid),str(now))
        
    def on_clock(self):
        now = self.clock.recv_pyobj()
        self.logger.info('PID(%s) - on_clock(): %s',str(self.pid),str(now))
    def on_modbusReqPort(self):
        req = self.modbusReqPort.recv_pyobj()
        self.logger.info("PID (%s) - on_modbusReqPort():%s",str(self.pid),str(req))
        
	def __destroy__(self):			
		self.logger.info("(PID %s) - stopping ComputationalComponent, %s",str(self.pid),now)   	        	        
