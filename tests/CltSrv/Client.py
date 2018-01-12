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
        self.logger.info('on_clock(): %s',str(now))
        msg = "clt_req: %d" % self.pid
        if self.pending == 0:
            self.logger.info('[%d] send req: %s' % (self.pid,msg))
            if self.cltReqPort.send_pyobj(msg):
                self.pending += 1
        else:
            rep = self.cltReqPort.recv_pyobj()
            self.pending -= 1
            self.logger.info('[%d] recv rep: %s' % (self.pid,rep))

    def __destroy__(self):
        self.logger.info("[%d] destroyed" % self.pid)

