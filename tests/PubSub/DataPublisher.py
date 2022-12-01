import json
import uuid
from riaps.run.comp import Component


class DataPublisher(Component):
    def __init__(self, uid):
        super().__init__()
        # self.uid = uid if uid else uuid.uuid4()
        self.uid = self.getUUID()
        self.actor_id = hex(int.from_bytes(self.getActorID(), 'big'))
        self.msg_id = 0

    def on_clock(self):
        now = self.clock.recv_pyobj()

        msg = {"uuid": self.getUUID(),
               "actor_id": self.actor_id,
               "timestamp": now,
               "msg_id": self.msg_id}
        if self.msg_id % 10 == 0:
            self.logger.info(f"{json.dumps(msg)}")
        self.msg_id += 1
        self.data_pub.send_pyobj(msg)

    def handlePeerStateChange(self, state, uuid):
        self.logger.info(f"peer {uuid} is {state}")

    def __destroy__(self):
        self.logger.info("terminated")


