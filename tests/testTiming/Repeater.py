#
import signal

from riaps.run.comp import Component
import logging
import os
import sys
from datetime import datetime


content =\
      bytes([0x13, 0x12, 0x11, 0x10, 0x08, 0x00,0x13, 0x00,  0x08, 0x01,
             0x13, 0x12, 0x11, 0x10, 0x08, 0x00, 0x13, 0x00, 0x08, 0x01,
             0x13, 0x12, 0x11, 0x10, 0x08, 0x00, 0x13, 0x00, 0x08, 0x01,
             0x13, 0x12, 0x11, 0x10, 0x08, 0x00, 0x13, 0x00, 0x08, 0x01,
             0x13, 0x12, 0x11, 0x10, 0x08, 0x00, 0x13, 0x00, 0x08, 0x01,
             0x13, 0x12, 0x11, 0x10, 0x08, 0x00, 0x13, 0x00, 0x08, 0x01,
             0x13, 0x12, 0x11, 0x10, 0x08, 0x00, 0x13, 0x00, 0x08, 0x01,
             0x13, 0x12, 0x11, 0x10, 0x08, 0x00, 0x13, 0x00, 0x08, 0x01,
             0x13, 0x12, 0x11, 0x10, 0x08, 0x00, 0x13, 0x00, 0x08, 0x01,
             0x13, 0x12, 0x11, 0x10, 0x08, 0x00, 0x13, 0x00, 0x08, 0x01])

class Repeater(Component):
    def __init__(self):
        super(Repeater, self).__init__()
        #self.testlogger = logging.getLogger(__name__)
        #self.testlogger.setLevel(logging.DEBUG)
        #self.fh = logging.FileHandler('/tmp/test_1_N_ActorTest1Np.log')
        #self.fh.setLevel(logging.DEBUG)
        #self.testlogger.addHandler(self.fh)
        self.messageCounter = 0
        self.log = ""

    def on_clock(self):
        msg = self.clock.recv_pyobj()
        #self.testlogger.info("[%d] on_clock():%s [%d]", msg, self.pid)

        messageToSend = {"messageCounter": 0, "body": bytes([])}
        messageToSend["messageCounter"] = self.messageCounter
        messageToSend["body"] = content
                      


        self.sendArray.send_pyobj(msg)
        self.log += str(datetime.now()) + " " + str(self.messageCounter) + " sent\n"

        self.messageCounter += 1
        
        if self.messageCounter%10==0:
            print(self.log)
            self.log=""


    def on_getResults(self):
        msg = self.getResults.recv_pyobj()
        self.log += str(datetime.now()) + " " + str(msg["messageCounter"]) + " arrived\n"


        #self.testlogger.info("Sent messages: %d", self.messageCounter)
        #if self.messageCounter == 15:
        #    print("kill %d", os.getpid())
        #    os.kill(os.getpid(), signal.SIGTERM)
