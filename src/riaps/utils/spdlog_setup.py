'''
Created on Jan 3, 2019

@author: riaps
'''
import platform
import toml
import spdlog
import os

global_pattern = "[%l]:[%m-%d-%Y %H:%M:%S.%e]:[%P]:%n:%v"
sinks = { }
patterns = { }
loggers = {}

levels = {
        'trace': spdlog.LogLevel.TRACE,
        'debug': spdlog.LogLevel.DEBUG,
        'info': spdlog.LogLevel.INFO,
        'warn': spdlog.LogLevel.WARN,
        'err': spdlog.LogLevel.ERR,
        'critical': spdlog.LogLevel.CRITICAL,
        'off': spdlog.LogLevel.OFF        
    }

sizes = {
    'T': 1E12,
    'G': 1E9,
    'M': 1E6,
    'k': 1E3
    }


def file_size(num):
    global sizes
    try:
        if type(num) == int:
            return num
        elif type(num) == str:
            last = num[-1]
            value = int(num[:-1])
            factor = sizes[last]
            return int(value * factor) 
        else:
            raise ValueError('invalid file size: %s' % str(num))
    except:
        raise


def add_stdout_sink_st(_s):
    return spdlog.stdout_sink_st()


def add_stdout_sink_mt(_s):
    return spdlog.stdout_sink_mt()


def add_color_stdout_sink_st(_s):
    return spdlog.stdout_color_sink_st()


def add_color_stdout_sink_mt(_s):
    return spdlog.stdout_color_sink_mt()


def add_parent_dir(s):
    if 'create_parent_dir' in s.keys() and s['create_parent_dir']:
        d = os.path.dirname(s['filename'])
        if d != '':
            try:
                os.mkdir(d)
            except FileExistsError:
                pass

    
def add_basic_file_sink_st(s):
    add_parent_dir(s)
    return spdlog.basic_file_sink_st(filename=s['filename'],
                                     truncate=s['truncate'] if 'truncate' in s.keys() else False)
         
     
def add_basic_file_sink_mt(s):
    add_parent_dir(s)
    return spdlog.basic_file_sink_mt(filename=s['filename'],
                                     truncate=s['truncate'] if 'truncate' in s.keys() else False)


def add_rotating_file_sink_st(s):
    add_parent_dir(s)
    return spdlog.rotating_file_sink_st(filename=s['base_filename'],
                                        max_size=file_size(s['max_size']),
                                        max_files=s['max_files'])


def add_rotating_file_sink_mt(s):
    add_parent_dir(s)
    return spdlog.rotating_file_sink_mt (filename=s['base_filename'],
                                         max_size=file_size(s['max_size']),
                                         max_files=s['max_files'])


def add_daily_file_sink_st(s):
    add_parent_dir(s)
    return spdlog.daily_file_sink_st(filename=s['base_filename'],
                                     rotation_hour=s['rotation_hour'],
                                     rotation_minute=s['rotation_minute'])


def add_daily_file_sink_mt(s):
    add_parent_dir(s)
    return spdlog.daily_file_sink_mt(filename=s['base_filename'],
                                     rotation_hour=s['rotation_hour'],
                                     rotation_minute=s['rotation_minute'])


def add_null_sink_st(_s):
    return spdlog.null_sink_st()


def add_null_sink_mt(_s):
    return spdlog.null_sink_mt()


def add_syslog_sink_st(s):
    return spdlog.syslog_sink_st(ident=s['ident'] if 'ident' in s.keys() else "",
                              syslog_option=s['syslog_option'] if 'syslog_option' in s.keys() else 0,
                              syslog_facility=s['syslog_facility'] if 'syslog_facility' in s.keys() else (1 << 3)
                              )


def add_syslog_sink_mt(s):
    return spdlog.syslog_sink_mt(ident=s['ident'] if 'ident' in s.keys() else "",
                              syslog_option=s['syslog_option'] if 'syslog_option' in s.keys() else 0,
                              syslog_facility=s['syslog_facility'] if 'syslog_facility' in s.keys() else (1 << 3)
                              )


def add_tcp_sink_st(s):
    return spdlog.tcp_sink_st(server_host=s["server_host"],
                               server_port=s["server_port"],
                               lazy_connect=False)  # if true connect on first log call instead of on construction

def add_tcp_sink_mt(s):
    return spdlog.tcp_sink_mt(server_host=s["server_host"],
                              server_port=s["server_port"],
                              lazy_connect=False)  # if true connect on first log call instead of on construction

