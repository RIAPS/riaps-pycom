#
from riaps.run.comp import Component
import logging
import os
import uuid

from CmpBase import CmpBase


class Cmp2(CmpBase):
    def __init__(self):
        super(Cmp2, self).__init__()
        self.publisherPorts.append("introduce1")
        self.publisherPorts.append("introduce2")

    def on_wakeup(self):
        timerMsg = self.wakeup.recv_pyobj()
        self.introduce()

    def on_update1(self):
        updateMsg = self.update1.recv_pyobj();
        self.on_update_base(updateMsg)
        print("Cmp2 knows " + str(len(self.others)-1) + " members")

    def on_update2(self):
        updateMsg = self.update2.recv_pyobj();
        self.on_update_base(updateMsg)
        print("Cmp2 knows " + str(len(self.others)-1) + " members")
