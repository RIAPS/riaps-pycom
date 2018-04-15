#
from riaps.run.comp import Component
import logging

class GlobalEstimator(Component):
    def __init__(self):
        super(GlobalEstimator, self).__init__()
        self.logger.info("GlobalEstimator") 

    def on_wakeup(self):
        msg = self.wakeup.recv_pyobj()
        self.logger.info("on_wakeup():%s",msg)
        
    def on_estimate(self):
        msg = self.estimate.recv_pyobj()
        self.logger.info("on_estimate():%s",msg)
    
