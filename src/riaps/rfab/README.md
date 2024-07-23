# `riaps_fab` tool for managing multiple RIAPS nodes
`riaps_fab` provides tools for configuring and controlling multiple RIAPS nodes.
It can be used with large or small clusters (even a single one) of RIAPS nodes.
This section explains the tools available and how to use them.  

- General use:  
	```
	riaps_fab  [GENERAL FLAGS] <command_name> [COMMAND FLAGS]
	```
- View all commands:   
	```
	riaps_fab --list
	```
- View command-specific help
	```
	riaps_fab -h <command_name>
	```

- To setup list of host nodes that the `riaps_fab` controls, edit the
  file `$RIAPSHOME/etc/riaps-hosts.conf` and set the `nodes`, and, optionally, the `control`
  settings. The `nodes` list specifies all the RIAPS hosts that serve as *target*
  hosts to run applications. The `control` setting specifies the host where the RIAPS
  controller application is running. The latter one is optional and it defaults to
  the host `riaps_fab` is executed from. The hostnames can be DNS names
  or IPv4 addresses, **always** as quoted strings.    
  > *Note*: If a control host is specified to be used as a target host, it must be
  specified using the **same** name, both in the `control` and the `nodes` setting.     

	```
  # This is the hosts configuration file for RIAPS
  [RIAPS]

  # List of remote RIAPS hosts
  # RIAPS nodes can be addressed by their IP address or the hostname.local (found at the command prompt on the RIAPS node)
  nodes = ["192.168.1.2","192.168.1.3","ubuntu.local","riaps-ef9e.local"]
  control = "riaps-VirtualBox.local"
	```
## General Flags
- `--host(-H)  <hostname>`: Specify target at runtime
	- Repeat the flag for each host. This can be useful for debugging individual hosts.
- `-v` : Verbose mode
	- Show remote results regardless of success/failure.
- `--role(-r) <rolename>`: Specify target role

  `riaps_fab` uses *roles* to form groups of nodes, and commands can be executed
for specific groups. Based on the `nodes` and the `control` settings, two more roles are populated, shown on the table below.  

	| Role      | Description        | Members                  |
	| ----------|------------------- |------------------------------------|
	| `nodes`   | nodes running apps | Listed in `riaps-hosts.conf` |
	| `control` | control host       | Listed in `riaps-hosts.conf` |
	| `remote`  | all non-control nodes | `nodes` *\* `control` |
	| `all`     | all nodes and control | `nodes` *union* `control` |

- `riaps_fab` can be called from the `riaps_ctrl` GUI. In this case the `control` host will be where `riaps_ctrl` is running, and the `nodes` will be determined based only on the *currently* connected nodes.

	>Note that the `riaps_hosts.conf` file is ignored in this case.

## Most Useful Commands

> NOTE: CLI tools like `riaps_fab`, by convention, don't print anything if the task succeeded. Any warnings or errors will always be printed. To always see output, success or failure, use the `-v` (verbose) general option.

- To check that all nodes are online and accessible
```
riaps_fab sys.check
```
- To update nodes to the latest RIAPS platform release (using apt-get). The updates both ***pycom*** and ***timesync*** packages.
```
riaps_fab riaps.update
```
- Hard stop all RIAPS processes, delete applications, and clean system state
```
riaps_fab riaps.reset
```
- Reboot remote nodes
```
riaps_fab sys.reboot
```
- Shutdown remote nodes. The default shutdown wait time is 1 minute, to wait longer use the `--when` option followed by a time in minutes.  A log message about the shutdown reason can be added by using the `--why` option.
```
riaps_fab sys.shutdown
```


## Command Descriptions

Additional `riaps_fab` commands available and described below.

### Deployment Commands

- Stop the deployment service on remote nodes
```
riaps_fab deplo.stop
```

- Start deployment service on remote nodes
```
riaps_fab deplo.start
```
>Note: When RIAPS is installed on the nodes, the default is to automatically start the deployment service. So this command is only necessary if the deployment service was previously stopped.

- Restart the deployment service on remote nodes
```
riaps_fab deplo.restart
```

- Disable the deployment service on remote nodes.  This keeps the deployment service from restarting after booting up the system.
```
riaps_fab deplo.disable
```

- Enable the deployment service on remote nodes (does not also start the service)
```
riaps_fab deplo.enable
```

- Get the status of the deployment service on all nodes.  This prints each node's output to the screen.  Optionally, the number of output lines desired (per node) and a `grep` filter string can be provided.  Default is 10 output lines.
```
riaps_fab deplo.status [-n NUM] [--grep STRING]
```

- Get the journal logs from the deployment service on all nodes.  This prints each node's output to the screen.  Optionally, the number of output lines desired (per node) and a `grep` filter string can be provided.  Default is 10 output lines.
```
riaps_fab deplo.journal [-n NUM] [--grep STRING]
```

- Manually start the deployment function on the remote nodes (not using the systemd service).  The deployment log will be saved on the node in the base directory (~/riaps-hostname.log).
```
riaps_fab deplo.startManual
```

### RIAPS Commands

Update and reset commands were listed in the "Most Useful Commands" section above.

- To turn on or off the RIAPS security features
```
riaps_fab riaps.security --on
riaps_fab riaps.security --off
```

- To install a locally built RIAPS platform package (.deb), either `pycom` or `timesync`.  This command should be run from the same directory containing the package file.  To overwrite the configuration files on the remote nodes, add `--clean`. The default is to keep the existing configuration.
```
riaps_fab riaps.install pycom [--clean]
riaps_fab riaps.install timesync [--clean]
```

