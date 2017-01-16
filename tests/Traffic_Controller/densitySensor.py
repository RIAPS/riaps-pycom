from riaps.run.comp import Component
import logging

class densitySensorThread(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.port = port
        self.period = 2500
        self.active = threading.Event()
    
    def run(self):
        self.plug = self.port.setupPlug(self) #I think this is basically to let the component poll its device ports...?