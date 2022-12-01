import logging
import threading

# https://stackoverflow.com/questions/9212228/using-custom-formatter-classes-with-pythons-logging-config-module
# https://docs.python.org/3/library/logging.config.html#user-defined-objects


class CustomFormatter(logging.Formatter):
    def __init__(self, default):
        super().__init__()
        self.default = default

    def format(self, record):
        record.msg = f"tid:{threading.get_native_id()}]: {record.msg}"
        return self.default.format(record)


def factory(fmt, datefmt, style):
    default = logging.Formatter(fmt, datefmt, style)
    return CustomFormatter(default)
