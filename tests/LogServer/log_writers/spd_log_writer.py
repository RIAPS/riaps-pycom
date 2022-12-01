import platform
import spdlog
import time


def add_tcp_sink_st():
    sink = spdlog.tcp_sink_st(server_host="10.0.3.15",
                              server_port=9021,
                              lazy_connect=True)  # if true connect on first log call instead of on construction
    return sink


sinks = [
    spdlog.stdout_sink_st(),
    add_tcp_sink_st(),

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
    time.sleep(1)
