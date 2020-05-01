# import riaps
from riaps.run.comp import Component
import logging

class HelloPub(Component):
    def __init__(self):
        super(HelloPub, self).__init__()
        
    def on_clock(self):
        now = self.clock.recv_pyobj()   # Receive time.time() as float
        nowStr = str(now)
        self.logger.info('on_clock(): %s' % nowStr)
        msg = "pub: %s" % nowStr
        self.pubPort.send_pyobj(msg)


