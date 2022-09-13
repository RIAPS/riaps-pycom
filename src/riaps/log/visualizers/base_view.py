import abc


class BaseView:

    def __init__(self, session_name):
        self.session_name = session_name
        self.nodes = {}

    @abc.abstractmethod
    def add_node_display(self, node_name):
        pass

    @abc.abstractmethod
    def write_display(self, node_name, msg):
        pass
