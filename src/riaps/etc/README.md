# RIAPS Configuration Files

This folder contains configuration files used by the RIAPS framework.  Some configuration files (such as redis.conf and riaps-ctl.glade) are specific to the RIAPS framework and are not expected to be modified by users.  But others (such as riaps.conf and riaps-log.conf) allow the user to configure the specific instance of the RIAPS framework to met the needs of their current activity.  The riaps-hosts.conf file will allow the user to indicate the RIAPS host nodes that are available in their system by indicating their hostnames.  This file is available for use when an action is needed on all hosts.  Users can customize these files on specific platforms (i.e. the host machine and/or specific target nodes) by modifying the files located in **/etc/riaps**.

> Note:  User changes made to riaps.conf, riaps-log.conf, riaps-hosts.conf will be preserved when the platform is updated (i.e. new version installed).  But the redis.conf and riaps-ctl.glade will be overwritten during the RIAPS update process.

## RIAPS Platform Configuration File (riaps.conf)

This is the main configuration file for the RIAPS Platform.  Each RIAPS node can have a different configuration setup to match the expected needs of the node hardware and system expectations.

### RIAPS Target User Name

This is the user account name that will be used to deploy and authenticate applications.  The controller system and the target nodes must have the same user name.

### Port Send/Receive Timeouts

The send and receive timeouts for messages ports in the framework can be individually configured.  The value is expressed in msec.

### Ethernet Interface

The **nic_name** indicates the ethernet interface used to communication with other RIAPS nodes. The default value is set assuming the remote target nodes are Beaglebone Black or TI SK-AM64B. `riaps-pycom` nodifies this value when creating a package intended for the VM.

#### Changing the RIAPS ethernet interface

1) Determine the desired ethernet interface

```
ifconfig
```   

2) Open riaps.conf in `nano`

```
sudo nano $RIAPSHOME/etc/riaps.conf
```   

3) Make sure the NIC name matchs the desired ethernet interface name from 'ifconfig'

```conf
# NIC name
# Typical VM interface
# nic_name = eth0 ##COMMENTED OUT
nic_name = enp0s8
```

4)  After changing the NIC name, restart the rpyc running in the background.

```
sudo systemctl restart riaps-rpyc-registry.service
```

### Discovery implementation 

There are two types of discovery implementations available: **redis** and **opendht**.  The preferred version is opendt.  To change the option used, change the following option:

```
disco_type = opendht
```

### Debug Server Options

The Python development environment in the Eclipse has a debugger that can be used
for debugging the components running on the RIAPS target nodes while the graphical
front-end of the debugger is running on the development machine. The debugger uses
the Python source code of the components located on development host.

>Note: The same debugger can also be used for debugging the RIAPS framework itself.

When an actor (or a device component that runs in its own device actor) on the target node
is started it must connect to the debugger front end that runs on the development host.
This is controlled by a configuration attribute in the **/usr/local/riaps/etc/riaps.conf**
file on the target node. The relevant part of this file on the target node
is as follows:

```
 RIAPS Debug server
# Typical debug server arguments
# ':'              -- Local host, default port
# ':1234'          -- Local host, port 1234
# '10.123.123.1:'  -- Typical mininet host VM, default port
# 'HOST:PORT'      -- Internet HOST (IP address or DNS name) and PORT (integer)

# riaps_ctrl debug server
ctrl_debug_server =

# riaps_deplo debug server
deplo_debug_server =

# riaps_disco debug server
disco_debug_server =

# riaps_actor debug server
actor_debug_server =

# riaps_device debug server
device_debug_server =
```

Suppose the debugger front-end runs on the development hosts **1.2.3.4** and we use the standard
port (i.e. 5678). If we want to debug the actors running on the target node, then this entry
must look like:

```
actor_debug_server=1.2.3.4:
```

If we want to debug the device component code from a development hosts **5.6.7.8** using the
non-standard **port 9876** then the entry should look like:

```
device_debug_server=5.6.7.8:9876
```

> Note: this configuration file affects all the actors/devices running on the target node where
the file is located.

### Application Logs

Log statements from the framework and application component code are provided on the stdout by default.  The component information can be logged to a file on the deployed target node by setting **app_logs = log** on that node.  The log file will be saved in ```~/riaps_apps/<app name>/<actor name>.log```.

### Heartbeat Options

A heartbeat message is available for both controller and RIAPS nodes.  These messages can be helpful when debugging a system issue, but they will also increase the message volume.  Therefore, the default for this option is to turn the heartbeats off.  To turn on either heartbeat, set to ```= on```.

```
ctrl_heartbeat = off
node_heartbeat = off
```

### Network Monitoring Option

This option turns **on** or **off** the network monitoring feature of RIAPS.  The current solution tends to stress the processing power of the remote nodes when many nodes are used in the system.  There are situations where this feature is desired and can be turned on with this option.

```
netmon = off
```

### Security Feature Control

Security can be turned **on** or **off** based on desired system configuration.  The default will be to turn on security features.  

```
security = on
```

The easiest way to update a system with multiple nodes to modify this option is to use the ```riaps_fab riaps.security --off``` (or ```--on```).


## RIAPS Logging Configuration File (riaps-log.conf)

This file allows configuration of the RIAPS Framework logging output to indicate what information will be available (loggers), how it will be displayed (handlers), and general output format (formatters).  The default configuration will output framework warnings (root).  If more information is needed to debug an issue, additional module information can be added by including the desired module (such as riaps.deplo.depm) in the comma separated **keys** list.  

## RIAPS Host Definition File (riaps-hosts.conf)

This file is used by **riaps_fab** to know which hosts to interact with when using riaps_fab commands.  This file should be configured when setting up a system or when hosts are added or removed.  Hostnames can either be specified as the IP address or the hostname seen when logging into the node.  The RIAPS configured remote nodes (listed as **nodes**) will have hostnames with a format of 'riaps-xxxx.local', where xxxx is that last four digits of the host's MAC address.  It is not recommended to put the VM hostname (localhost) into the **nodes** list even if a deployment node is started on the VM. The VM hostname should be listed as the **control** value.  The hostnames are enclosed in double quotes and comma separated.
