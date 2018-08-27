#
from riaps.run.comp import Component
import logging
import os
from reqreplib.reqrep import ReqRep

class Replier(Component):
    def __init__(self):
        super(Replier, self).__init__()
        self.pid = os.getpid()
        self.logger.info('call ReqRep')
        self.rr = ReqRep()
        self.logger.info('called ReqRep')

    def on_srvRepPort(self):
        msg = self.srvRepPort.recv_pyobj()
        self.logger.info("[%d] on_srvRepPort():%s" %(self.pid, msg))
        rep = "clt_req: %d" % self.pid
        self.logger.info("[%d] send rep: %s" % (self.pid,rep)) 
        self.srvRepPort.send_pyobj(rep)
        self.rr.rep()

    def __destroy__(self):
        self.logger.info("[%d] destroyed" % self.pid)