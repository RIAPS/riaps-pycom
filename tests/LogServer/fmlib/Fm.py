# import riaps
from riaps.run.comp import Component
import logging
import fmlib.faults

class Fm(Component):
    '''
    '''
    def __init__(self,test):
        super(Fm, self).__init__()
        self.logger.info("FM('%s')" % test)
        self.test = test
        self.fault = False                    # Set if deplo killed
        
    def on_timeout(self):
        now = self.timeout.recv_pyobj()       # Receive time.time() as float
        self.logger.info("fault: %s" % self.test)
        if self.fault: return                       # Deplo killed, do nothing
        if self.test == 'e':                        # Actor exit
            fmlib.faults.exit()
        elif self.test == 'a':                      # Actor crash
            fmlib.faults.crash()
        elif self.test == 'd':                      # Deplo crash
            fmlib.faults.kill('riaps_deplo')
            self.fault = True                       
        elif self.test == 'i':                      # Disco crash
            fmlib.faults.kill('riaps_disco')
        elif self.test == 's':                      # Deplo+disco crash
            fmlib.faults.kill('"(riaps_deplo|riaps_disco)"')
            self.fault = True
        elif self.test == 'k':                      # Kernel panic
            fmlib.faults.panic()
        elif self.test == 'r':
            fmlib.faults.reboot()
        else:
            self.logger.info("ok")
            
    def on_ping(self):
        now = self.ping.recv_pyobj() 
        self.logger.info("ping")
        