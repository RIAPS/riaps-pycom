# import riaps
from riaps.run.comp import Component
import logging
import random
import os
import time
import random, string

def randomword(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

# Space  limited component

class SpcLimit(Component):
    def __init__(self):
        super(SpcLimit, self).__init__()
        self.logger.info('SpcLimit[%d]', os.getpid())
        self.chain = []
        self.delta = 1 # 1 MB
        self.size = self.delta
        self.name = '/tmp/tmp%s' % randomword(8)
            
    def waste(self):
        try:
            cmd = 'dd if=/dev/zero of=%s bs=1M count=%d' % (self.name,self.size)
            res = os.system(cmd)
        except:     
            self.logger.info("waste: op failed at %d" % (self.size))
        if res == 0:
            self.size += self.delta
        
    def on_ticker(self):
        trg = self.ticker.recv_pyobj()              # Receive time (as float)
        now = time.time() 
        self.logger.info('on_ticker():%s at %s, waste = %d' % (trg,now,self.size))
        self.waste()
        
    def handleSpcLimit(self):
        self.logger.info('handleSpcLimit() ')
        os.remove(self.name)
        self.size = self.delta
   
    def __destroy__(self):
        os.remove(self.name)
        self.logger.info("__destroy__")