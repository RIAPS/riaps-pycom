# import riaps
from riaps.run.comp import Component
import logging
import os

class Collector(Component):
    def __init__(self, address):
        super(Collector, self).__init__()
        self.testlogger = logging.getLogger(__name__)
        self.testlogger.setLevel(logging.DEBUG)
        self.fh = logging.FileHandler('/tmp/' + address + '.log')
        self.fh.setLevel(logging.DEBUG)
        self.testlogger.addHandler(self.fh)
        self.messageCounter = 0
        
    def on_getTemperature(self):
        msg = self.getTemperature.recv_pyobj()
        self.testlogger.info("Received messages: %d", msg)

    def on_stopComponent(self):
        self.testlogger.info("Component commits suicide (pid: %d)", os.getpid())
        print("kill %d", os.getpid())
        os.kill(os.getpid(), -9)

    




