# import riaps
from riaps.run.comp import Component
import os
import logging

class Requestor(Component):
    def __init__(self):
        super(Requestor, self).__init__()
        self.pid = os.getpid()

    def on_clock(self):
        now = self.clock.recv_pyobj()   # Receive time.time() as float
        self.logger.info('on_clock(): %s' % str(now))
        msg = "clt_req: %d" % self.pid
        self.logger.info('[%d] send req: %s' % (self.pid,msg))
        self.cltReqPort.send_pyobj(msg)

    def on_cltReqPort(self):
        rep = self.cltReqPort.recv_pyobj()
        self.logger.info('[%d] recv rep: %s' % (self.pid,rep))

    def __destroy__(self):
        self.logger.info("[%d] destroyed" % self.pid)
