# Fabric File for Handling Multiple RIAPS Nodes Setup
The **riaps_fab** script provides tools for configuring and controlling multiple RIAPS nodes.  This can be used with large or small clusters (even a single one) of RIAPS nodes.  This section explains the tools available and how to use them.  

- To utilize the fabric tool, type the following with the command name desired.  If you do not know the command name, just type something for a command name and help information will be provided
```
riaps_fab <command_name>
```
- To get a **full list of available commands**, use:
```
riaps_fab help
```

- To setup a list of host nodes that are to be controlled by the fab command, edit the **/etc/riaps/riaps-hosts.conf** and update the **env.hosts** information. Notice that these can be either IP addresses or hostnames.  Also, the hostnames are within double quotes and is a comma separated list without spaces.
```
  # This is the hosts configuration file for the RIAPS fabfile
  [RIAPS]

  # List of remote RIAPS hosts for Fabric
  # RIAPS nodes can be addressed by their IP address or the hostname.local (found at the command prompt on the RIAPS node)
  hosts = "192.168.1.2","192.168.1.3",
          "ubuntu.local","riaps-ef9e.local"
```
- Hosts can additionally be specified explicitly with a flag (**'-H'**) followed by the list of hosts. This can be useful for debugging individual hosts or indicating the development machine (localhost).  Like the riaps-hosts.conf file, the hostnames are listed within double quotes and comma separated (without spaces).
```
riaps_fab <command_name> -H <comma_separated_host_list>
```
- Also, a locally stored riaps-hosts.conf file (or any name) can be used to configure the list of hosts.  This file can be utilized by using the **-f** followed by the absolute path and name of the host file.  This file will be used instead of the default one in **/etc/riaps/**
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
riaps_fab sys.get:riaps_apps/<appname>/log/alogfile.log,.,true -H <hostname>
```
- Running system commands can be done by providing the command desired after the fab command </br>
```sys.run:<command>```.  
  - If the command is multiworded, the command should be wrapped in both single and then double quotes.  
  - Single word commands do not need any quotes.
  - The sudo command is the same.
```
riaps_fab sys.run:'"cat riaps_install_node.sh"'
riaps_fab sys.run:lsb_release
riaps_fab sys.sudo:'"chmod 755 /usr/local/bin/riaps_fab"'
```
