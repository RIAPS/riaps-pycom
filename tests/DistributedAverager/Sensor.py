# import riaps
from riaps.run.comp import Component
import logging
import random

class Sensor(Component):
    def __init__(self,value):
        super(Sensor, self).__init__()
        if value == 0.0:
            self.myValue = (10.0 * random.random()) - 5.0
        else:
            self.myValue = value

    def on_clock(self):
        now = self.clock.recv_pyobj()   # Receive time (as float)
        # self.logger.info('on_clock():%s' % msg)
        msg = (now,self.myValue)        # Send (timestamp,value)
        self.sensorReady.send_pyobj(msg)
