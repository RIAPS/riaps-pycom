# import riaps
from riaps.run.comp import Component
import os
import logging
import time

class Query(Component):
    def __init__(self,cnt=1):
        super(Query, self).__init__()
        self.pid = None
        self.cnt = cnt
        self.logger.info("__init__(%s)" % str(id(self)))

    def on_clock(self):
        if self.pid == None:
            self.pid = os.getpid()
        now = self.clock.recv_pyobj()   # Receive time.time() as float
        self.logger.info('on_clock(): %s' % str(now))

        if self.cltQryPort.connected() == 0:
            self.logger.info('Not yet connected!')
            return

        msg = self.cnt # "clt_qry:%d" % self.pid
        self.logger.info('[%d] send qry[R]: %r' % (self.pid,msg))
        self.cltQryPort.send_pyobj(msg)
        self.cnt += 1

    def on_cltQryPort(self):
        rep = self.cltQryPort.recv_pyobj()
        self.logger.info('[%d] recv rep: %r' % (self.pid,rep))
        if rep > 0:
            self.logger.info('[%d] handshake complete %r' % (self.pid,rep))
            return
        # sendTime = self.cltQryPort.get_sendTime()
        # recvTime = self.cltQryPort.get_recvTime()
        # self.logger.info("AnsRep recv'd @ %f, sent @ %f, diff = %f"
        #                 % (recvTime,sendTime,recvTime-sendTime))
        msg = rep
        self.logger.info('[%d] send qry[W]: %r' % (self.pid,msg))
        self.cltQryPort.send_pyobj(msg)
        msg = msg * -1000
        self.logger.info('[%d] pub: %r' % (self.pid,msg))
        self.pubPort.send_pyobj(msg)

    def on_subPort(self):
        msg = self.subPort.recv_pyobj()
        self.logger.info('on_subPort(): %s' % str(msg))

    def __destroy__(self):
        self.logger.info("[%d] destroyed" % self.pid)
