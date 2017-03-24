# import riaps
from riaps.run.comp import Component
import logging
import random

class SporadicTimer(Component):
    def __init__(self):
        super(SporadicTimer, self).__init__()
        
    def on_sporadic(self):
        now = self.sporadic.recv_pyobj()            # Receive time (as float)
        self.logger.info("on_sporadic() %s",now)
        if self.sporadic.getDelay() == 1.0:         # If delay = 1.0 (i.e. the first firing)
            self.sporadic.setDelay(4.0)             # Change delay to 4.0
            self.sporadic.launch()                  # Launch it again
        
    def on_ticker(self):
        now = self.ticker.recv_pyobj()              # Receive message
        self.logger.info('on_ticker():%s',now)
        if self.sporadic.running():
            self.logger.info("canceling sporadic")
            self.sporadic.cancel()
        self.sporadic.setDelay(1.0)                 # Set the sporadic timer delay 
        self.sporadic.launch()                      # Launch the sproadic timer
        

