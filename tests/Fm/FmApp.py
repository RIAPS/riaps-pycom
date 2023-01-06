# import riaps
from riaps.run.comp import Component
import logging
from fmlib.Fm import Fm

class FmApp(Fm):
    '''
    Fault management test for application actors
    '''
    def __init__(self,test):
        super(FmApp, self).__init__(test)
        self.logger.info("FmApp('%s')" % test)

        