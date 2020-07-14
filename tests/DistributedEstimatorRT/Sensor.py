# import riaps
from riaps.run.comp import Component
import logging
import threading
import prctl

class Sensor(Component):
    def __init__(self):
        super(Sensor, self).__init__()
        
    def handleActivate(self):
        flag = prctl.cap_permitted.sys_nice
        self.logger.info("Sensor.sys_nice = %s" % str(flag))

    def on_clock(self):
        now = self.clock.recv_pyobj()   # Receive time.time() as float
        self.logger.info('on_clock(): %s' % str(now))
        msg = "data_ready"
        self.ready.send_pyobj(msg)
    
    def on_request(self):
        req = self.request.recv_pyobj()
        self.logger.info("on_request():%s" % req)
        rep = "sensor_rep"
        self.request.send_pyobj(rep)


