#
from riaps.run.comp import Component
import logging
import os
import capnp
import distributedestimator_capnp

class LocalEstimator(Component):
    def __init__(self,iArg,fArg,sArg,bArg):
        super(LocalEstimator, self).__init__()
        self.pid = os.getpid()
        self.pending = 0
        self.logger.info("LocalEstimator(iArg=%d,fArg=%f,sArg=%s,bArg=%s)"
                         %(iArg,fArg,sArg,str(bArg)))
        self.logger.info("name,typeName,localID,actorName,appName = (%s,%s,%s,%s,%s,%s)"
                         % (self.getName(),self.getTypeName(),hex(self.getLocalID()),
                            self.getActorName(),self.getAppName(),
                            hex(int.from_bytes(self.getActorID(),'big'))))

    def on_ready(self):
        # msg = self.ready.recv_pyobj()
        msgSensorReadyBytes = self.ready.recv()
        msgSensorReady = distributedestimator_capnp.SensorReady.from_bytes(msgSensorReadyBytes)

        self.logger.info("on_ready():%s [%d]" % (msgSensorReady.msg, self.pid))

        # Check if the 'query' port is connected, if not, return
        if self.query.connected() == 0:
            self.logger.info('Not yet connected!')
            return

        while self.pending > 0:     # Handle the case when there is a pending request
            self.on_query()

        queryMsg = distributedestimator_capnp.SensorQuery.new_message()
        queryMsg.msg = "sensor_query"

        #msg = "sensor_query"
        #self.query.send_pyobj(msg)
        queryBytes = queryMsg.to_bytes()
        if self.query.send(queryBytes):
            self.pending += 1

    def on_query(self):
        #msg = self.query.recv_pyobj()
        queryBytes = self.query.recv()
        queryMsg   = distributedestimator_capnp.SensorValue.from_bytes(queryBytes)
        self.logger.info("on_query():%s" % queryMsg.msg)
        self.pending -= 1

        estimateMsg = distributedestimator_capnp.Estimate.new_message()
        estimateMsg.msg = "local_est(" + str(self.pid) + ")"
        #msg = "local_est(" + str(self.pid) + ")"
        #self.estimate.send_pyobj(msg)
        estimateMsgBytes = estimateMsg.to_bytes()
        self.estimate.send(estimateMsgBytes)
