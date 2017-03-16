# import riaps
from riaps.run.comp import Component
import logging
import random

class PeriodicTimer(Component):
    def __init__(self):
        super(PeriodicTimer, self).__init__()
        
    def on_periodic(self):
        now = self.periodic.recv_pyobj()                # Receive time (as float)
        self.logger.info('on_periodic():%s',now)
        period = self.periodic.getPeriod()              # Query the period
        if period == 5.0:
            period = period - 1.0
            self.periodic.setPeriod(period)             # Set the period
            self.logger.info('setting period to %f',period)
        msg = now
        self.ticker.send_pyobj(msg)

