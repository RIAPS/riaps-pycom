#
from riaps.run.comp import Component
import logging
import os

class Answer(Component):
    def __init__(self):
        super(Server, self).__init__()
        self.pid = os.getpid()

    def on_srvAnsPort(self):
        msg = self.srvAnsPort.recv_pyobj()
        self.logger.info("[%d] on_srvAnsPort():%s" %(self.pid, msg))
        rep = "clt_qry: %d" % self.pid
        self.logger.info("[%d] send ans: %s" % (self.pid,rep)) 
        self.srvAnsPort.send_pyobj(rep)

    def __destroy__(self):
        self.logger.info("[%d] destroyed" % self.pid)