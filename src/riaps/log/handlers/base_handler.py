import abc
import logging

class BaseHandler(abc.ABC):

    def __init__(self, handler_type):
        self.logger = logging.getLogger(__name__)
        self.handler_type = handler_type
        self.nodes = {}

    @abc.abstractmethod
    def handle(self, msg):
        pass

    def close(self):
        pass

    # @abc.abstractmethod
    # def add_node_display(self, node_name):
    #     pass
    #
    # @abc.abstractmethod
    # def write_display(self, node_name, msg):
    #     pass
