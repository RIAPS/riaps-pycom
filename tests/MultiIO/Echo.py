# 
# Trivial echo server
# 
from riaps.run.comp import Component
import logging
import time
import os

class Echo(Component):
    def __init__(self):
        super(Echo, self).__init__()
        self.logger.info("Echo - starting")

    def on_echo(self):
        (ident,msg) = self.echo.recv_pyobj()    # Receive src_id, string
        msg = str(msg)[::-1]            # Reverse it
        self.echo.send_pyobj((ident,msg))       # Send it back (with src_id)

    def on_clock(self):
        msg = self.clock.recv_pyobj()      # Receive time stamp 
        self.logger.info("on_clock():%s" % str(msg))   
