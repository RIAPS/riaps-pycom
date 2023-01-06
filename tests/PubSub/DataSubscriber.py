import json

from riaps.run.comp import Component


class DataSubscriber(Component):
    def __init__(self):
        super().__init__()
        self.known_senders = []

    def on_data_sub(self):
        msg = self.data_sub.recv_pyobj()
        timestamp = msg["timestamp"]
        msg_id = msg["msg_id"]
        sender = msg["uuid"]
        if sender not in self.known_senders:
            self.known_senders.append(sender)
            log_msg = {"known_senders": self.known_senders}
            self.logger.info(json.dumps(log_msg))
        else:
            if msg_id % 10 == 0:
                log_msg = {"known_senders": self.known_senders}
                self.logger.info(json.dumps(log_msg))

    def handlePeerStateChange(self, state, uuid):
        self.logger.info(f"peer {uuid} is {state}")

    def __destroy__(self):
        self.logger.info("terminated")


