# import riaps
from riaps.run.comp import Component
import logging
from Message import message
from datetime import datetime

class Forwarder(Component):
    def __init__(self):
        super(Forwarder, self).__init__()
        self.log=""
        
    def on_getArray(self):
        msg = self.getArray.recv_pyobj()
         
        newMsg = message()
        newMsg.messageCounter = msg.messageCounter
        newMsg.body = bytearray([])
        
        #self.log += "<= " +str(datetime.now()) + " " + str(msg.messageCounter) + " arrived\n"
        if msg.messageCounter%1000==0:
            print("1000. message")
        
        
        
        for value in msg.body:
            newMsg.body.append(value*2)
            
            
        self.sendArray.send_pyobj(newMsg)

    




