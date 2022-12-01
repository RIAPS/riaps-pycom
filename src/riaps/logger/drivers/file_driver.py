import json

from riaps.logger.drivers.base_driver import BaseDriver


class ServerLogDriver(BaseDriver):
    def __init__(self, driver_type, session_name):
        super().__init__(driver_type, session_name)
        self.nodes = {}
        self.msg_count = 0

    def handle(self, msg):
        node_name = msg["client"]
        data = msg["data"]
        if node_name not in self.nodes:
            self.logger.info(f"driver: add new node: {node_name}")
            f = open(f"{node_name}.log", "a+")
            self.nodes[node_name] = f
        f = self.nodes[node_name]
        f.write(f"{data}\n")
        if self.msg_count % 10 == 0:
            f.flush()

    def close(self):
        self.logger.info("close file handlers")
        for node in self.nodes:
            f = self.nodes[node]
            f.close()



if __name__ == '__main__':
    h = ServerLogDriver("file", "test")
    msg = {"client": "172.21.20.70", "data": "log message"}
    h.handle(msg)
    h.close()
