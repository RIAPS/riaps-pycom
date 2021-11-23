# `fabric` script for managing multiple RIAPS nodes
The `riaps_fab` script provides tools for configuring and controlling multiple RIAPS nodes. 
This script can be used with large or small clusters (even a single one) of RIAPS nodes. 
This section explains the tools available and how to use them.  

- To utilize the fabric tool, type the following with the desired fab command name.  
	```
	riaps_fab <command_name>
	```
- To get a full list of available commands use:   
	```
	riaps_fab help
	```
  
- To setup list of host nodes that the `fab` command controls, edit the
  file `/etc/riaps/riaps-hosts.conf` and set the `nodes`, and, optionally, the `control` 
  settings. The `nodes` list specifies all the RIAPS hosts that serve as *target* 
  hosts to run applications. The `control` setting specifies the host where the RIAPS 
  controller application is running. The latter one is optional and it defaults to 
  the host the `riaps_fab` script is executed on. The hostnames can be DNS names 
  or IP address, **always** as quoted strings.    
  *Note*: If a control host is specified that is used as a target host, it must be 
  specified using the **same** name, both in the `control` and the `nodes` setting.     
 
	```
  # Example hosts configuration file 
  [RIAPS]
  # List of remote RIAPS hosts for Fabric
  # RIAPS nodes can be addressed by their IP address or their hostname 
  # The .local suffix maybe required on some networks 
  nodes = [ "192.168.1.2","192.168.1.3", "devvm.local","riaps-ef9e.local" ]
  # Optional control host
  control = "devvm.local"
  ```
	
- Hosts can be specified explicitly with a flag (`-H`) followed by the comma-separated 
  list of hosts. In this case the `fab` command will be executed *only* on the selected 
  hosts. This can be useful for debugging individual hosts. Like the `riaps-hosts.conf` 
  file, the hostnames are listed within double quotes and comma separated (without spaces).
	```
	riaps_fab <command_name> -H <comma_separated_host_list> 
	```
- Also, a local file compatible with the syntax of `riaps-hosts.conf` can be used to configure the list of hosts.  
  This file can be utilized by using the `-f` flag followed by the absolute path and name of the file.  
  This file will be used instead of the default one in `/etc/riaps/`.
	```
	riaps_fab <command_name> -f <absolute path and filename of host file>
	```
- The `fab` script uses *roles* to form group of nodes, and commands can be executed 
only on specific groups. Based on the `nodes` and the `control` settings, two more groups 
are determined, as shown on the table below.  
  
	| Group     | Content            | Specified in                       |
	| ----------|------------------- |------------------------------------|
	| `nodes`   | nodes running apps | `riaps-hosts.conf` or command line |
	| `control` | control host       | optional in `riaps-hosts.conf` |
	| `remote`  | all non-control nodes | `nodes` - `control` |
	| `all`     | all nodes and control | `nodes` *union* `control` |  

 
	Roles for the the nodes the `fab` command must be executed on can be sepcified as command 
	line arguments. Only the above four role names can be used.
	
	```
	riaps_fab <command_name> -R <comma-separated_list_of_roles> 
	```
	The `<command_name>` will be executed on the hosts only *only* that appear the selected 
	role. The hosts are specific in the `riaps-hosts.conf` file.

- Both the `-H` and `-R` arguments can be specified on the command line.
	```
	riaps_fab <command_name> -H <comma_separated_host_list> -R <comma-separated_list_of_roles> 
	```
	In this case, the following algorithm is used:
	1. The `riaps-hosts.conf` file is loaded and parsed
	2. The hosts that do *not* appear in the `-H` argument list are removed.
	3. The roles that do *not* appear in the `-R` argument list are removed.
	4. The `<fabcmd>` is executed on the remaining hosts and roles. 

- The `riaps_fab` script can be called from the `riaps_ctrl` tool. In this case the `control` 
host will be the one the script is running on, and the `nodes` will be determined based 
on the *currently* connected nodes. Note that the `riaps_hosts.conf` file is ignored 
in this case.
 
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
- Upload a file from the current working directory to all hosts.
```
riaps_fab sys.put:<fileName>
```
- Get files from all or specific hosts. This example shows how to grab application saved log files from the application deployment folder (the folder is protected, so sudo=true)
```
riaps_fab sys.get:riaps_apps/<appname>/log/alogfile.log,.,true -H <hostname>
```
- Running system commands can be done by providing the complete command lined as an 
argument to the command.   
<br> 
`sys.run:<command>`.  
 	- If the command is multiworded, the command should be wrapped in both single and then double quotes.  
 	- Single word commands do not need any quotes.
  - The `sys.sudo` command works the same way.
  - For example:
	```
	riaps_fab sys.run:'"cat riaps_install_node.sh"'
	riaps_fab sys.run:lsb_release
	riaps_fab sys.sudo:'"chmod 755 /usr/local/bin/riaps_fab"'
	```

 

