import logging
import logging.handlers
import platform
import time


class CustomAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        return '[%s] %s' % (self.extra['hostname'], msg), kwargs


rootLogger = logging.getLogger('')
rootLogger.setLevel(logging.DEBUG)
socketHandler = logging.handlers.SocketHandler('172.21.20.70',
                                               logging.handlers.DEFAULT_TCP_LOGGING_PORT)
consoleHandler = logging.StreamHandler()
# don't bother with a formatter, since a socket handler sends the event as
# an unformatted pickle
rootLogger.addHandler(socketHandler)
rootLogger.addHandler(consoleHandler)
hostname = platform.uname().node

logger1 = logging.getLogger('myapp.area1')
adapter1 = CustomAdapter(logger1, {'hostname': hostname})
logger2 = logging.getLogger('myapp.area2')
adapter2 = CustomAdapter(logger2, {'hostname': hostname})

for i in range(10):
    msg = f"message: {i}"
    adapter1.info(msg)
    time.sleep(1)

