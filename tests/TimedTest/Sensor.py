# import riaps
from riaps.run.comp import Component
import logging

class Sensor(Component):
    def __init__(self):
        super(Sensor, self).__init__()
        
    def on_clock(self):
        now = self.clock.recv_pyobj()   # Receive time.time() as float
        self.logger.info('on_clock(): %s' % str(now))
        msg = "sensor_ready"
        self.ready.send_pyobj(msg)
    
    def on_request(self):
        req = self.request.recv_pyobj()
        self.logger.info("on_request():%s" % req)
        sendTime = self.request.get_sendTime()
        recvTime = self.request.get_recvTime()
        self.logger.info("SensorQuery recv'd @ %f, sent @ %f, diff = %f" 
                         % (sendTime,recvTime,recvTime-sendTime))
        rep = "sensor_rep"
        self.request.send_pyobj(rep)



