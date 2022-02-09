# import riaps
from riaps.run.comp import Component
import logging

class Device(Component):
    def __init__(self):
        super(Device, self).__init__()
        
    def on_clock(self):
        now = self.clock.recv_pyobj()   # Receive time.time() as float
        self.logger.info('on_clock(): %s' % str(now))
        
    def handleDeactivate(self):
        self.logger.flush()
        
    def __destroy__(self):
        self.logger.flush()    
    


