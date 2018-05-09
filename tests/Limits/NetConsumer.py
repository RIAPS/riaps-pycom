#
from riaps.run.comp import Component
import logging
import os

class NetConsumer(Component):
    def __init__(self):
        super(NetConsumer, self).__init__()
        self.pid = os.getpid()
        self.logger.info("NetConsumer[%d]",self.pid)
        
    def on_consume(self):
        msg = self.consume.recv_pyobj()
        self.logger.info("on_consume()[%d]:%d", self.pid,len(msg))

    