# import riaps
from riaps.run.comp import Component
import logging
from Message import message
from datetime import datetime


class Final(Component):
    def __init__(self):
        super(Final, self).__init__()
        

    def on_getArray(self):
        msg = self.getArray.recv_pyobj()
        print("Got message, forward it ")
        
         
        newMsg = message()
        newMsg.messageCounter = msg.messageCounter
        newMsg.body = bytearray([])
        
        
        for value in msg.body:
            newMsg.body.append(value*2)
        
        self.returnResults.send_pyobj(newMsg)
        
