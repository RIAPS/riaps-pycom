#
from riaps.run.comp import Component
import logging
import uuid
import time
import os


class Concentrator(Component):
    def __init__(self):
        super().__init__()
        self.uuid = uuid.uuid4().int
        self.pid = os.getpid()
        self.logger.info("%s - starting",str(self.pid))

    def on_pmuDataReady(self):
        msg = self.pmuDataReady.recv_pyobj() # Receive DataFrame
        self.logger.info("on_pmuDataReady()[%s]: %s", str(self.pid), repr(msg))
        
    def on_display(self):
        msg = self.display.recv_pyobj()
        self.logger.info('on_display()[%s]', str(self.pid))
