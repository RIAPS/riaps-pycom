# Using RIAPS Log Servers
RIAPS logs can be viewed in real-time for both local and remote nodes using the RIAPS log servers. 
There are two, which can be started simultaneously if desired:

- `riaps_log_server -p ${host} ${port}` captures logs written by RIAPS applications
- `riaps_log_server -a ${host} ${port}` captures logs written by the RIAPS platform itself

These servers create a `tmux` session for viewing all node logs in a single terminal window

---

# Application Logs: `riaps_log_server -a ${host} ${port}`
When developing RIAPS apps, viewing log output can be very useful. To view application logs, RIAPS nodes need:
1. Network access to the `riaps_log_server` endpoint
2. An application logging config file (`riaps-log.conf`)

Start the log server with:
```bash
$ riaps_log_server [-a APP] ${host} ${port}
```
This creates a tmux session named "app".

View the app logs by attaching to the tmux session with:
```bash
$ tmux attach -t app
```

## 1) Network access to the `riaps_log_server` endpoint

If RIAPS has security enabled, each node **MUST** be given explicit access to the log server in the application deployment file. For example:
```
// RIAPS deployment file
app ExampleApplication {
    host riaps-1234.local {
        network 10.0.0.2; //IP address of riaps_app_log_server
    }
    ...
}
```



## 2) An application logging config file (`riaps-log.conf`)
Using the `spdlog` format, `riaps-log.conf` should use either `tcp_sink_st` or `tcp_sink_mt`, such as:
```conf
[[sink]]
name = "tcp_st"
type = "tcp_sink_st"
server_host = "<APP_LOG_SERVER_IP_ADDR, default localhost>"
server_port = <APP_LOG_SERVER_PORT, default 12345>
lazy_connect = false

[[logger]]
name = "<ACTOR NAME>.<COMPONENT NAME>"
sinks = ["tcp_st",]
level = "trace"
```
See the [RIAPS Component Logging Tutorial](https://riaps.github.io/tutorials/logging.html) for more info

---

# Platform Logs: `riaps_log_server -p ${host} ${port}`
Sometimes it's useful to see log outputs from the RIAPS platform when debugging.
Run:
```bash
$ riaps_log_server [-p PLATFORM] ${host} ${port}
```
Then view the platform logs by attaching tmux:
```bash
$ tmux attach -t platform
```

## Configure Platform Logging
Each remote node needs the following added to its `riaps-log.conf`. (Note: not the config with the application code, but the one in $RIAPSHOME/etc/)
```conf
[handler_socketHandler]
class=handlers.SocketHandler
level=...
formatter=...
args=("<PLATFORM LOG SERVER IP>",<PLATFORM LOG SERVER PORT>,)
```
Add the key `socketHandler` to the keys list under `[handlers]`. Then, adding `socketHandler` to any logger will also send those logs `riaps_platform_log_server`.