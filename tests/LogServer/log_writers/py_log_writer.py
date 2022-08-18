import logging
import logging.handlers
import platform


class CustomAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        return '[%s] %s' % (self.extra['hostname'], msg), kwargs


rootLogger = logging.getLogger('')
rootLogger.setLevel(logging.DEBUG)
socketHandler = logging.handlers.SocketHandler('localhost',
                                               logging.handlers.DEFAULT_TCP_LOGGING_PORT)
# don't bother with a formatter, since a socket handler sends the event as
# an unformatted pickle
rootLogger.addHandler(socketHandler)
hostname = platform.uname().node
adapter = CustomAdapter(rootLogger, {'hostname': hostname})

# Now, we can log to the root logger, or any other logger. First the root...
adapter.info('Jackdaws love my big sphinx of quartz.')

# Now, define a couple of other loggers which might represent areas in your
# application:

logger1 = logging.getLogger('myapp.area1')
adapter1 = CustomAdapter(logger1, {'hostname': hostname})
logger2 = logging.getLogger('myapp.area2')
adapter2 = CustomAdapter(logger2, {'hostname': hostname})

adapter1.debug('Quick zephyrs blow, vexing daft Jim.')
adapter1.info('How quickly daft jumping zebras vex.')
adapter2.warning('Jail zesty vixen who grabbed pay from quack.')
adapter2.error('The five boxing wizards jump quickly.')

