#
from riaps.run.comp import Component
import logging
import os
import time

class Server(Component):
    def __init__(self):
        super(Server, self).__init__()
        self.pid = os.getpid()
        self.sleep = 0.3
        self.sleepMax = 1.5

    def on_srvRepPort(self):
        msg = self.srvRepPort.recv_pyobj()
        self.logger.info("[%d] on_srvRepPort():%s" %(self.pid, msg))
        rep = "clt_req: %d, sleep = %f" % (self.pid,self.sleep)
        time.sleep(self.sleep)
        self.sleep += 0.3
        if self.sleep > self.sleepMax:
            self.sleep = 0.3
        self.logger.info("[%d] send rep: %s" % (self.pid,rep)) 
        self.srvRepPort.send_pyobj(rep)

    def __destroy__(self):
        self.logger.info("[%d] destroyed" % self.pid)
        