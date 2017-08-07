'''
Created on July 31, 2017

@author: Tim Krentz
'''
from riaps.run.comp import Component
import os


class TestUartComponentA(Component):
    def __init__(self):
        super().__init__()
        self.pid = os.getpid()
        self.setValue = 0  # default off
        self.logger.info('TestUartComponent: %s - starting',str(self.pid))
        self.count = 0

    def on_activity(self):
        msg = self.activity.recv_pyobj()
        self.activity.setPeriod(1.0)

        msg = ('write',str.encode(str(self.count)))
        self.uartReqPort.send_pyobj(msg)
        self.count = self.count + 1

        self.logger.info('on_activity()[%s]: requested to write: %s',
            str(self.pid),repr(msg))


    def on_uartReqPort(self):
        msg = self.uartReqPort.recv_pyobj()
        self.logger.info('on_uartReqPort()[%s]: got reply : %s ',
                        str(self.pid),repr(msg))
