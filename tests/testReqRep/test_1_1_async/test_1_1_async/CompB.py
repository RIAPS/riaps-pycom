#
from riaps.run.comp import Component
import logging
import os
import sys

class CompB(Component):
    def __init__(self, logfile):
        super(CompB, self).__init__()
        logpath = '/tmp/' + logfile
        try:
            os.remove(logpath)
        except OSError:
            pass

        self.testlogger = logging.getLogger(__name__)
        self.testlogger.setLevel(logging.DEBUG)
        self.fh = logging.FileHandler(logpath)
        self.fh.setLevel(logging.DEBUG)
        self.testlogger.addHandler(self.fh)
        self.messageCounter = 0

    def on_sendTemperature(self):
        msg = self.sendTemperature.recv_pyobj()
        self.testlogger.info("Got request: %d", msg)
        self.sendTemperature.send_pyobj(msg)
        self.testlogger.info("Sent response: %d", msg)


