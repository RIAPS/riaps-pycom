# import riaps
from riaps.run.comp import Component
import logging
import os

class CompA(Component):
    def __init__(self, logfile):
        super(CompA, self).__init__()
        logpath = '/tmp/' + logfile
        try:
            os.remove(logpath)
        except OSError:
            pass

        self.testlogger = logging.getLogger(__name__)
        self.testlogger.setLevel(logging.DEBUG)
        self.fh = logging.FileHandler(logpath)
        self.fh.setLevel(logging.DEBUG)
        self.testlogger.addHandler(self.fh)
        self.messageCounter = 0
        self.pendingRequest = 0
        
    def on_clock(self):
        if self.pendingRequest == 0:
            self.pendingRequest+=1
            msg = self.messageCounter
            self.messageCounter+=1

            self.getTemperature.send_pyobj(msg)
            self.testlogger.info("Sent request: %d", msg)

    def on_getTemperature(self):
        self.pendingRequest-=1
        msg = self.getTemperature.recv_pyobj()
        self.testlogger.info("Got response: %d", msg)
    




