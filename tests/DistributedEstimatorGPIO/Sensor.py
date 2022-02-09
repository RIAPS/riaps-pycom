# import riaps
from riaps.run.comp import Component
import logging

class Sensor(Component):
    def __init__(self,rate):
        super(Sensor, self).__init__()
        self.rate = rate
        self.count = 0
        
    def on_clock(self):
        now = self.clock.recv_pyobj()   # Receive time.time() as float
        # self.logger.info('on_clock(): %s' % str(now))
        self.count += 1
        if self.count == self.rate:
            msg = "rdy"
            self.ready.send_pyobj(msg)
            self.count = 0
    
    def on_request(self):
        req = self.request.recv_pyobj()
        # self.logger.info("on_request():%s" % req)
        rep = "val"
        self.request.send_pyobj(rep)



