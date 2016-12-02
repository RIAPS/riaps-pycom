#
from riaps.run.comp import Component
import logging

# Averager algorithm
# Continuous time update equation (for node i)
# dx_i/dt = - Sum_{j} a_{ij} (x_{i} - x_{j} 
# Discretized
# x_{i,k+1} = x_{i,k} - (1 / T_{S}) Sum_{j} a_{ij} (x_{i,k} - x_{j,k})  

class Averager(Component):
    def __init__(self):
        super(Averager, self).__init__()
        # Get our unique actor ID
        # Create measurement table

    def on_sensorReady(self):
        msg = self.sensorReady.recv_pyobj() # Receive (timestamp,value)
        self.logger.info("on_sensorReady():%s",msg)
        # Save our own data

    def on_otherReady(self):
        msg = self.otherReady.recv_pyobj()  # Receive (actorID,timestamp,value)
        self.logger.info("on_otherReady():%s",msg)
        # Store data from other
        pass
    
    def on_update(self):
        msg = self.update.recv_pyobj()
        self.logger.info("on_update():%s",msg)
        # Update average using discrete time equation
        # Broadcast it to others: 
        msg = "node data"                   # Should be (actorID,timestamp,value)
        self.nodeReady.send_pyobj(msg)        
        pass

    
