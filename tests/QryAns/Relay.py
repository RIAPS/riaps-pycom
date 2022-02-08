# import riaps
from riaps.run.comp import Component
import logging
import os
import time

class Relay(Component):
    def __init__(self):
        super(Relay, self).__init__()
        self.pid = os.getpid()
        
    def on_subPort(self):
        msg = self.subPort.recv_pyobj()   
        self.logger.info('on_subPort(): %r' % msg)
        if msg < 0: return
        msg = -(msg + 1)
        time.sleep(0.1)
        self.pubPort.send_pyobj(msg)
        
        
    


