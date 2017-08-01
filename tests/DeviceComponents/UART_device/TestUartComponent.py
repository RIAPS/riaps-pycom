'''
Created on July 31, 2017

@author: Tim Krentz
'''
from riaps.run.comp import Component
import os


class TestUartComponent(Component):
    def __init__(self):
        super().__init__()
        self.pid = os.getpid()
        self.setValue = 0  # default off
        self.logger.info('TestUartComponent: %s - starting',str(self.pid))
        self.written = 0

    def on_activity(self):
        msg = self.activity.recv_pyobj()
        if self.written == 0:
            self.written = 1
            msg = ('write',str.encode('RIAPS'))
            self.uartReqPort.send_pyobj(msg)
            self.logger.info('on_activity()[%s]: sent read request',str(self.pid))
        else:
            self.written = 0
            msg = ('read',5)
            self.uartReqPort.send_pyobj(msg)
            self.logger.info('on_activity()[%s]: sent read request',str(self.pid))


    def on_uartReqPort(self):
        msg = self.uartReqPort.recv_pyobj()
        self.logger.info('on_uartReqPort()[%s]: got reply : %s ',
                        str(self.pid),repr(msg))
