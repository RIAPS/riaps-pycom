#
from riaps.run.comp import Component
import logging
import os

class Filter(Component):
    def __init__(self):
        super(Filter, self).__init__()
        self.pid = os.getpid()
        self.pending = 0
        self.logger.info("Filter()")

    def on_ready(self):
        msg = self.ready.recv_pyobj()
        self.logger.info("on_ready():%s [%d]" % (msg, self.pid))
        sendTime = self.ready.get_sendTime()
        recvTime = self.ready.get_recvTime()
        self.logger.info("SensorReady recv'd @ %f, sent @ %f, diff = %f"
                         % (sendTime,recvTime,recvTime-sendTime))
        while self.pending > 0:     # Handle the case when there is a pending request
            self.on_query()
        msg = "sensor_query"
        if self.query.send_pyobj(msg):
            self.pending += 1

    def on_query(self):
        msg = self.query.recv_pyobj()
        self.logger.info("on_query():%s" % msg)
        sendTime = self.query.get_sendTime()
        recvTime = self.query.get_recvTime()
        self.logger.info("SensorValue recv'd @ %f, sent @ %f, diff = %f"
                         % (sendTime,recvTime,recvTime-sendTime))

        self.pending -= 1
        msg = "local_est(" + str(self.pid) + ")"
        # self.estimate.send_pyobj(msg)
