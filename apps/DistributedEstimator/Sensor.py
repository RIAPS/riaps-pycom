# import riaps
from riaps.run.comp import Component
import logging

class Sensor(Component):
    def __init__(self):
        super(Sensor, self).__init__()
        
    def on_clock(self):
        msg = self.clock.recv_pyobj()
        self.logger.info('on_clock():%s',msg)
        msg = "data_ready"
        self.ready.send_pyobj(msg)
    
    def on_request(self):
        req = self.request.recv_pyobj()
        self.logger.info("on_request():%s", req)
        rep = "sensor_rep"
        self.request.send_pyobj(rep)



