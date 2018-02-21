# import riaps
from riaps.run.comp import Component
import logging
import os

class NetProducerLimit(Component):
    def __init__(self):
        super(NetProducerLimit, self).__init__()
        self.pid = os.getpid()
        self.logger.info("NetProducer [%d]" % self.pid)
        self.blk = 512
        self.min = 1*self.blk
        self.max = 4*self.blk
        self.size = self.min
        
    def on_ticker(self):
        now = self.ticker.recv_pyobj()   # Receive time.time() as float
        self.logger.info('on_ticker()[%d]: %s',self.pid,str(now))
        msg = bytearray(self.size)
        self.produce.send_pyobj(msg)
        self.size = self.size + self.blk
        if self.size == self.max: self.size = self.min
        
    def handleNetLimit(self):
        self.logger.info('handleNetLimit')
        self.size = self.min
        
        