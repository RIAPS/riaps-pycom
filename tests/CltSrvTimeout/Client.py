# import riaps
from riaps.run.comp import Component
from riaps.run.exc import PortError

import os
import logging

class Client(Component):
    def __init__(self):
        super(Client, self).__init__()
        self.pid = os.getpid()
        self.pending = 0

    def handleActivate(self):
        self.cltReqPort.set_recv_timeout(1.0)
        self.cltReqPort.set_send_timeout(1.0)
        rto = self.cltReqPort.get_recv_timeout()
        sto = self.cltReqPort.get_send_timeout()
        self.logger.info("handleActivate: (rto,sto) = (%s,%s)" % (str(rto),str(sto)))

    def on_clock(self):
        now = self.clock.recv_pyobj()   # Receive time.time() as float
        self.logger.info('on_clock(): %s' % str(now))

        if self.cltReqPort.connected() == 0:
            self.logger.info('Not yet connected!')
            return

        if self.pending == 0:
            msg = "clt_req: %d" % self.pid
            self.logger.info('[%d] send req: %s' % (self.pid,msg))
            try:
                self.cltReqPort.send_pyobj(msg)
                self.pending += 1
            except PortError as e:
                self.logger.info("on_clock:send exception = %d" % e.errno)
                if e.errno in (PortError.EAGAIN,PortError.EPROTO):
                    self.logger.info("on_clock: resetting socket (send)")
                    self.cltReqPort.reset()
        else:
            try:
                rep = self.cltReqPort.recv_pyobj()
                self.logger.info('[%d] recv rep: %s' % (self.pid,rep))
            except PortError as e:
                rep = None
                self.logger.info("on_clock:recv exception = %d" % e.errno)
                if e.errno in (PortError.EAGAIN,PortError.EPROTO):
                    self.logger.info("on_clock: resetting socket (recv)")
                    self.cltReqPort.reset()
            finally:
                # In either case we decrement the number of pending messages
                self.pending -= 1


    def __destroy__(self):
        self.logger.info("[%d] destroyed" % self.pid)
