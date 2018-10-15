# import riaps
from riaps.run.comp import Component
import logging
import random
import os
import time

# CPU limited component

class CPULimit(Component):
    def __init__(self):
        super(CPULimit, self).__init__()
        self.logger.info('CPULimit[%d]', os.getpid())
        self.limit = 200000 # min, max ~ 215000
            
    def waste(self):
        self.limit = self.limit + 1000      # Increase limit, do more cycles
        limit = self.limit
        "-".join(str(n) for n in range(self.limit))         
        
    def on_ticker(self):
        trg = self.ticker.recv_pyobj()              # Receive time (as float)
        now = time.time() 
        self.logger.info('on_ticker():%s at %s, limit = %d' % (trg,now,self.limit))
        self.waste()
        
    def handleCPULimit(self):
        self.logger.info('handleCPULimit()')
        self.limit = self.limit - 3000      # Throttle back
        
    def handleMemLimit(self):
        self.logger.info('handleMemLimit()')
        # self.limit = self.limit - 3000      # Throttle back
