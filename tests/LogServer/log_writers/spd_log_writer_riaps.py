import riaps.utils.spdlog_setup as spdlog_setup
import platform
import time

loggers = spdlog_setup.from_file("example_configs/riaps-log.conf")

print(f"loggers: {loggers}")


def test_loggers(msg):
    for logger in loggers:
        print(f"logger: {logger}")
        loggers[logger].info(msg)


def tcp_log(log_msg, level):
    jsonpattern = f"{{\"time\": \"%E\", " \
                  "\"name\": \"%n\", " \
                  "\"level\": \"%^%l%$\", " \
                  "\"process\": %P," \
                  "\"thread\": %t, " \
                  "\"message\": \"%v\", " \
                  f"\"hostname\": \"{platform.uname().node}\" }}"

#     basic = "message: %v"
#     pattern = jsonpattern
#     logger.set_pattern(pattern)
#     print(log_msg)
#     getattr(logger, level)(log_msg)
#
#


for i in range(10):
    test_loggers(f"message: {i}")
    time.sleep(1)
