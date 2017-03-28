#
from riaps.run.comp import Component
import logging
import os
import sys
import datetime

class CompB(Component):
    def __init__(self, logfile):
        super(CompB, self).__init__()

        logpath = '/tmp/CompB_' + logfile
        try:
            os.remove(logpath)
        except OSError:
            pass

        self.pid = os.getpid()
        self.pending = 0

        self.testlogger = logging.getLogger(__name__)
        self.testlogger.setLevel(logging.DEBUG)
        self.fh = logging.FileHandler(logpath)
        self.fh.setLevel(logging.DEBUG)
        self.testlogger.addHandler(self.fh)

        now = datetime.datetime.now()
        self.testlogger.info("CompB is started at %s", now.strftime("%H:%M"))

    def on_getTopic2(self):
        msg = self.getTopic2.recv_pyobj()
        self.testlogger.info("Received message: %s", msg)

    def on_getTopic3(self):
        msg = self.getTopic3.recv_pyobj()
        self.testlogger.info("Received message: %s", msg)


