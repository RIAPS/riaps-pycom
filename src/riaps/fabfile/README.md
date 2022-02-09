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
  > *Note*: If a control host is specified that is used as a target host, it must be
  specified using the **same** name, both in the `control` and the `nodes` setting.     

	```
  # This is the hosts configuration file for the RIAPS fabfile
  [RIAPS]

  # List of remote RIAPS hosts for Fabric
  # RIAPS nodes can be addressed by their IP address or the hostname.local (found at the command prompt on the RIAPS node)
  nodes = ["192.168.1.2","192.168.1.3","ubuntu.local","riaps-ef9e.local"]
  control = "ubuntu.local"
	```

- Hosts can be specified explicitly with a flag (`-H`) followed by the comma-separated
  list of hosts. In this case the `fab` command will be executed *only* on the selected
  hosts. This can be useful for debugging individual hosts. Like the `riaps-hosts.conf`
  file, the hostnames are listed within double quotes and comma separated (without spaces).
	```
	riaps_fab <command_name> -H <comma_separated_host_list>
	```
- Also, a local file compatible with the syntax of `riaps-hosts.conf` can be used to configure the list of hosts.  This file can be utilized by using the `-f` flag followed by the absolute path and name of the file.  This file will be used instead of the default one in `/etc/riaps/`.
	```
	riaps_fab <command_name> -f <absolute path and filename of host file>
	```
- The `fab` script uses *roles* to form group of nodes, and commands can be executed
only on specific groups. Based on the `nodes` and the `control` settings, two more groups are determined, as shown on the table below.  

	| Group     | Content            | Specified in                       |
	| ----------|------------------- |------------------------------------|
	| `nodes`   | nodes running apps | `riaps-hosts.conf` or command line |
	| `control` | control host       | optional in `riaps-hosts.conf` |
	| `remote`  | all non-control nodes | `nodes` - `control` |
	| `all`     | all nodes and control | `nodes` *union* `control` |

- 	Roles for the the nodes the `fab` command must be executed on can be specified as command line arguments. Only the above four role names can be used.

	```
	riaps_fab <command_name> -R <comma-separated_list_of_roles>
	```
	The `<command_name>` will *only* be executed on the hosts that appear in the selected
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

- The `riaps_fab` script can be called from the `riaps_ctrl` tool. In this case the `control` host will be where the script is running, and the `nodes` will be determined based on the *currently* connected nodes.

	>Note that the `riaps_hosts.conf` file is ignored in this case.

## Most Useful Commands

Command arguments are placed after a `:` and are comma separated. Parameters listed without brackets are required arguments.  ```[]``` in commands indicate optional arguments with the parameter description within the square brackets.  

- To check that all nodes are communicating
```
riaps_fab sys.check
```
- To update all nodes to the latest RIAPS platform release (using apt-get)
```
riaps_fab riaps.update
```
- Start the deployment service on all nodes using
```
riaps_fab deplo.start
```
- Stop the deployment service on all remote nodes using
```
riaps_fab deplo.stop
```
- In the event reset any hanging RIAPS processes
```
riaps_fab riaps.reset
```

- Reboot remote nodes
```
riaps_fab sys.reboot
```

- Shutdown remote nodes, optionally providing when and why information.  Default **when** is `now`
```
riaps_fab sys.shutdown:[when],[why]
```

## Command Descriptions

Additional `riaps_fab` commands available and described below.

### Deployment Commands

Start and stop commands were listed in the "Most Useful Commands" section above.

- Restart the deployment service on remote nodes
```
riaps_fab deplo.restart
```

- Disable the deployment service on remote nodes.  This keeps the deployment service from restarting after booting up the system.
```
riaps_fab deplo.disable
```

- Enable the deployment service on remote nodes
```
riaps_fab deplo.enable
```

- Get the status of the deployment service on all nodes.  This prints each node's output to the screen.  Optionally, the number of output lines desired (per node) and a search criteria can be provided.  Default is 10 output lines.
```
riaps_fab deplo.status:[# of lines],[grep args]
```

- Get the journal logs from the deployment service on all nodes.  This prints each node's output to the screen.  Optionally, the number of output lines desired (per node) and a search criteria can be provided.  Default is 10 output lines.
```
riaps_fab deplo.journal:[# of lines],[grep args]
```

- Manually start the deployment function on the remote nodes (not using the systemd service).  The deployment log will be saved on the node in the base directory (~/riaps-hostname.log).
```
riaps_fab deplo.startManual
```

- Start the deployment service serially on the remote nodes with a specified delay (default 1 second)
```
riaps_fab deplo.slowStart:[delay]
```

### RIAPS Commands

Update and reset commands were listed in the "Most Useful Commands" section above.

- To turn on or off the RIAPS security features
```
riaps_fab riaps.securityOn
riaps_fab riaps.securityOff
```

- To install the latest development packages release (.deb) on all nodes.  The latest versions of the RIAPS packages should be located in the directory where this command is run.  To keep the current configuration files on the remote nodes, add `True` to indicate the value of the **keepConfig** parameter. The default is to override the configuration files (keepConfig = False).
```
riaps_fab riaps.install:[keepConfig]
```

- To uninstall all RIAPS packages from all nodes
```
riaps_fab riaps.uninstall
```

