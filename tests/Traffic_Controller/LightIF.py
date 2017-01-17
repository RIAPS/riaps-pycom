from riaps.run.comp import Component
import logging #if we have a logger, is this necessary? For the thread, yes. 
import threading
import time

import os # not sure why we need this. Its used to get the pid

import socket
import json

class LightIFThread(threading.Thread):
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
                lightState = self.send2Game(self.getLightState(self.IC))
                #value = time.time()
                #self.plug.send_pyobj(value)
                self.plug.send_pyobj(lightState)
                
    def activate(self):
        self.active.set()
    
    def deactivate(self):
        self.active.clear()
    
    def terminate(self):
        self.terminated.set()
        
    def setLights(self, state_req):
        rep = self.send2Game(self.setLightState_All(self.IC, state_req))
        print("set light reply", rep)
        #self.plug.send_pyobj(rep)
        
    def send2Game(self, msg):
        response = 0
        self.gameSock.settimeout(1)
        msg_string = json.dumps(msg)
        #gameSock.sendto(data_string, ("localhost", 11000))
        self.gameSock.sendto(msg_string.encode(encoding='utf_8', errors='strict'), (self.gameServerIP, 11000))
        #self.logger.info("@SEND msg_str: %s", pprint.pformat(msg_string))
        try:
            response_str, srvr = self.gameSock.recvfrom(1024)
            #self.logger.info("@SEND response_str: %s", pprint.pformat(response_str))
            response = json.loads(response_str.decode())

        except socket.timeout:
            response = ""
            self.logger.warning('Request timed out')
        return response
    
    def getLightState(self, IC):
        msg = {
        'Method': 'GETSTATE',
        'Object': {
                    'Name': 'NodeId',
                    'Type': 'PARAMETER',
                    'Value': IC,  #// should be 0 - 3 (for the selected ids)
                    'ValueType': 'System.UInt32'
                    }
        }
        return msg;
    
    def setLightState_All(self, IC, state):
        msg = {
                'Method': 'SETSTATE',
                'Object':
                            {
                            'Name': 'NodeId',
                            'Type': 'PARAMETER',
                            'Value': IC,  #// should be 0 - 3 (for the selected ids)
                            'ValueType': 'System.UInt32',
                            'Parameters':
                                        [
                                            {
                                            'Name': 'SegmentId',
                                            'Type': 'PARAMETER',
                                            'Value': '0',
                                            'ValueType': 'System.UInt32'        },
                                            {
                                            'Name': 'VehicleState',
                                            'Type': 'PARAMETER',
                                            'Value': state['segment0']['vehicle'],
                                            'ValueType': 'System.String'        },
                                            {
                                            'Name': 'PedestrianState',
                                            'Type': 'PARAMETER',
                                            'Value':state['segment0']['pedestrian'] ,
                                            'ValueType': 'System.String'
                                            },
                                            {
                                            'Name': 'SegmentId',
                                            'Type': 'PARAMETER',
                                            'Value': '1',
                                            'ValueType': 'System.UInt32'        },
                                            {
                                            'Name': 'VehicleState',
                                            'Type': 'PARAMETER',
                                            'Value': state['segment1']['vehicle'],
                                            'ValueType': 'System.String'        },
                                            {
                                            'Name': 'PedestrianState',
                                            'Type': 'PARAMETER',
                                            'Value':state['segment1']['pedestrian'] ,
                                            'ValueType': 'System.String'
                                            },
                                            {
                                            'Name': 'SegmentId',
                                            'Type': 'PARAMETER',
                                            'Value': '2',
                                            'ValueType': 'System.UInt32'        },
                                            {
                                            'Name': 'VehicleState',
                                            'Type': 'PARAMETER',
                                            'Value': state['segment2']['vehicle'],
                                            'ValueType': 'System.String'        },
                                            {
                                            'Name': 'PedestrianState',
                                            'Type': 'PARAMETER',
                                            'Value':state['segment2']['pedestrian'] ,
                                            'ValueType': 'System.String'
                                            },
                                            {
                                            'Name': 'SegmentId',
                                            'Type': 'PARAMETER',
                                            'Value': '3',
                                            'ValueType': 'System.UInt32'        },
                                            {
                                            'Name': 'VehicleState',
                                            'Type': 'PARAMETER',
                                            'Value': state['segment3']['vehicle'],
                                            'ValueType': 'System.String'        },
                                            {
                                            'Name': 'PedestrianState',
                                            'Type': 'PARAMETER',
                                            'Value':state['segment3']['pedestrian'],
                                            'ValueType': 'System.String'
                                            }
                                        ]
                            }
                }
        return msg
        

class LightIF(Component):
    def __init__(self,rate, gameServerIP, parent):
        super(LightIF, self).__init__()
        self.pid = os.getpid()
        self.logger.info("LightIF(rate=%d) [%d]", rate, self.pid)
        self.LightIFThread = None #handle for thread once we make it
        self.rate = rate
        self.gameServerIP = gameServerIP
        self.parent = parent
        #self.density = {}
        
    def on_clock(self):
        if self.LightIFThread == None:
            self.LightIFThread = LightIFThread(self.rate, self.trigger, self.gameServerIP, self.parent)          # Port object to talk to 
            self.LightIFThread.start()
            self.trigger.activate()        
        now = self.clock.recv_pyobj()   # Receive time (as float)
        self.logger.info('on_clock():%s',now)
        msg = (now,self.pid)        # Send (timestamp,value) 
        
        
        #self.densityPort.send_pyobj(msg)
        
    def on_setLightsPort(self):
        state_req = self.setLightsPort.recv_pyobj()
        self.logger.info("Client Message received: \n%s", pprint.pformat(state_req))
        self.LightIFThread.setLights(state_req)
        
        
        #rep = self.send2Game(self.setLightState_All(self.IC, state_req))
        #self.setLightsPort.send_pyobj(rep)

    def __destroy__(self):
        self.logger.info("__destroy__")
        
    def on_trigger(self):                   # Internally triggered op
        self.lightState = self.trigger.recv_pyobj()     # Receive time (as float)
        self.logger.info('on_trigger():%s',self.lightState)
        self.lightPort.send_pyobj(self.lightState)
