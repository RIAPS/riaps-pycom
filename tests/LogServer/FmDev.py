# import riaps
from riaps.run.comp import Component
import logging
from fmlib.Fm import Fm

class FmDev(Fm):
    '''
      Fault management test for system (devices, services, kernel)
    '''
    def __init__(self,test):
        super(FmDev, self).__init__(test)
        self.logger.info("FmDev('%s')" % test)

        