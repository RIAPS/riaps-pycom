#
from riaps.run.comp import Component
import logging
import os
import time

class Answer(Component):
    def __init__(self):
        super(Answer, self).__init__()
        self.pid = os.getpid()
        self.logger.info("__init__(%s)" % str(id(self)))

    def on_srvAnsPort(self):
        msg = self.srvAnsPort.recv_pyobj()
        ident = self.srvAnsPort.get_identity()
        self.logger.info("[%d] on_srvAnsPort():%r @ %s" %(self.pid, msg, str(ident)))
        # sendTime = self.srvAnsPort.get_sendTime()
        # recvTime = self.srvAnsPort.get_recvTime()
        #self.logger.info("QryReq recv'd @ %f, sent @ %f, diff = %f" 
        #                % (recvTime,sendTime,recvTime-sendTime))
        time.sleep(0.5)
        rep = -msg # "clt_qry: %d" % self.pid
        self.logger.info("[%d] send ans: %r" % (self.pid,rep)) 
        self.srvAnsPort.send_pyobj(rep)
    
    def __destroy__(self):
        self.logger.info("[%d] destroyed" % self.pid)