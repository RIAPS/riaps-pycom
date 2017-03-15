#
from riaps.run.comp import Component
import logging
import os
import uuid

from CmpBase import CmpBase


class Cmp1(CmpBase):
    def __init__(self):
        super(Cmp1, self).__init__()
        self.publisherPorts.append("introduce1")

    def on_wakeup(self):
        timerMsg = self.wakeup.recv_pyobj()
        self.introduce()

    def on_update1(self):
        updateMsg = self.update1.recv_pyobj();
        self.on_update_base(updateMsg)
        print("Cmp1 knows " + str(len(self.others)-1) + " members")

    