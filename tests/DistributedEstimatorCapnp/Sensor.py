# import riaps
from riaps.run.comp import Component
import capnp
import distributedestimator_capnp
import logging

class Sensor(Component):
    def __init__(self):
        super(Sensor, self).__init__()
        
    def on_clock(self):
        now = self.clock.recv_pyobj()   # Receive time.time() as float
        self.logger.info('on_clock(): %s' % str(now))

        msg = distributedestimator_capnp.SensorReady.new_message()
        msg.msg = "data_ready"
        msgBytes = msg.to_bytes()
        self.ready.send(msgBytes)
        #msg = "data_ready"
        #self.ready.send_pyobj(msg)
    
    def on_request(self):
        # one more abstraction would be useful
        # the developers should get the capnp object and shouldnt
        # deal with the deserializing
        bytes = self.request.recv()
        req = distributedestimator_capnp.SensorQuery.from_bytes(bytes)


        #req = self.request.recv_pyobj()
        self.logger.info("on_request():%s" % req.msg)

        rep = distributedestimator_capnp.SensorValue.new_message()
        rep.msg = "sensor_rep"
        repBytes = rep.to_bytes()
        self.request.send(repBytes)
        #rep = "sensor_rep"
        #self.request.send_pyobj(rep)