- To update the feature and setup information for RIAPS, modify a copy of the [riaps.conf](https://github.com/RIAPS/riaps-pycom/blob/master/src/riaps/etc/riaps.conf) file locally and then transfer the file to the RIAPS nodes.
```
riaps_fab riaps.updateConfig
```
>Note: If the control node is also listed in the nodes list (in the /etc/riaps/riaps-hosts.conf file), then this file will also be copied to this node The control node typically has a different **nic_name** in this file and will need to be modified to the appropriate value.

- To update the logging output for RIAPS components, modify a copy of the [riaps-log.conf](https://github.com/RIAPS/riaps-pycom/blob/master/src/riaps/etc/riaps-log.conf) file locally and then transfer the file to the RIAPS nodes.
```
riaps_fab riaps.updateLogConfig
```
>Note: If the control node is also listed in the nodes list (in the /etc/riaps/riaps-hosts.conf file), then this file will also be copied to this node.

- For debugging RIAPS application issues, the developer can create log files to trace the output of the RIAPS components. These log files are stored in the node application directory, which is available when the application is load, running or stopped. Remember that this directory is removed when the application is removed, so the files should be retrieved before the application is removed. Using this command, all available application log files (.log) will be retrieved from each node for the application identified (**app_name**). For each node, these files will be placed under a `logs/<hostname>` directory.
```
riaps_fab riaps.getAppLogs:app_name
```

- For debugging RIAPS platform issues, a log file of the RIAPS deployment service from each node can be retrieved. These files will be placed under a `logs/` directory with each node indicated in the filename:  `riaps-deplo-<hostname>.log`.  This will contain the log information for the current day.
```
riaps_fab riaps.getSystemLogs
```

- To rekey the remote nodes with newly generated ssh keys and RIAPS certificates use the **updateNodeKey** command.  Make sure that **ALL the remote nodes desired** are communicating prior to running this command, this can be done by using the sys.check command to see that each node is available. This rekeying process does turn off the remote node's password ssh access by access. To keep the password access, add `True` for the **keepPasswd** parameter.
```
riaps_fab riaps.updateNodeKey:[keepPasswd]
```

- To start the RIAPS controller using `riaps_fab`. The controller window will appear the same as using `riaps_ctrl` on the command line.
```
riaps_fab riaps.ctrl
```

- Each RIAPS control VM is setup with a default apt repository key. If the key needs updating, this command will retrieve the current RIAPS apt repository key.
```
riaps_fab riaps.updateAptKey
```

- Configure remote nodes (eth0) to use control host as their default gateway
```
riaps_fab riaps.configRouting
```

### System Commands

Check, reboot and shutdown commands were listed in the "Most Useful Commands" section above.

- Print the native architecture of all the nodes; for example amd64, armhf, arm64
```
riaps_fab sys.arch
```

- Any Linux command can be run on all nodes using the **run** command with the console output feedback provided. Single word commands can be placed after the `:`, but multiworded commands should be wrapped in both a single and then double quotes after the `:`.  Environment variables will be evaluated on the remote nodes as the command is executed. Here are some examples:
```
riaps_fab sys.run:lsb_release
riaps_fab sys.run:'"ls -al $RIAPSAPPS"'
riaps_fab sys.run:'"cat riaps_install_node.sh"'
riaps_fab sys.sudo:'"chmod 755 /usr/local/bin/riaps_fab"'
```

- Any priviledge Linux command that requires `sudo` can be run the same way as `sys.run`, but using `sys.sudo` instead.
```
riaps_fab sys.sudo:'"ls -al /etc/riaps"'
```

- When debugging a system setup, the **getConfig** command can be used to pull the relevant information into separate files for all the nodes.  This information can then be passed to RIAPS experts to assist in understanding how the system is configured at that time.  These files will be placed under a `logs/` directory with each node indicated in the filename:  `sysconfig-<hostname>.log`.  
```
riaps_fab sys.getConfig
```

- The system journal run continuously with no regard to login session. So to isolate testing data, the system journal can be cleared. This command removes all logs in `/run/log/journal/` from all nodes.
```
riaps_fab sys.clearJournal
```

- Change systemd journal log file size on all remote nodes by changing the value in the system configuration file.  Specify the size in bytes (K, M, G, T, P, E), default is 64M.
```
riaps_fab sys.setJournalLogSize:size
```

- Flush the iptables on remote nodes
```
riaps_fab sys.flushIPTables
```


### Time and Timesync Commands

- Get the system date from all nodes
```
riaps_fab time.date
```

- Run date update using rdate and time.nist.gov for reference on all nodes
```
riaps_fab time.rdate
```

- Compare the system time for all nodes.  The resulting files from each node are placed in a `logs/` directory with the file indicated as 'riaps-time-<hostname>.log'
```
riaps_fab time.compare
```

- Check the status of RIAPS timesync on all nodes
```
riaps_fab time.status
```

- Configure RIAPS timesync on specific nodes (typically using -H option).  The desired **role** to configure must be provided in the command. See https://github.com/RIAPS/riaps-timesync for information on available timesync roles.
```
riaps_fab time.config:role
```

- Restart RIAPS timesync
```
riaps_fab time.restart
```

- Check control node to see if the PTP process is running, results provide relevant active process list.
```
riaps_fab time.checkPTP
```