- Uninstall a RIAPS platform package. Add `--purge` to purge the configuration files as well. 
```
riaps_fab riaps.uninstall pycom [--purge]
riaps_fab riaps.uninstall timesync [--purge]
```

- To update the feature and setup information for RIAPS, modify a copy of the [riaps.conf](https://github.com/RIAPS/riaps-pycom/blob/master/src/riaps/etc/riaps.conf) file locally and then transfer the file to the RIAPS nodes.
```
riaps_fab riaps.updateRiapsConfig
```
>Note: If the control node is also listed in the nodes list (in the /etc/riaps/riaps-hosts.conf file), then this file will also be copied to this node The control node typically has a different **nic_name** in this file and will need to be modified to the appropriate value.

- To install a local RIAPS platform logging configuration (`riaps-log.conf`). 
```
riaps_fab riaps.updateLogConfig
```
>Note: If the control node is also listed in the nodes list (in the /etc/riaps/riaps-hosts.conf file), then this file will also be copied to this node.

- For debugging RIAPS applications, `riaps.conf` can tell actors to log to separate files. These log files are stored in the node application directory, which is accessible when the application is stopped. Remember that this directory is removed when the application is removed, so the files should be retrieved before the application is removed. Using this command, all available application log files (.log) will be retrieved from each node for the application identified (**app_name**). For each node, these files will be placed under a `logs/<hostname>` directory.
```
riaps_fab riaps.getAppLogs app_name
```

<!-- - To rekey the remote nodes with newly generated ssh keys and RIAPS certificates use the **updateNodeKey** command.  Make sure that **ALL the remote nodes desired** are communicating prior to running this command, this can be done by using the sys.check command to see that each node is available. This rekeying process does turn off the remote node's password ssh access by access. To keep the password access, add `True` for the **keepPasswd** parameter.
```
riaps_fab riaps.updateNodeKey:[keepPasswd]
``` -->

- Each RIAPS control VM is setup with a default apt repository key. If the key needs updating, this command will retrieve the current RIAPS apt repository key.
```
riaps_fab riaps.updateAptKey
```


### System Commands

Check, reboot and shutdown commands were listed in the "Most Useful Commands" section above.

- Print the native architecture of all the nodes; for example amd64, armhf, arm64.
```
riaps_fab sys.arch
```

- Any Linux command can be run on all nodes using the **run** command with the console output feedback provided.  Environment variables will be evaluated on the remote nodes as the command is executed. Here are some examples:
```
riaps_fab sys.run lsb_release
riaps_fab sys.run "ls -al $RIAPSAPPS"
riaps_fab sys.run "cat riaps_install_node.sh"
riaps_fab sys.sudo "chmod 755 /usr/local/bin/riaps_fab"
```

- Any priviledged Linux command that requires `sudo` can be run the same way as `sys.run`, but using `sys.sudo` instead.
```
riaps_fab sys.sudo "ls -al /etc/riaps"
```

- To copy a file from remote nodes to a development machine use the **get** command. The desired remote file must be located in a folder within the remote `riaps` user's folder (`/home/riaps`). The desired remote filename is specified using the `--remote-file=` option and can be a relative path from the user's home folder. If a new name is desired for the file on the development machine, use the `--name=` option to indicate the new name. The copied file could be placed in a different folder by using the `--local-dir=` option, which will create the folder if it does not already exist.
```
riaps_fab sys.get --remote-file="remote-data.txt"
riaps_fab sys.get --remote-file="notes/remote-data.txt" --name="remote-data-notes.txt" --local-dir="test-results"
```

- To copy a local file over to the remote node's `riaps` user folder (`/home/riaps`), use the **put** command. Use the `--local-file=` option to specify the location of the file. Relative paths are possible from the current local directory. The remote node directory option (`--remote-dir=`) indicates where to place the file within the `riaps` users folder. This remote directory must already exist.
```
riaps_fab sys.put --local-file="test-setup.py" 
riaps_fab sys.put --local-file="test-setup.py" --remote-dir="temp"
```

- When debugging a system setup, the **getConfig** command can be used to pull the relevant information into separate files for all the nodes.  This information can then be passed to RIAPS experts to assist in understanding how the system is configured at that time.  These files will be placed under a `logs/` directory with each node indicated in the filename:  `sysconfig-<hostname>.log`.  
```
riaps_fab sys.getConfig
```

- The system journal runs continuously with no regard to login session. To isolate testing data, the system journal can be cleared. This command removes all logs in `/run/log/journal/` from all nodes.
```
riaps_fab sys.clearJournal
```

- Change systemd journal log file size on all remote nodes by changing the value in the system configuration file.  Specify the size in MB, default is 64MB.
```
riaps_fab sys.setJournalLogSize SIZE
```

- Flush the iptables on remote nodes
```
riaps_fab sys.flushIPTables
```


### Time and Timesync Commands

- Get the system date & time from all nodes
```
riaps_fab time.date
```

- Sync system time to NTP
```
riaps_fab time.rdate
```

<!-- - Compare the system time for all nodes.  The resulting files from each node are placed in a `logs/` directory with the file indicated as 'riaps-time-<hostname>.log'
```
riaps_fab time.compare
``` -->

- Check the status of RIAPS timesync on all nodes
```
riaps_fab time.status
```

- Configure RIAPS timesync to the desired **role**. See https://github.com/RIAPS/riaps-timesync for information on available timesync roles.
```
riaps_fab time.config ROLE
```

- Restart RIAPS timesync
```
riaps_fab time.restart
```
<!-- 
- Check control node to see if the PTP process is running, results provide relevant active process list.
```
riaps_fab time.checkPTP
``` -->
