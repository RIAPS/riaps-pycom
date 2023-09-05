# RIAPS Logger Quick reference
RIAPS logs can be viewed in real-time for both local and remote nodes using the `riaps_logger` log server tool. Note that the following commands rely on correct configuration of the `riaps-log.conf` files. This is explained below this quick reference section.

There are two loggers, which can be started simultaneously if desired:

- platform logger: `riaps_logger -p [HOST:[PORTP]][-d DRIVER]` captures logs written by the RIAPS platform itself.
- app logger: `riaps_logger -a [HOST:[PORTA]][-d DRIVER]` captures logs written by RIAPS applications.
- `riaps_logger -p [HOST:[PORTP]] -a [HOST:[PORTA]][-d DRIVER] `starts both loggers

The logger operates uses a network interface and a port. 

The network interface is identified by the IP address of that interface (provided in the `HOST` argument) and it defaults to the network interface used by the RIAPS framework (as set in `/etc/riaps.conf`). 

The port arguments: `PORTP` for the platform logger and `PORTA` for the app logger are optional and
default to `logging.handlers.DEFAULT_TCP_LOGGING_PORT` (9020) and `logging.handlers.DEFAULT_TCP_LOGGING_PORT+1` (9021) respectively. 

The port numbers must be unique (and different), and must match the port numbers used in the logger configuration of the RIAPS nodes, i.e. the `/etc/riaps-log.conf` for the platform, and the `riaps_apps/APP/riaps-log.conf` for the app. 

The `DRIVER` options can take the values `console` (the default) and `tmux`. 

The console option selects sending all messages to the `stdout` of the `riaps_logger` process. 

The `tmux` option will launch `tmux` sessions called `platform` and `app` for viewing the respective logs in terminal window. To view them a user would run:

`tmux attach -t platform`

or 

`tmux attach -t app`


---

## Platform logging
###  Configuration

Each node specified in `/etc/riaps/riaps-hosts.conf` needs the `socketHandler` to be added to the list of `[handlers]` for the `root` logger in the `/etc/riaps/riaps-log.conf` file, and the `args` in the `[handler_socketHandler]` definition needs to be modified to match the IP address of the node running the `riaps_logger`. To be explicit, here is an example of those elements:
 
```
[loggers]
keys=root,riaps.deplo.spcmon
...
[handlers]
keys=consoleHandler,socketHandler
...
[logger_root]
level=WARNING
handlers=consoleHandler, socketHandler
propagate=0

[logger_riaps.deplo.spcmon]
level=INFO
handlers=consoleHandler,socketHandler
qualname=riaps.deplo.spcmon
propagate=0
...
[handler_socketHandler]
class=handlers.SocketHandler
level=DEBUG
formatter=simpleFormatter
# IP address and port number for the riaps_logger host and port
args=("192.168.1.123",9020,)
```

All the incoming platform log messages are formatted by the `riaps_logger` using the the handler's formatter attached to the logger called `riaps.rlog`. Note that this is done on the server side, not in the clients. The logger defaults to:
```
[logger_riaps.rlog]
level=INFO
# do NOT include sockethandler here
handlers=consoleHandler
propagate=0
qualname=riaps.rlog

```
 
### Usage 

Start the log server with:
```bash
$ riaps_logger -p [HOST:[PORT]]
```
e.g.,
```bash
$ riaps_logger -p -d tmux
```

Then view the platform logs by attaching to the tmux session:
```bash
$ tmux attach -t platform
```

---

## Application logging
###  Configuration

#### 1. Network access to the `riaps_logger` endpoint

If RIAPS has security enabled, each node **MUST** be given explicit access to the log server in the application deployment file. For example:
```
// RIAPS deployment file
app ExampleApplication {
    host riaps-1234.local {
        network 192.168.1.123; //IP address of the host running riaps_logger
    }
    ...
}
```
#### 2. Configuring the application logger

The application `spdlog` configuration file (`riaps_apps/APP/riaps-log.conf`) in the application directory (APP) uses the `spdlog` format and must include a "TCP sink" (endpoint), such as:
```conf
[[sink]]
name = "tcp_st"
type = "tcp_sink_st"
server_host = "192.168.1.123"
server_port = 9021
lazy_connect = true

[[logger]]
name = "<ACTOR NAME>.<COMPONENT NAME>"
sinks = ["tcp_st",]
level = "trace"
```
Where the `server_host` and `server_port` match overall configuration and `<ACTOR NAME>.<COMPONENT NAME>` is to be replaced with the name of actor and component to log e.g., `WeatherIndicator.sensor` for the [WeatherMonitor](https://github.com/RIAPS/riaps-apps/tree/master/apps-vu/WeatherMonitor/Python) application. See the [RIAPS Component Logging Tutorial](https://riaps.github.io/tutorials/logging.html) for more information.

***Note***: The platform log messages should always go to a platform logger port and the app log messages should always go to an app logger port. Violating this rule can lead to strange crashes in the `riaps_logger`. 

***Note***: Each logger has a sink and a formatting pattern associated with it. These are linked together when the logger is created. If multiple loggers use the same sink, the sink will be associated only with the last logger and its assigned pattern. This can lead to unexpected formatting of messages coming from loggers that instantiated the sink with a different pattern previously.  To avoid this, one can use separate sinks/patterns for each logger (the sinks will use the same server_host and server-port). 

### Usage: 
Start the log server with:
```bash
$ riaps_logger -a [HOST:[PORT]]
```
e.g.,
```bash
$ riaps_logger -a -d tmux
```
Then view the application logs by attaching to the tmux session:

```bash
$ tmux attach -t app
```



