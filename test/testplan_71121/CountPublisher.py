#
from riaps.run.comp import Component
import logging
import os
import pydevd   # needed for remote debugging
        

class CountPublisher(Component):
    def __init__(self):
        super(CountPublisher, self).__init__()
        self.pid = os.getpid()
        self.PubCounter = 0
        self.startedPublisher = False
        
    '''
    Timer starts the Publisher - depending on the test, the publisher 
    may come up first or second (after the subscriber).  
    This is a one shot timer, so it is deactivated after the publisher starts.
    '''
    def on_starter(self):
        pydevd.settrace('192.168.1.101')  # start point for debugging, must add breakpoint after this point
        if not self.startedPublisher:
            msg = self.starter.recv_pyobj()
            self.logger.info("on_starter():%s",msg)
            self.startedPublisher = True
            self.starter.deactivate()  
            
    '''
    Once the publisher has been started, then send an incrementing count every time the timer fires
    '''
    def on_wakeup(self):
        if self.startedPublisher:
            msg = self.wakeup.recv_pyobj()
            self.logger.info("on_wakeup():%s [%d]", msg, self.pid)
            self.PubCounter += 1
            msg = "PubCount = " + str(self.PubCounter)
            self.newCount.send_pyobj(msg)

    