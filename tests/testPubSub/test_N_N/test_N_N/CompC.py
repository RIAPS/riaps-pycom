#
from riaps.run.comp import Component
import logging
import os
import sys
import datetime

class CompC(Component):
    def __init__(self, logfile):
        super(CompC, self).__init__()

        logpath = '/tmp/CompC_' + logfile
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
        self.messageCounter3 = 0

        now = datetime.datetime.now()
        self.testlogger.info("CompC is started at %s", now.strftime("%H:%M"))

    def on_clock(self):
        msg = self.clock.recv_pyobj()
        self.messageCounter3 += 1

        msg3 = 'topic3_' + str(self.messageCounter3)
        self.sendTopic3.send_pyobj(msg3)

        self.testlogger.info("Sent message: %s", msg3)

    def on_getTopic1(self):
        msg = self.getTopic1.recv_pyobj()
        self.testlogger.info("Received message: %s", msg)


