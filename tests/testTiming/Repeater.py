#
import signal

from riaps.run.comp import Component
import logging
import os
import sys
import time
from Message import message


content = bytearray(
            [0x13, 0x12, 0x11, 0x10, 0x08, 0x00,0x13, 0x00,  0x08, 0x01,
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
        self.messageCounter = 0
        self.sendLog = ""
        self.receiveLog = ""
        

    def on_clock(self):
        msg = self.clock.recv_pyobj()
        #self.testlogger.info("[%d] on_clock():%s [%d]", msg, self.pid)

        m = message()
        m.messageCounter = self.messageCounter
        m.body = content

        self.sendArray.send_pyobj(m)
        #self.sendLog += "=> " + str(datetime.now()) + " " + str(self.messageCounter) + " sent\n"
        self.sendLog += "=> " + str(time.perf_counter()) + " " + str(self.messageCounter) + " sent\n"


        self.messageCounter += 1
        
        if self.messageCounter%2000==0:
            print(self.sendLog)
            print("-----")
            print(self.receiveLog)
            self.sendLog=""
            self.receiveLog = ""


    def on_getResults(self):
        mmm = self.getResults.recv_pyobj()
        #self.receiveLog += "<= " +str(datetime.now()) + " " + str(mmm.messageCounter) + " arrived\n"
        self.receiveLog += "<= " +str(time.perf_counter()) + " " + str(mmm.messageCounter) + " arrived\n"
