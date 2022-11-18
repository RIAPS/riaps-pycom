# from riaps.log.base_handler import BaseHandler
import json

from riaps.log.handlers.base_handler import BaseHandler


class AppProperties:
    has_started = False
    has_ended = False


class ServerLogHandler(BaseHandler):
    def __init__(self, handler_type, test_data):
        super().__init__(handler_type)
        print(f"handler type: {self.handler_type}")

        self.test_data = test_data
        # self.app_properties = AppProperties()
        self.app_properties = {"has_started": False,
                               "has_ended": False}

    def handle(self, msg):
        # msg = json.loads(raw_msg)
        # print(f"type(msg): {type(msg)}")
        # print(f"sender: {msg['node_name']}")
        try:
            data = json.loads(msg["data"])
        except json.decoder.JSONDecodeError as e:
            print(f"Why can't I load this? {e}")
            data = msg["data"]
        # print(f"type(data): {type(data)}")
        # print(f"data: {data}")
        # print(f"time: {data['time']}")
        node = msg["node_name"]
        app_name = data["name"]
        app_msg = data["message"]
        # print(f"app_msg: {app_msg}")

        if app_name == "SineMQTT.mqtt.mqtt":
            if app_msg == "MQTT - starting":
                # self.app_properties.has_started = True
                self.app_properties["has_started"] = True
                self.test_data[node] = self.app_properties
                print(f"self.app_properties.has_started: {self.app_properties}")
            if app_msg == "MQThread ended":
                # self.app_properties.has_ended = True
                self.app_properties["has_ended"] = True
                self.test_data[node] = self.app_properties
                print(f"self.app_properties.has_started: {self.app_properties}")


if __name__ == '__main__':
    test_data = {}
    h = ServerLogHandler("hoi", test_data)
