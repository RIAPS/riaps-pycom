#
from riaps.run.comp import Component
import logging
import os
import uuid

from CmpBase import CmpBase


class Cmp4(CmpBase):
    def __init__(self):
        super(Cmp4, self).__init__()
        self.publisherPorts.append("introduce3")
        self.publisherPorts.append("introduce4")

    def on_wakeup(self):
        timerMsg = self.wakeup.recv_pyobj()
        self.introduce()

    def on_update3(self):
        updateMsg = self.update3.recv_pyobj();
        self.on_update_base(updateMsg)
        print("Cmp4 knows " + str(len(self.others)-1) + " members")

    def on_update4(self):
        updateMsg = self.update4.recv_pyobj();
        self.on_update_base(updateMsg)
        print("Cmp4 knows " + str(len(self.others)-1) + " members")