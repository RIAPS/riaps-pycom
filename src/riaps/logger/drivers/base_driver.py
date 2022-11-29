import abc
import logging

class BaseDriver(abc.ABC):

    def __init__(self, driver_type):
        self.logger = logging.getLogger("riaps.logger")
        self.logger.propagate = False
        self.driver_type = driver_type

    @abc.abstractmethod
    def handle(self, msg):
        pass

    def close(self):
        pass
