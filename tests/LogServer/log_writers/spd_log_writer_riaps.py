import platform
import spdlog
import struct
import time
import riaps.utils.spdlog_setup as spdlog_setup

import toml


def add_stdout_sink_mt(_s):
    return spdlog.stdout_sink_mt()


def add_tcp_sink_st(s):
    sink = spdlog.tcp_sink_st(server_host=s["server_host"],
                              server_port=s["server_port"],
                              lazy_connect=True)  # if true connect on first log call instead of on construction
    return sink

    # try:
    #     sink = spdlog.tcp_sink_st(server_host=s["server_host"],
    #                               server_port=s["server_port"],
    #                               lazy_connect=True)  # if true connect on first log call instead of on construction
    #     return sink
    # except RuntimeError as e:
    #     print(f"e: {e}")


def add_tcp_sink_mt(s):
    return spdlog.tcp_sink_mt(server_host=s["server_host"],
                              server_port=s["server_port"],
                              lazy_connect=True)  # if true connect on first log call instead of on construction

    # try:
    #     sink = spdlog.tcp_sink_mt(server_host=s["server_host"],
    #                               server_port=s["server_port"],
    #                               lazy_connect=True)  # if true connect on first log call instead of on construction
    #     return sink
    # except RuntimeError as e:
    #     print(f"e: {e}")


sinks = {}
patterns = {}
loggers = {}
types = {
    'stdout_sink_mt': add_stdout_sink_mt,
    'tcp_sink_st': add_tcp_sink_st,
    'tcp_sink_mt': add_tcp_sink_mt
}
levels = {
    'trace': spdlog.LogLevel.TRACE,
    'debug': spdlog.LogLevel.DEBUG,
    'info': spdlog.LogLevel.INFO,
    'warn': spdlog.LogLevel.WARN,
    'err': spdlog.LogLevel.ERR,
    'critical': spdlog.LogLevel.CRITICAL,
    'off': spdlog.LogLevel.OFF
}


def from_file(fname):
    global global_pattern, sinks, patterns, loggers, levels
    d = toml.load(fname)
    if 'global_pattern' in d.keys():
        global_pattern = d['global_pattern']
    if 'sink' in d.keys():
        for s in d['sink']:
            fun = types[s['type']]
            sink = fun(s)
            if 'level' in s.keys():
                sink.set_level(levels[s['level']])
            sinks[s['name']] = sink
    if 'pattern' in d.keys():
        for p in d['pattern']:
            patterns[p['name']] = p
    if 'logger' in d.keys():
        for l in d['logger']:
            name = l['name']
            _sinks = []
            for sname in l['sinks']:
                _sinks += [sinks[sname]]
            logger = spdlog.SinkLogger(name, _sinks)
            if 'pattern' in l.keys():
                p = l['pattern']
                if p in patterns.keys():
                    if 'value' in patterns[p]:
                        pat = patterns[p]['value']
                        if 'extra' in patterns[p]:
                            extra = patterns[p]['extra']
                            node_id = platform.uname().node
                            print(extra)
                            pat = pat.format(*extra, node_id=node_id)
                        logger.set_pattern(pat)
            elif global_pattern:
                logger.set_pattern(global_pattern)
            if 'level' in l.keys():
                logger.set_level(levels[l['level']])
            loggers[name] = logger


def get_logger(name):
    global loggers
    if name in loggers.keys():
        return loggers[name]
    else:
        return None


# from_file("riaps-log.conf")
# logger = get_logger("")


spdlog_setup.from_file("riaps-log.conf")
logger = spdlog_setup.get_logger("")

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
