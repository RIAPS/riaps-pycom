#
from riaps.run.comp import Component
import logging
import os

class CountSubscriber(Component):
    def __init__(self):
        super(CountSubscriber, self).__init__()
        self.startedSubscription = False

    '''
    Timer starts the Subscriber - depending on the test, the subscriber 
    may come up first or second (after the publisher).  
    This is a one shot timer, so it is deactivated after the subscriber starts.
    '''
    def on_starter(self):
        if not self.startedSubscription:
            msg = self.starter.recv_pyobj()
            self.logger.info("on_starter():%s",msg)
            self.startedSubscription = True
            self.starter.deactivate()
        
    '''
    Receive and log the incoming publisher count once the subscriber is started
    '''
    def on_newCount(self):
        
        if self.startedSubscription:
            msg = self.newCount.recv_pyobj()
            self.logger.info("on_newCount():%s",msg)
 