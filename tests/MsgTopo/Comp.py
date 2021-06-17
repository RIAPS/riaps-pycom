# 
# MsgTopo component 
# 
from riaps.run.comp import Component
import logging
import time
import os

class Comp(Component):
    def __init__(self,name):
        super(Comp, self).__init__()
        self.name = name
        self.logger.info("Comp.%s - starting" % name)
   
    def send(self,where,stamp):
        msg = "Comp.%s.%s ! %r" % (self.name,where,stamp)
        port = getattr(self, where, None)
        if port:
            self.logger.info('%s' % msg)
            port.send_pyobj(msg)
        else:
            pass
        
    def on_clock(self):
        stamp = self.clock.recv_pyobj()      # Receive time stamp 
        self.logger.info("on_clock():%f" % stamp)
        for scope in ['global','local','internal']:
            for port in ['Pub', 'Qry']:
                self.send('%s%s' % (scope,port),stamp)
    
    def recv(self,scope,port,rep=False):
        where = '%s%s' % (scope, port)
        port = getattr(self,where,None)
        if port:
            msg = port.recv_pyobj()
            self.logger.info("Comp.%s.%s ? [%s]" % (self.name, where,msg))
            if rep:
                self.send('%s%s'% (scope,rep),'[%s]' % msg)
        else:
            self.logger.error('Comp.%s %s: ???' % (self.name,where))
            
    def on_globalSub(self):
        self.recv('global','Sub')
        
    def on_globalQry(self):
        self.recv('global','Qry')

    def on_globalAns(self):
        self.recv('global','Ans', 'Ans')
                
    def on_localSub(self):
        self.recv('local','Sub')
        
    def on_localQry(self):
        self.recv('local','Qry')
    
    def on_localAns(self):
        self.recv('local','Ans', 'Ans')        
    
    def on_internalSub(self):
        self.recv('internal','Sub')

    def on_internalQry(self):
        self.recv('internal','Qry')
    
    def on_internalAns(self):
        self.recv('internal','Ans', 'Ans')
        
       