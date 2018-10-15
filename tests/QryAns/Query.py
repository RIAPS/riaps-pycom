# import riaps
from riaps.run.comp import Component
import os
import logging

class Query(Component):
    def __init__(self):
        super(Query, self).__init__()
        self.pid = os.getpid()
        
    def on_clock(self):
        now = self.clock.recv_pyobj()   # Receive time.time() as float
        self.logger.info('on_clock(): %s',str(now))
        msg = "clt_qry:%d" % self.pid
        self.logger.info('[%d] send qry: %s' % (self.pid,msg))
        self.cltQryPort.send_pyobj(msg)
    
    def on_cltQryPort(self):
        rep = self.cltQryPort.recv_pyobj()
        self.logger.info('[%d] recv rep: %s' % (self.pid,rep))
        sendTime = self.cltQryPort.get_sendTime()
        recvTime = self.cltQryPort.get_recvTime()
        self.logger.info("AnsRep recv'd @ %f, sent @ %f, diff = %f" 
                         % (recvTime,sendTime,recvTime-sendTime))

    def __destroy__(self):
        self.logger.info("[%d] destroyed" % self.pid)

