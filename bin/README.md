# Fabric File for Handling Multiple BBB Setup
The fabfile.py provides tools for configuring and controlling multiple BBBs.  This can be used with large or small clusters (even a single one) of BBBs.  This section explains the tools available and how to use them.  The "fabfile.py" can be customized to your system (and should be).  Use this tool as guidance for ideas of functions that could be used to work with multiple host nodes.	
- To utilize the fabric tool, type the following with the command name desired.  If you do not know the command name, just type something and help information will be provided
```
	$ fab <command_name>
```

- To setup a list of host nodes that are to be controlled by the fab command, edit the "fabfile.py" and update the "env.hosts" information
```
	# ---- START OF EDIT HERE ----
	# List of bbb hosts
	# BBBs can be addressed by their IP address or the hostname.local (found at the command prompt on the BBB)
	env.hosts = ['192.168.0.101', 'bbb-ff98.local']
	# ----  END OF EDIT HERE  ----
```

## For host node maintenance
- To check that all host nodes are communicating, use the *hello_hosts* command
```
	$ fab hello_hosts
```
- To update host nodes to the latest RIAPS platform release, use the *update_riaps* command
```
	$ fab update_riaps
```

## To control RIAPS operation (manual control)
- RIAPS controller can be launched on a control host sytem using
```
	$ fab riaps
```
- Start deployment on all host nodes using
```
	$ fab deplo
```

## To control RIAPS services (for more automation)
	- Start the deployment on the host nodes when the system is booted up with *startDeplo*.  This will also start the discovery process. 
	- Turn the deployment service off on the host nodes by using *stopDeplo*.  This will also stop and disable the discovery service.
	- When using the RIAPS services, the application logs are stored in the system logs with a tag for the service.  To pull this information into your own file, use the *createDeployLogs* command.  These logs are continuous.  So if you want only the logs from the current testing set, first *clear_journal_log*.
- To control activity on RIAPS host nodes use either *stop*, *halt*, or *reboot*.  The *halt* should be done prior to powering down the hosts.

## Time synchronization functions 
	- *timeStamp* will compare the clocks on the hosts
	- *checkPTP* checks to see if ptp is running on the control host

## System utilities available	
	- Transfer files between the control host and the host nodes use the following command.  Be sure to edit the fabfile.py to find the right locations of where to get and place the files.  If transferring to a system location, use_sudo=True.
		*fileTransferFrom* will transfer files from host nodes to the control host
		*fileTransferTo* will transfer files to the host nodes from the control host 
	- Configure routing in a cluster that has a gateway to the internet using *config_routing*.  Be sure to edit the fabfile.py to update the gateway address.

# Utilities for Mininet Operations
This is for RIAPS developers - NOT for APP developers.

The scripts are as follows:
- riaps.mn: launches a simple mininet configuration, uses sshd.py. RIAPS environment variables must be set.  
- riaps-mn.ctrl: script to be run on the 'lead' node of mininet, launches the registry and the controller
- riaps-mn-dns.ctrl: similar to the riaps-mn.ctrl, but it also launches a small dns server so that
  symbolic names can be used to access the mininet nodes. NOT RECOMMENDED.
- riaps-mn.node : script to be run on the 'slave' nodes of mininet, launches the deplo manager
- pytinydns.py, pytinydns.host, pytinydns.conf: the script for the small dns server (used by riaps-mn-dns.ctrl),
  and its configuration files.
- sshd.py: starts mininet with a 4 node network, each node running sshd. Used for mininet-based testing.
