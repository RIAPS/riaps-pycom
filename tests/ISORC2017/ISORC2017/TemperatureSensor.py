#
from riaps.run.comp import Component
import logging
import os
import sys
import time

class TemperatureSensor(Component):
    def __init__(self, address):
        super(TemperatureSensor, self).__init__()

        logfile = '/tmp/' + address + '.log'
        try:
            os.remove(logfile)
        except OSError:
            pass

        self.pid = os.getpid()
        self.pending = 0

        self.testlogger = logging.getLogger(__name__)
        self.testlogger.setLevel(logging.DEBUG)
        self.fh = logging.FileHandler(logfile)
        self.fh.setLevel(logging.DEBUG)
        self.testlogger.addHandler(self.fh)
        self.messageCounter = 0

    def on_clock(self):
        msg = self.clock.recv_pyobj()
        #self.testlogger.info("[%d] on_clock():%s [%d]", msg, self.pid)
        self.messageCounter += 1
        msg = self.messageCounter
        self.sendTemperature.send_pyobj(msg)
        self.testlogger.info("[%f] => %d", time.time(), self.messageCounter)

    def on_stopComponent(self):
        self.testlogger.info("Component commits suicide (pid: %d)", os.getpid())
        #print("kill %d", os.getpid())
        #os.kill(os.getpid(), -9)
        #os.kill(os.getpid(), -9)

