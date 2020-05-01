# import riaps
from riaps.run.comp import Component
import logging

class HelloSub(Component):
    def __init__(self):
        super(HelloSub, self).__init__()
        
    def on_subPort(self):
        msg = self.subPort.recv_pyobj()   # Receive msg
        self.logger.info('on_subPort(): %s' % str(msg))
    


