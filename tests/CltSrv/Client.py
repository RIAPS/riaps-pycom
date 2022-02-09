# import riaps
from riaps.run.comp import Component
import os
import logging

class Client(Component):
    def __init__(self):
        super(Client, self).__init__()
        self.pid = os.getpid()
        self.pending = 0

    def on_clock(self):
        now = self.clock.recv_pyobj()   # Receive time.time() as float
        self.logger.info('on_clock(): %s' % str(now))

        if self.cltReqPort.connected() == 0:
            self.logger.info('Not yet connected!')
            return

        if self.pending == 0:
            msg = "clt_req: %d" % self.pid
            try:
                self.logger.info('[%d] send req: %s' % (self.pid,msg))
                self.cltReqPort.send_pyobj(msg)
                self.pending += 1
            except PortError:
                self.logger.info('Failed %d %d' % msg)
        else:
            # self.pending != 0 implies that we already sent a message -> try to read response
            try:
                rep = self.cltReqPort.recv_pyobj()
                self.logger.info('[%d] recv rep: %s' % (self.pid,rep))
            except PortError:
                # The first message sent is probably lost, and thus the above read failed
                self.logger.info('Failed (PortError)')
            finally:
                # In either case we decrement the number of pending messages
                self.pending -= 1

    def __destroy__(self):
        self.logger.info("[%d] destroyed" % self.pid)
