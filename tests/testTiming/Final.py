# import riaps
from riaps.run.comp import Component
import logging


class Final(Component):
    def __init__(self):
        super(Final, self).__init__()
        # self.testlogger = logging.getLogger(__name__)
        # self.testlogger.setLevel(logging.DEBUG)
        # self.fh = logging.FileHandler('/tmp/test_1_N_ActorTest1Ns.log')
        # self.fh.setLevel(logging.DEBUG)
        # self.testlogger.addHandler(self.fh)
        # self.messageCounter = 0

    def on_getArray(self):
        msg = self.getArray.recv_pyobj()
        # self.testlogger.info("Received messages: %d", msg)
        self.returnResults.send_pyobj(msg)
