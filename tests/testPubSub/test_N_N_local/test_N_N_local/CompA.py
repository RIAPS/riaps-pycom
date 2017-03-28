#
from riaps.run.comp import Component
import logging
import os
import sys
import datetime

class CompA(Component):
    def __init__(self, logfile):
        super(CompA, self).__init__()

        logpath = '/tmp/CompA_' + logfile
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
        self.messageCounter1 = 0
        self.messageCounter2 = 0

        now = datetime.datetime.now()
        self.testlogger.info("CompA is started at %s", now.strftime("%H:%M"))

    def on_clock(self):
        msg = self.clock.recv_pyobj()
        self.messageCounter1 += 1
        self.messageCounter2 += 1

        msg1 = 'topic1_' + str(self.messageCounter1)
        msg2 = 'topic2_' + str(self.messageCounter2)

        self.sendTopic1.send_pyobj(msg1)
        self.sendTopic2.send_pyobj(msg2)


        self.testlogger.info("Sent messages: %s", msg1)
        self.testlogger.info("Sent messages: %s", msg2)


