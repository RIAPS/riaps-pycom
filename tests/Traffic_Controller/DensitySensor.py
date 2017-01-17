from riaps.run.comp import Component
import logging #if we have a logger, is this necessary? For the thread, yes. 
import threading
import time

import os # not sure why we need this. Its used to get the pid

import socket
import json

class DensitySensorThread(threading.Thread):
    def __init__(self, rate, port, gameServerIP, parent):
        threading.Thread.__init__(self)
        self.port = port
        self.period = rate
        self.active = threading.Event()
        self.waiting = threading.Event()
        self.terminated = threading.Event()
        self.terminated.clear()
        
        self.gameSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.gameServerIP = gameServerIP
        print("GSIP", self.gameServerIP)
        self.IC = parent[-1]
        print("parent: ", parent[-1])
        
    
    def run(self):
        self.plug = self.port.setupPlug(self) #I think this is basically to let the component poll its device ports...?
        # I think this is essentially a heartbeat and handles ctrl-c
        while 1:
            self.active.wait(None)#no clue
            if self.terminated.is_set():break #no clue
            self.waiting.wait(self.period)
            if self.terminated.is_set():break
            if self.active.is_set():
                gameDensity = self.send2Game(self.getDensities(self.IC))
                #value = time.time()
                #self.plug.send_pyobj(value)
                self.plug.send_pyobj(gameDensity)
                
    def activate(self):
        self.active.set()
    
    def deactivate(self):
        self.active.clear()
    
    def terminate(self):
        self.terminated.set()
        
    def send2Game(self, msg):
        response = 0
        self.gameSock.settimeout(1)
        msg_string = json.dumps(msg)
        #print ("msg string: {}".format(type(msg_string)))
        #gameSock.sendto(data_string, ("localhost", 11000))
        self.gameSock.sendto(msg_string.encode(encoding='utf_8', errors='strict'), (self.gameServerIP, 11000))
        #self.logger.info("@SEND msg_str: %s", pprint.pformat(msg_string))
        try:
            response_str, srvr = self.gameSock.recvfrom(1024)            
            #self.logger.info("@SEND response_str: %s", pprint.pformat(response_str))
            response = json.loads(response_str.decode())
            #print("response: ", response_str)

        except socket.timeout:
            response = ""
            self.logger.warning('Request timed out')
        return response
    
    def getDensities(self, IC):
        msg = {
                'Method': 'GETDENSITIES',
                'Object':{
                            'Name': 'NodeId',
                            'Type': 'PARAMETER',
                            'Value': IC,  #// should be 0 - 3 (for the selected ids)
                            'ValueType': 'System.UInt32',
                            'Parameters':
                            [
                                {
                                'Name': 'SegmentId',
                                'Type': 'PARAMETER',
                                'Value': 0,
                                'ValueType': 'System.UInt32'
                                },
                                {
                                'Name': 'SegmentId',
                                'Type': 'PARAMETER',
                                'Value': 1,
                                'ValueType': 'System.UInt32'
                                },
                                {
                                'Name': 'SegmentId',
                                'Type': 'PARAMETER',
                                'Value': 2,
                                'ValueType': 'System.UInt32'
                                },
                                {
                                'Name': 'SegmentId',
                                'Type': 'PARAMETER',
                                'Value': 3,
                                'ValueType': 'System.UInt32'
                                },

                            ]
                         }
                }
        return msg;
        
class DensitySensor(Component):
    def __init__(self,rate, gameServerIP, parent):
        super(DensitySensor, self).__init__()
        self.pid = os.getpid()
        self.logger.info("Sensor(rate=%d) [%d]", rate, self.pid)
        self.DensitySensorThread = None #handle for thread once we make it
        self.rate = rate
        self.gameServerIP = gameServerIP
        self.parent = parent
        self.density = {}
        
    def on_clock(self):
        if self.DensitySensorThread == None:
            self.DensitySensorThread = DensitySensorThread(self.rate, self.trigger, self.gameServerIP, self.parent)          # Port object to talk to 
            self.DensitySensorThread.start()
            self.trigger.activate()        
        now = self.clock.recv_pyobj()   # Receive time (as float)
        self.logger.info('on_clock():%s',now)
        msg = (now,self.pid)        # Send (timestamp,value) 
        
        
        #self.densityPort.send_pyobj(msg)

    def __destroy__(self):
        self.logger.info("__destroy__")
        
    def on_trigger(self):                   # Internally triggered op
        self.density = self.trigger.recv_pyobj()     # Receive time (as float)
        self.logger.info('on_trigger():%s',self.density)
        self.densityPort.send_pyobj(self.density)

    