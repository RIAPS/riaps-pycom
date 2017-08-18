'''
Created on Aug 2, 2017

@author: Tim Krentz
'''
from riaps.run.comp import Component
import os
import threading


class TestUartComponentB(Component):
    def __init__(self):
        super().__init__()
        self.pid = os.getpid()
        self.setValue = 0  # default off
        self.logger.info('TestUartComponent: %s - starting',str(self.pid))
        self.protectReq = threading.Event()
        self.protectReq.set()
        self.protectRead = threading.Event()
        self.protectRead.set()
        self.closeState = 0

    def on_activity(self):
        msg = self.activity.recv_pyobj()
        self.activity.setPeriod(1.0)

        if self.protectReq.isSet() and self.protectRead.isSet():
            self.protectReq.clear()
            self.protectRead.clear()
            msg = ('read',10)
            self.uartReqPort.send_pyobj(msg)

            self.logger.info('on_activity()[%s]: requested to read: %s',
                str(self.pid),repr(msg))

    def on_uartReqPort(self):
        msg = self.uartReqPort.recv_pyobj()
        self.logger.info('on_uartReqPort()[%s]: got reply : %s ',
                        str(self.pid),repr(msg))
        self.protectReq.set()

    def on_uartReadSub(self):
        msg = self.uartReadSub.recv_pyobj()
        self.logger.info('on_uartReadSub()[%s]: got bytes : %s ',
                        str(self.pid),repr(msg))
        self.protectRead.set()
