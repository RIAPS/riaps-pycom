#
from riaps.run.comp import Component
import logging
import uuid
import time
import os


# Averager algorithm
# Continuous time update equation (for node i)
# dx_i/dt = - Sum_{j} a_{ij} (x_{i} - x_{j} 
# Discretized
# x_{i,k+1} = x_{i,k} - (1 / T_{S}) Sum_{j} a_{ij} (x_{i,k} - x_{j,k})  

class Averager(Component):
    def __init__(self,Ts):
        super(Averager, self).__init__()
        self.Ts = Ts
        self.uuid = uuid.uuid4().int
        self.pid = os.getpid()
        self.dataValues = { }
        self.sensorTime = 0.0
        self.sensorValue = 0.0
        self.ownValue = 0.0
        self.sensorUpdate = False
        self.logger.info("%s - starting",str(self.pid))

    def on_sensorReady(self):
        msg = self.sensorReady.recv_pyobj() # Receive (timestamp,value)
        self.logger.info("on_sensorReady():%s",str(msg[1]))
        self.sensorTime, self.sensorValue = msg
        self.sensorUpdate = True

    def on_nodeReady(self):
        msg = self.nodeReady.recv_pyobj()  # Receive (actorID,timestamp,value)
        # self.logger.info("on_otherReady():%s",str(msg[2]))
        otherId,otherTimestamp,otherValue = msg
        if otherId != self.uuid:
            self.dataValues[otherId] = otherValue
    
    def on_update(self):
        msg = self.update.recv_pyobj()      # Receive timestamp 
        # self.logger.info("on_update():%s",str(msg))
        if self.sensorUpdate:
            self.ownValue = self.sensorValue
            self.sensorUpdate = False
        if len(self.dataValues) != 0:
            sum = 0.0
            for value in self.dataValues.values():
                sum += (self.ownValue - value)
            der = sum / self.Ts
            self.ownValue -= der
        now = time.time()
        msg = (self.uuid,now,self.ownValue)
        self.thisReady.send_pyobj(msg)        

    def on_display(self):
        msg = self.display.recv_pyobj()
        self.logger.info('[%s]:%f' % (str(self.pid),self.ownValue))
