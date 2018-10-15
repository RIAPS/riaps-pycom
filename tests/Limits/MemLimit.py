# import riaps
from riaps.run.comp import Component
import logging
import random
import os
import time

# Memory  limited component

class MemLimit(Component):
    def __init__(self):
        super(MemLimit, self).__init__()
        self.logger.info('MemLimit[%d]', os.getpid())
        self.chain = []
        self.delta = 64 * 1024 * 1024 # 64MB
            
    def waste(self):
        arr = bytearray(self.delta)
        self.chain.append(arr)        
        
    def on_ticker(self):
        trg = self.ticker.recv_pyobj()              # Receive time (as float)
        now = time.time() 
        self.logger.info('on_ticker():%s at %s, waste = %d' % (trg,now,self.delta*len(self.chain)))
        self.waste()
        
    def handleCPULimit(self):
        self.logger.info('handleCPULimit() - ignore')
        
    def handleMemLimit(self):
        self.chain = self.chain[:1]            # Throttle back  
        self.logger.info('handleMemLimit(): waste = %d' %(self.delta*len(self.chain)))
   
