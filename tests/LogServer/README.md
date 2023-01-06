# RIAPS Log Servers Quick reference
RIAPS logs can be viewed in real-time for both local and remote nodes using the RIAPS log servers. ( Note that the follwing commands rely on correct configuration of the `riaps-log.conf` files. This is explained below this quick reference section.)
There are two, which can be started simultaneously if desired:


- Platform: `riaps_log_server -p ${host} ${port}` captures logs written by the RIAPS platform itself.
- Applications: `riaps_log_server -a ${host} ${port}` captures logs written by RIAPS applications.
- Both: `riaps_log_server -p ${host} ${platform_port} -a ${host} ${app_port}`

These servers create `tmux` sessions called `platform` and `app` for viewing the respective logs in terminal window. To view them a user would run:
`tmux attach -t platform` for example. 

Note:
* The ports used by the platform and app log servers must be unique. 
* The arguments such as `${host}` are placeholders. A concrete example is `riaps_log_server -p 10.0.0.100 9020`.

---

# Platform Logging
##  Configuration
Each node specified in `/etc/riaps/riaps-hosts.conf` needs the socketHandler to be added the list of `[handlers]` in the `/etc/riaps/riaps-log.conf` file and the `args` in the `[handler_socketHandler]` definition needs to be modified to match the ip of the node that will run the log server. To be explicit here is an example of those elements (The ip and port will need to be modified to match your node):
```conf
...
[loggers]
keys=root,riaps.deplo.spcmon
...
[handlers]
keys=consoleHandler,socketHandler
...
[logger_riaps.deplo.spcmon]
level=INFO
handlers=consoleHandler,socketHandler
qualname=riaps.deplo.spcmon
propagate=0
...
[handler_socketHandler]
class=handlers.SocketHandler
level=DEBUG
formatter=devFormatter
args=("10.0.0.100",9020,)
```

## Usage 

Start the log server with:
```bash
$ riaps_log_server [-p PLATFORM] ${host} ${port}
```
e.g.,
```bash
$ riaps_log_server -p 10.0.0.100 9020
```

Then view the platform logs by attaching to the tmux session:
```bash
$ tmux attach -t platform
```

---

# Application Logging
##  Configuration
1. Network access to the `riaps_log_server` endpoint

If RIAPS has security enabled, each node **MUST** be given explicit access to the log server in the application deployment file. For example:
```
// RIAPS deployment file
app ExampleApplication {
    host riaps-1234.local {
        network 10.0.0.100; //IP address of riaps_app_log_server
    }
    ...
}
```
2. The application spd logging config file (`riaps-log.conf`) in the application directory uses the `spdlog` format and must include a tcp sink, such as:
```conf
[[sink]]
name = "tcp_st"
type = "tcp_sink_st"
server_host = "10.0.0.100"
server_port = 12345
lazy_connect = true

[[logger]]
name = "<ACTOR NAME>.<COMPONENT NAME>"
sinks = ["tcp_st",]
level = "trace"
```
Where the `server_host` and `port` match  your node configuration and `<ACTOR NAME>.<COMPONENT NAME>` is replaced with the name of actor and component to log e.g., `WeatherIndicator.sensor` for the [WeatherMonitor](https://github.com/RIAPS/riaps-apps/tree/master/apps-vu/WeatherMonitor/Python) application. See the [RIAPS Component Logging Tutorial](https://riaps.github.io/tutorials/logging.html) for more information.

## Usage: 
Start the log server with:
```bash
$ riaps_log_server [-a APP] ${host} ${port}
```
e.g.,
```bash
$ riaps_log_server -a 10.0.0.100 12345
```
Then view the application logs by attaching to the tmux session:

```bash
$ tmux attach -t app
```



---



