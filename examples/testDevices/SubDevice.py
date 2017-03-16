#
from riaps.run.comp import Component
import logging
import uuid
import time
import os

class SubDevice(Component):
    def __init__(self):
        super(SubDevice, self).__init__()
        self.logger.info("%s - starting",str(os.getpid()))

    def on_getDeviceData(self):
        msg = self.getDeviceData.recv_pyobj() # Receive (timestamp,value)
        self.logger.info("Message: {0} arrived.".format(msg))