types = {
        'stdout_sink_st': add_stdout_sink_st,
        'stdout_sink_mt': add_stdout_sink_mt,
        'color_stdout_sink_st': add_color_stdout_sink_st,
        'color_stdout_sink_mt': add_color_stdout_sink_mt,
        'basic_file_sink_st': add_basic_file_sink_st,
        'basic_file_sink_mt': add_basic_file_sink_mt,
        'rotating_file_sink_st': add_rotating_file_sink_st,
        'rotating_file_sink_mt': add_rotating_file_sink_mt,
        'daily_file_sink_st': add_daily_file_sink_st,
        'daily_file_sink_mt': add_daily_file_sink_mt,
        'null_sink_st': add_null_sink_st,
        'null_sink_mt': add_null_sink_mt,
        'syslog_sink_st': add_syslog_sink_st,
        'syslog_sink_mt': add_syslog_sink_mt,
        'tcp_sink_st': add_tcp_sink_st,
        'tcp_sink_mt': add_tcp_sink_mt
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

    
if __name__ == '__main__':
    test = """# level is optional for both sinks and loggers
# level for error logging is 'err', not 'error'
# _st => single threaded, _mt => multi threaded
# syslog_sink is automatically thread-safe by default, no need for _mt suffix

# max_size supports suffix
# - T (terabyte)
# - G (gigabyte)
# - M (megabyte)
# - K (kilobyte)
# - or simply no suffix (byte)

# check out https://github.com/gabime/spdlog/wiki/3.-Custom-formatting
global_pattern = "[%Y-%m-%dT%T%z] [%^%l%$] <%n>: %v"

[[sink]]
name = "console_st"
type = "stdout_sink_st"

[[sink]]
name = "console_mt"
type = "stdout_sink_mt"

[[sink]]
name = "color_console_st"
type = "color_stdout_sink_st"

[[sink]]
name = "color_console_mt"
type = "color_stdout_sink_mt"

[[sink]]
name = "file_out"
type = "basic_file_sink_st"
filename = "log/spdlog_setup.log"
# truncate field is optional
# truncate = false (default)
level = "info"
# optional flag to indicate the set-up to create the log dir first
create_parent_dir = true

[[sink]]
name = "file_err"
type = "basic_file_sink_mt"
filename = "log/spdlog_setup_err.log"
truncate = true
level = "err"
# to show that create_parent_dir is indeed optional (defaults to false)

[[sink]]
name = "rotate_out"
type = "rotating_file_sink_st"
base_filename = "log/rotate_spdlog_setup.log"
max_size = "1M"
max_files = 10
level = "info"

[[sink]]
name = "rotate_err"
type = "rotating_file_sink_mt"
base_filename = "log/rotate_spdlog_setup_err.log"
max_size = "1M"
max_files = 10
level = "err"

[[sink]]
name = "daily_out"
type = "daily_file_sink_st"
base_filename = "log/daily_spdlog_setup.log"
rotation_hour = 17
rotation_minute = 30
level = "info"

[[sink]]
name = "daily_err"
type = "daily_file_sink_mt"
base_filename = "log/daily_spdlog_setup_err.log"
rotation_hour = 17
rotation_minute = 30
level = "err"

[[sink]]
name = "null_sink_st"
type = "null_sink_st"

[[sink]]
name = "null_sink_mt"
type = "null_sink_mt"

# only works for Linux
[[sink]]
name = "syslog_sink_mt"
type = "syslog_sink_mt"
# generally no need to fill up the optional fields below
# ident = "" (default)
# syslog_option = 0 (default)
# syslog_facility = LOG_USER (default macro value)

[[sink]]
name = "syslog_sink_st"
type = "syslog_sink_st"
# generally no need to fill up the optional fields below
# ident = "" (default)
# syslog_option = 0 (default)
# syslog_facility = LOG_USER (default macro value)

[[sink]]
name = "tcp_st"
type = "tcp_sink_st"
server_host = "localhost"
server_port = 12345
lazy_connect = false

[[sink]]
name = "tcp_mt"
type = "tcp_sink_mt"
server_host = "localhost"
server_port = 12345
lazy_connect = false

[[pattern]]
name = "succient"
value = "%c-%L: %v"

[[logger]]
name = "root"
sinks = [
    "console_st", "console_mt",
    "color_console_st", "color_console_mt",
    "daily_out", "daily_err",
    "file_out", "file_err",
    "rotate_out", "rotate_err",
    "null_sink_st", "null_sink_mt",
    "syslog_sink_st", "syslog_sink_mt"]
level = "trace"

[[logger]]
name = "console"
sinks = ["console_st", "console_mt"]
pattern = "succient"

[[logger]]
name = "tcp"
sinks = ["tcp_st", "tcp_mt"]
pattern = "succient"
level = "trace"


""" 
    with open('test.toml', 'w') as f:
        f.write(test)
        
    from_file('test.toml')
    
    for l in loggers.keys():
        logger = spdlog.get(l)
        logger.trace('trace')
        logger.debug('debug')        
        logger.info('info')
        logger.warn('warn')
        logger.error('error')
        logger.critical('critical')
    
