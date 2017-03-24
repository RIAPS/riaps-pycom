#
from riaps.run.comp import Component
import logging

import pprint
from time import time

class IC(Component):
    def __init__(self, parent):
        super(IC, self).__init__()
        self.pending = 0
        
        self.GameLightState = {}
        self.LightState = {}
        self.Densities = {}
        self.initialized = False
        self.timeStamp = time()
        self.cardDict = {'N':'segment1',
                         'E':'segment3',
                         'S':'segment0',
                         'W':'segment2'}
        self.SegDict = {'segment1':'N',
                        'segment3':'E',
                        'segment0':'S',
                        'segment2':'W'}
        self.ICs = {'NIC':0,
                    'EIC':0,
                    'SIC':0,
                    'WIC':0}
        self.ignoreDensities = False
        self.weight = .3 #how much influence surrounding ICs have
        self.minDensity = 10
        self.maxDensity = 50
        self.minTime = 5
        self.maxTime = 20
        self.myActor = parent
        print( self.myActor)

    def on_subICPort(self):
        msg = self.subICPort.recv_json()
        
        if self.myActor == "Actor0":
            if(msg['IC'] == "Actor1"):
                segA = msg['Densities'][self.cardDict['N']]
                segB = msg['Densities'][self.cardDict['E']]
                segC = msg['Densities'][self.cardDict['W']]
                self.ICs['NIC'] = segA + segB + segC
                print("subbed Msg %s", msg)
            if(msg['IC'] == "Actor3"):
                segA = msg['Densities'][self.cardDict['N']]
                segB = msg['Densities'][self.cardDict['E']]
                segC = msg['Densities'][self.cardDict['S']]
                self.ICs['EIC'] = segA + segB + segC
                print("subbed Msg %s", msg)
                
        if self.myActor == "Actor1":
            if(msg['IC'] == "Actor0"):
                segA = msg['Densities'][self.cardDict['E']]
                segB = msg['Densities'][self.cardDict['S']]
                segC = msg['Densities'][self.cardDict['W']]
                self.ICs['SIC'] = segA + segB + segC
                print("subbed Msg %s", msg)
            if(msg['IC'] == "Actor2"):
                segA = msg['Densities'][self.cardDict['N']]
                segB = msg['Densities'][self.cardDict['E']]
                segC = msg['Densities'][self.cardDict['S']]
                self.ICs['EIC'] = segA + segB + segC
                print("subbed Msg %s", msg)
                
        if self.myActor == "Actor2":
            if(msg['IC'] == "Actor1"):
                segA = msg['Densities'][self.cardDict['N']]
                segB = msg['Densities'][self.cardDict['S']]
                segC = msg['Densities'][self.cardDict['W']]
                self.ICs['WIC'] = segA + segB + segC
                print("subbed Msg %s", msg)
            if(msg['IC'] == "Actor3"):
                segA = msg['Densities'][self.cardDict['E']]
                segB = msg['Densities'][self.cardDict['S']]
                segC = msg['Densities'][self.cardDict['W']]
                self.ICs['SIC'] = segA + segB + segC
                print("subbed Msg %s", msg)
                
        if self.myActor == "Actor3":
            if(msg['IC'] == "Actor0"):
                segA = msg['Densities'][self.cardDict['N']]
                segB = msg['Densities'][self.cardDict['S']]
                segC = msg['Densities'][self.cardDict['W']]
                self.ICs['WIC'] = segA + segB + segC
                print("subbed Msg %s", msg)
            if(msg['IC'] == "Actor2"):
                segA = msg['Densities'][self.cardDict['N']]
                segB = msg['Densities'][self.cardDict['E']]
                segC = msg['Densities'][self.cardDict['W']]
                self.ICs['NIC'] = segA + segB + segC
                print("subbed Msg %s", msg)
                
        
    def on_clock(self):
        msg = self.clock.recv_pyobj()
        #self.logger.info('on_clock():%s', msg)
        #msg = "data_ready"
        
        if(bool(self.GameLightState)and not self.initialized):
            self.LightState = self.GameLightState
            #self.initialized = True
            for seg in self.LightState:
                if self.SegDict[seg] in ('N', 'S'):
                    self.LightState[seg]['vehicle']='Green'
                    self.LightState[seg]['pedestrian']='Red'
                else:
                    self.LightState[seg]['vehicle']='Red'
                    self.LightState[seg]['pedestrian']='Red'
            self.setGameLights()
            self.timeStamp = time()
        elif(not self.initialized):
            self.logger.info("%s Waiting for server", self.myActor)
        else:
            if True == self.controller():
                self.switchState()
                self.timeStamp = time()
            else:
                pass
            
        #while self.pending > 0:     # Handle the case when there is a pending request
        #    self.on_setLightsPort()
        #self.setLightsPort.send_pyobj("client message")
        #self.pending += 1 
        
        #self.logger.info('self:\n%s\n', pprint.pformat(self.__dict__))

        #self.densityPort.send_pyobj(msg)
        
    def controller(self):
        dT = time() - self.timeStamp
        if dT >= self.maxTime:
            return True
        if self.ignoreDensities:
            return False
        if dT < self.minTime:
            return False
        
        RedQ = 0
        GreenQ = 0
        for seg in self.LightState:
            ICDs = self.ICs[self.SegDict[seg]+'IC']
            #print "----------{}------------".format(ICDs)
            if(self.LightState[seg]['vehicle'])=='Green':
                GreenQ += self.Densities[seg] + ICDs*self.weight
            else:
                RedQ += self.Densities[seg] + ICDs*self.weight

        #print "name:{}, redQ:{}".format(self.name, RedQ)
        #print "name:{}, GreenQ:{}".format(self.name, GreenQ)
        if RedQ <= self.minDensity:
            return False
        if GreenQ > self.maxDensity:
            return False
        else:
            return True
        
    def on_lightPort(self):
        msg = self.lightPort.recv_pyobj()
        self.GameLightState = msg
        self.logger.info("lightState: \n%s\n", pprint.pformat(msg))
        
    def on_densityPort(self):
        msg = self.densityPort.recv_pyobj()
        self.Densities = msg
        self.logger.info("DensityState: \n%s\n", pprint.pformat(msg))
        ICD = {'IC' : self.myActor,
               'Densities' : self.Densities}
        #print("ICD: ", ICD)
        #self.pubICPort.send_json(ICD)
        self.pubICPort.send_pyobj(ICD)
        
    def on_setLightsPort(self):
        msg = self.setLightsPort.recv_pyobj()
        self.logger.info("Server response received: %s", pprint.pformat(msg))
        self.pending -= 1    
        self.initialized = True    
        
    def setGameLights(self):
        #msg_string = json.dumps(self.LightState)
        while self.pending > 0:     # Handle the case when there is a pending reques          
            self.on_setLightsPort()
        #self.setLightsPort.send_pyobj("client message")
        self.setLightsPort.send_pyobj(self.LightState)
        #print(self.LightState)
        self.pending += 1 
        
        #response = self.client("setGameLightState_client").call(msg_string)
        #logging.debug("@setGameLights IC:%s success:%s", self.name, json.loads(response))
        
    def switchState(self):
        for seg in self.LightState:
            if(self.LightState[seg]['vehicle'])=='Green':
                self.LightState[seg]['vehicle']='Red'
                self.LightState[seg]['pedestrian']='Red'
            else:
                self.LightState[seg]['vehicle']='Green'
                self.LightState[seg]['pedestrian']='Red'
        self.setGameLights()
        
    
    
