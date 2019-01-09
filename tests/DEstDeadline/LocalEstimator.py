#
from riaps.run.comp import Component
import logging
import os

class LocalEstimator(Component):
    def __init__(self):
        super(LocalEstimator, self).__init__()
        self.pid = os.getpid()
        self.pending = 0
        self.logger.info("LocalEstimator")
        
    def on_ready(self):
        msg = self.ready.recv_pyobj()
        self.logger.info("on_ready():%s [%d]" % (msg, self.pid))
        while self.pending > 0:     # Handle the case when there is a pending request
            self.on_query()
        msg = "sensor_query"
        if self.query.send_pyobj(msg):
            self.pending += 1 
    
    def on_query(self):
        msg = self.query.recv_pyobj()
        self.logger.info("on_query():%s" % msg)
        self.pending -= 1
        msg = "local_est(" + str(self.pid) + ")"
        self.estimate.send_pyobj(msg)
    
