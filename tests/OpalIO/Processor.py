#
from riaps.run.comp import Component
import logging
import uuid
import time
import os


class Processor(Component):
    def __init__(self):
        super().__init__()
        self.uuid = uuid.uuid4().int
        self.pid = os.getpid()
        self.logger.info("%s - starting",str(self.pid))

    def on_rx_c37data(self):
        msg = self.rx_c37data.recv_pyobj() # Receive DataFrame
        self.logger.info("on_rx_c37data()[%s]: %s", str(self.pid), repr(msg))
        
    def on_rx_c37header(self):
        msg = self.rx_c37header.recv_pyobj() # Receive DataFrame
        self.logger.info("on_rx_c37header()[%s]: %s", str(self.pid), repr(msg))
        
    def on_rx_c37config(self):
        msg = self.rx_c37config.recv_pyobj() # Receive DataFrame
        self.logger.info("on_rx_c37config()[%s]: %s", str(self.pid), repr(msg))