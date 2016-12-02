# import riaps
from riaps.run.comp import Component
import logging

class Measurer(Component):
    def __init__(self):
        super(Measurer, self).__init__()
        
    def on_clock(self):
        msg = self.clock.recv_pyobj()
        self.logger.info('on_clock():%s',msg)
        msg = "data_ready" # Should be a real message: (timestamp,value) 
        self.sensorReady.send_pyobj(msg)

