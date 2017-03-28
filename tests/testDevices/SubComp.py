#
from riaps.run.comp import Component
import logging
import uuid
import time
import os

class SubComp(Component):
    def __init__(self):
        super(SubComp, self).__init__()
        self.logger.info("%s - starting",str(os.getpid()))

    def on_getComponentData(self):
        msg = self.getComponentData.recv_pyobj() # Receive (timestamp,value)

        self.sendDeviceData.send_pyobj(msg)