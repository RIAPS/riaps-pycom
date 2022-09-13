import platform
import spdlog
import struct
import time

sinks = [
    spdlog.stdout_sink_st(),
    spdlog.tcp_sink_st("localhost", 12345, True),
]

logger = spdlog.SinkLogger("MyLogger", sinks)


def tcp_log(log_msg, level):
    jsonpattern = f"{{\"time\": \"%E\", " \
                  "\"name\": \"%n\", " \
                  "\"level\": \"%^%l%$\", " \
                  "\"process\": %P," \
                  "\"thread\": %t, " \
                  "\"message\": \"%v\", " \
                  f"\"hostname\": \"{platform.uname().node}\" }}"

    basic = "message: %v"
    pattern = jsonpattern
    logger.set_pattern(pattern)
    print(log_msg)
    getattr(logger, level)(log_msg)


for i in range(10):
    tcp_log(f"message: {i}", "info")
    # time.sleep(5)