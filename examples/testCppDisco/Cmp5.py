#
from riaps.run.comp import Component
import logging
import os
import uuid

from CmpBase import CmpBase


class Cmp5(CmpBase):
    def __init__(self):
        super(Cmp5, self).__init__()
        self.publisherPorts.append("introduce4")

    def on_wakeup(self):
        timerMsg = self.wakeup.recv_pyobj()
        self.introduce()

    def on_update4(self):
        updateMsg = self.update4.recv_pyobj();
        self.on_update_base(updateMsg)
        print("Cmp5 knows " + str(len(self.others)-1) + " members")

    