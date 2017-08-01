'''
Created on July 27, 2017

@author: Tim Krentz
'''
from riaps.run.comp import Component
import os


class ToggleGpioComponent(Component):
    def __init__(self):
        super().__init__()
        self.pid = os.getpid()
        self.setValue = 0  # default off
        self.logger.info("ToggleGpioComponent: %s - starting",str(self.pid))
        self.waiting = 0

    def on_toggle(self):
        msg = self.toggle.recv_pyobj()
        self.toggle.setPeriod(1.0)
        if self.waiting == 0:
            self.waiting = 1
            # self.logger.info("on_toggle()[%s]: %s",str(self.pid),repr(msg))
            if self.setValue == 0:
                self.setValue = 1
            else:
                self.setValue = 0
            msg = ('write',self.setValue)
            self.logger.info("on_toggle()[%s]: SEND write request, setValue=%d",
                            str(self.pid), self.setValue)
            self.gpioReqPort.send_pyobj(msg)
            self.logger.info("on_toggle()[%s]: DONE write request, setValue=%d",
                            str(self.pid), self.setValue)

    def on_readValue(self):
        msg = self.readValue.recv_pyobj()
        if self.waiting == 0:
            self.waiting = 1
            self.logger.info("on_readValue()[%s]: %s",str(self.pid),repr(msg))
            msg = ('read',0)
            self.gpioReqPort.send_pyobj(msg)

    def on_gpioReqPort(self):
        msg = self.gpioReqPort.recv_pyobj()
        self.logger.info("on_gpioReqPort()[%s]: got reply : %s ",
                        str(self.pid),repr(msg))
        self.waiting = 0
