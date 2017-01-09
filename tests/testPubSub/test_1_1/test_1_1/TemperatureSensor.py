#
from riaps.run.comp import Component
import logging
import os
import sys

class TemperatureSensor(Component):
    def __init__(self):
        super(TemperatureSensor, self).__init__()
        self.pid = os.getpid()
        self.pending = 0

        self.testlogger = logging.getLogger(__name__)
        self.testlogger.setLevel(logging.DEBUG)
        self.fh = logging.FileHandler('/tmp/test_1_1_ActorTest1p.log')
        self.fh.setLevel(logging.DEBUG)
        self.testlogger.addHandler(self.fh)
        self.messageCounter = 0

    def on_clock(self):
        msg = self.clock.recv_pyobj()
        #self.testlogger.info("[%d] on_clock():%s [%d]", msg, self.pid)
        self.messageCounter += 1
        msg = self.messageCounter
        self.sendTemperature.send_pyobj(msg)
        self.testlogger.info("Sent messages: %d", self.messageCounter)

    def on_stopComponent(self):
        self.testlogger.info("Component commits suicide (pid: %d)", os.getpid())
        print("kill %d", os.getpid())
        os.kill(os.getpid(), -9)

