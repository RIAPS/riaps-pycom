# import riaps
from riaps.run.comp import Component
import os
import logging
from reqreplib.reqrep import ReqRep

class Requestor(Component):
    def __init__(self):
        super(Requestor, self).__init__()
        self.pid = os.getpid()
        self.logger.info("LD_LIBRARY_PATH=%s" % (os.getenv("LD_LIBRARY_PATH") or ""))
        self.logger.info('call ReqRep')
        self.rr = ReqRep()
        self.logger.info('called ReqRep')

    def on_clock(self):
        now = self.clock.recv_pyobj()   # Receive time.time() as float
        self.logger.info('on_clock(): %s' % str(now))

        if self.cltReqPort.connected() == 0:
            self.logger.info('Not yet connected!')
            return

        msg = "clt_req: %d" % self.pid
        self.logger.info('[%d] send req: %s' % (self.pid,msg))
        self.cltReqPort.send_pyobj(msg)
        self.rr.req()

    def on_cltReqPort(self):
        rep = self.cltReqPort.recv_pyobj()
        self.logger.info('[%d] recv rep: %s' % (self.pid,rep))

    def __destroy__(self):
        self.logger.info("[%d] destroyed" % self.pid)
