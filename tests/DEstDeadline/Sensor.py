# import riaps
from riaps.run.comp import Component
import logging

class Sensor(Component):
    def __init__(self):
        super(Sensor, self).__init__()
        self.limit = 1000 # min, max ~ 215000
        
    def on_clock(self):
        now = self.clock.recv_pyobj()   # Receive time.time() as float
        self.logger.info('on_clock(): %s',str(now))
        msg = "data_ready"
        self.ready.send_pyobj(msg)
        self.limit += 1000      # Increase limit, do more cycles
        "-".join(str(n) for n in range(self.limit))   
    
    def on_request(self):
        req = self.request.recv_pyobj()
        self.logger.info("on_request():%s", req)
        rep = "sensor_rep"
        self.request.send_pyobj(rep)

    def handleDeadline(self,funcName):
        self.logger.info("handleDeadline(): %s" % funcName)
        self.limit = 1000 
        

