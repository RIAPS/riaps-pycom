# import riaps
from riaps.run.comp import Component
import logging

class Groupie(Component):
    def __init__(self):
        super(Groupie, self).__init__()
        
    def on_clock(self):
        now = self.clock.recv_pyobj()   # Receive time.time() as float
        self.logger.info('on_clock(): %s' % str(now))
    


