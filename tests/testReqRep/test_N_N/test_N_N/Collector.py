# import riaps
from riaps.run.comp import Component
import logging
import os

class Collector(Component):
    def __init__(self):
        super(Collector, self).__init__()
        self.testlogger = logging.getLogger(__name__)
        self.testlogger.setLevel(logging.DEBUG)
        self.fh = logging.FileHandler('/tmp/test_1_N_ActorTestNreq.log')
        self.fh.setLevel(logging.DEBUG)
        self.testlogger.addHandler(self.fh)
        self.messageCounter = 0
        
    def on_clock(self):
        msg = self.messageCounter
        self.messageCounter+=1

        self.getTemperature.send_pyobj(msg)
        self.testlogger.info("Sent request: %d", msg)
        msg = self.getTemperature.recv_pyobj()
        self.testlogger.info("Got response: %d", msg)

    def on_stopComponent(self):
        self.testlogger.info("Component commits suicide (pid: %d)", os.getpid())
        print("kill %d", os.getpid())
        os.kill(os.getpid(), -9)

    




