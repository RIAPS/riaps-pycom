## NAME
riaps_log_server -- RIAPS Central log server.

---

### SYNOPSIS
`riaps_log_server` [-p PLATFORM (HOST, PORT)] 
`riaps_log_server` [-a APP (HOST, PORT)] 

### DESCRIPTION
`riaps_log_server` starts a log server using the specified host ip address and port.

#### OPTIONS
* **--help**
  + show this help message and exit
* **-p, --platform**
  + takes a HOST and PORT as arguments. E.g., `$ riaps_log_server -p 10.0.0.100 9020`
* **-a, --app**
  + takes a HOST and PORT as arguments. E.g., `$ riaps_log_server -a 10.0.0.100 12345`
* **-t, --trace**
* **-s, --script**

#### EXAMPLES 
See the [log server test](https://github.com/RIAPS/riaps-pycom/tree/develop/tests/LogServer)






