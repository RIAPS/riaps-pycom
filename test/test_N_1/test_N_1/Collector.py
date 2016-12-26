# import riaps
from riaps.run.comp import Component
import logging

class Collector(Component):
    def __init__(self):
        super(Collector, self).__init__()
        self.testlogger = logging.getLogger(__name__)
        self.testlogger.setLevel(logging.DEBUG)
        self.fh = logging.FileHandler('/tmp/test_N_1_ActorTestN1s.log')
        self.fh.setLevel(logging.DEBUG)
        self.testlogger.addHandler(self.fh)
        self.messageCounter = 0
        
    def on_getTemperature(self):
        msg = self.getTemperature.recv_pyobj()
        self.testlogger.info("Received messages: %d", msg)

    




