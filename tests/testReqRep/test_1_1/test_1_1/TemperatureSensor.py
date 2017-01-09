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
        self.fh = logging.FileHandler('/tmp/test_1_1_ActorTest1rep.log')
        self.fh.setLevel(logging.DEBUG)
        self.testlogger.addHandler(self.fh)

    def on_sendTemperature(self):
        msg = self.sendTemperature.recv_pyobj()
        self.testlogger.info("Got request: %d", msg)
        self.sendTemperature.send_pyobj(msg)
        self.testlogger.info("Sent response: %d", msg)

    def on_stopComponent(self):
        self.testlogger.info("Component commits suicide (pid: %d)", os.getpid())
        print("kill %d", os.getpid())
        os.kill(os.getpid(), -9)

