# Fabric File for Handling Multiple BBB Setup
The **fabfile.py** provides tools for configuring and controlling multiple BBBs.  This can be used with large or small clusters (even a single one) of BBBs.  This section explains the tools available and how to use them.  The fabfile.py can be customized to your system (and should be).  Use this tool as guidance for ideas of functions that could be used to work with multiple host nodes.
- To utilize the fabric tool, type the following with the command name desired.  If you do not know the command name, just type something and help information will be provided
```
fab <command_name>
```
- To get a **full list of available commands**, use:
```
fab help
```

- To setup a list of host nodes that are to be controlled by the fab command, edit the **fabfile/riaps_hosts.py** and update the **env.hosts** information
```
# ---- START OF EDIT HERE ----
# List of bbb hosts
# BBBs can be addressed by their IP address or the hostname.local (found at the command prompt on the BBB)
env.hosts = ['192.168.0.101', 'bbb-ff98.local']
# ----  END OF EDIT HERE  ----
```
- Hosts can additionally be specified explicitly with a command. This can be useful for debugging individual hosts
```
fab <command_name> -H <comma_separated_host_list>
```

## Most useful commands
- To check that all host nodes are communicating, use the **sys.check** command
```
fab sys.check
```
- To update host nodes to the latest RIAPS platform release, use the **riaps.updates** command
```
fab riaps.update
```
- Start deployment on all host nodes using
```
fab deplo.start
```
- Kill all RIAPS actors and deployments
```
fab riaps.kill
```
- Upload a file to all hosts. **Make sure to update fabile/__init__.py** to reflect the local paths of your machine.
```
fab riaps.put <fileName>
```

# Eclipse External Tool Launch Files

If using eclipse to work on RIAPS application development, there are several external tool launch files available to run the RIAPS framework tools.  
These tools can be imported into the eclipse environment using "Run/Debug" and "Launch Configurations" options in the "Import Wizard".  When 
importing these launch configurations, the "Build before launch" flag is automatically checked under the "Build" tab of the configuration.  ***Make
sure to uncheck this option.***

- riaps_ctrl.launch:  starts the RIAPS controller
- riaps_deplo.launch:  starts the RIAPS deployment manager on the host environment


# Utilities for Mininet Operations
This is for RIAPS developers - **NOT for APP developers**.

The scripts are as follows:
- riaps.mn: launches a simple mininet configuration, uses sshd.py. RIAPS environment variables must be set.  

- riaps-mn.ctrl: script to be run on the 'lead' node of mininet, launches the registry and the controller

- riaps-mn-dns.ctrl: similar to the riaps-mn.ctrl, but it also launches a small dns server so that symbolic names can be used to access the mininet nodes. NOT RECOMMENDED.

- riaps-mn.node : script to be run on the 'slave' nodes of mininet, launches the deplo manager

- pytinydns.py, pytinydns.host, pytinydns.conf: the script for the small dns server (used by riaps-mn-dns.ctrl), and its configuration files.

- sshd.py: starts mininet with a 4 node network, each node running sshd. Used for mininet-based testing.
