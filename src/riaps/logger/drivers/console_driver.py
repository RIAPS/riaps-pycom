# 
# Console log driver
#

from riaps.logger.drivers.base_driver import BaseDriver

class ServerLogDriver(BaseDriver):
    def __init__(self, driver_type,session_name):
        super().__init__(driver_type)
        self.session_name = session_name
        # print(f"driver type: {self.driver_type}, session: {self.session_name}")

    def handle(self, msg):
        node = msg["client"]
        data = msg["data"]
        print("[%s:%s]:%s" % (str(node),str(self.session_name),str(data)))
    
    def close(self):
        pass

if __name__ == '__main__':
    h = ServerLogDriver("console","test")
    msg = { "127.0.0.1" : "riaps-1234.local", "data" : "log message"  }
    h.handle(msg)
    h.close()
    
    