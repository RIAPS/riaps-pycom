# import riaps
from riaps.run.comp import Component
import logging
import os
import time

class Collector(Component):
    def __init__(self, address):
        super(Collector, self).__init__()

        logfile = '/tmp/' + address + '.log'
        try:
            os.remove(logfile)
        except OSError:
            pass

        self.testlogger = logging.getLogger(__name__)
        self.testlogger.setLevel(logging.DEBUG)
        self.fh = logging.FileHandler(logfile)
        self.fh.setLevel(logging.DEBUG)
        self.testlogger.addHandler(self.fh)
        self.messageCounter = 0
        
    def on_getTemperature(self):
        msg = self.getTemperature.recv_pyobj()
        self.testlogger.info("[%f] <= %d", time.time(), msg)

    def on_stopComponent(self):
        self.testlogger.info("Component commits suicide (pid: %d)", os.getpid())
        #print("kill %d", os.getpid())
        #os.kill(os.getpid(), -9)

