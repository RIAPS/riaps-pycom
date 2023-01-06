# import riaps
from riaps.run.comp import Component
import logging

class Ping(Component):
    def __init__(self):
        super(Ping, self).__init__()
        self.logger.info("Ping()")
        
    def on_tick(self):
        now = self.tick.recv_pyobj()   # Receive time.time() as float
        self.logger.info('on_tick(): %s' % str(now))
        msg = "ping"
        self.ping.send_pyobj(msg)



