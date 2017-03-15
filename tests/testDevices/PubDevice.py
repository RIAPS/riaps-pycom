#
from riaps.run.comp import Component
import logging
import uuid
import time
import os

class PubDevice(Component):
    def __init__(self):
        super(PubDevice, self).__init__()
        self.logger.info("%s - starting",str(os.getpid()))
        self.messageCounter = 0

    def on_clock(self):
        msg = self.clock.recv_pyobj() # Receive (timestamp,value)
        self.messageCounter+=1
        self.sendDeviceData.send_pyobj(self.messageCounter)