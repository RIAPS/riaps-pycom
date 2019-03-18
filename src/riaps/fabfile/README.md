# Fabric File for Handling Multiple BBB Setup
The **riaps_fab** script provides tools for configuring and controlling multiple BBBs.  This can be used with large or small clusters (even a single one) of BBBs.  This section explains the tools available and how to use them.  

- To utilize the fabric tool, type the following with the command name desired.  If you do not know the command name, just type something for a command name and help information will be provided
```
riaps_fab <command_name>
```
- To get a **full list of available commands**, use:
```
riaps_fab help
```

- To setup a list of host nodes that are to be controlled by the fab command, edit the **/usr/local/riaps/etc/riaps-hosts.conf** and update the **env.hosts** information. Notice that these can be either IP addresses or hostnames.
```
  # ---- START OF EDIT HERE ----
  # List of bbb hosts
  # BBBs can be addressed by their IP address or the hostname.local (found at the command prompt on the BBB)
  env.hosts = ['192.168.1.2','192.168.1.3','ubuntu.local','bbb-ef9e.local']
  # ----  END OF EDIT HERE  ----
```
- Hosts can additionally be specified explicitly with a flag (**'-H'**) followed by the list of hosts. This can be useful for debugging individual hosts or indicating the development machine (localhost).
```
riaps_fab <command_name> -H <comma_separated_host_list>
```
- Also, a locally stored riaps-hosts.conf file (of any name) can be used to configure the list of hosts.  This file can be utilized by using the **-f** followed by the absolute path and name of the host file.  This file will be used instead of the default one in **/usr/local/riaps/etc/**
```
riaps_fab <command_name> -f <absolute path and filename of host file>
```

## Most useful commands
- To check that all host nodes are communicating, use the **sys.check** command
```
riaps_fab sys.check
```
- To update host nodes to the latest RIAPS platform release, use the **riaps.updates** command
```
riaps_fab riaps.update
```
- Start deployment on all host nodes using
```
riaps_fab deplo.start
```
- Stop deployment and any running applications
```
riaps_fab deplo.stop
```
- Kills any hanging RIAPS processes. Should only be called after deplo.stop
```
riaps_fab riaps.kill
```
- Upload a file to all hosts. **Make sure to update fabile/__init__.py** to reflect the local paths of your machine.
```
riaps_fab sys.put <fileName>
```
- Get files from all or specific hosts. This example shows how to grab application saved log files from the application deployment folder (the folder is protected, so sudo=true) 
```
riaps_fab sys.get:riaps_apps/<appname>/log/*,.,true -H <hostname>
```
