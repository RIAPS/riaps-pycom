# Eclipse External Tool Launch Files

If using eclipse to work on RIAPS application development, there are several external tool launch files available to run the RIAPS framework tools.  
These tools can be imported into the eclipse environment using "Run/Debug" and "Launch Configurations" options in the "Import Wizard".  When
importing these launch configurations, the "Build before launch" flag is automatically checked under the "Build" tab of the configuration.  ***Make
sure to uncheck this option.***

- riaps_ctrl.launch:  starts the RIAPS controller
- riaps_deplo.launch:  starts the RIAPS deployment manager on the host environment
- rpyc_registry.launch:  starts the background rpyc_registry tool used by the RIAPS Controller.  This external tool is no longer necessary since this is automatically started using systemd on the development environment where the controller will be run.  It is available here in case it is desired to be run manually instead of in the background.


# Utilities for Mininet Operations
This is for RIAPS developers - **NOT for APP developers**.

The scripts are as follows:
- riaps.mn: launches a simple mininet configuration, uses sshd.py. RIAPS environment variables must be set.  

- riaps-mn.ctrl: script to be run on the 'lead' node of mininet, launches the registry and the controller

- riaps-mn-dns.ctrl: similar to the riaps-mn.ctrl, but it also launches a small dns server so that symbolic names can be used to access the mininet nodes. NOT RECOMMENDED.

- riaps-mn.node : script to be run on the 'slave' nodes of mininet, launches the deplo manager

- pytinydns.py, pytinydns.host, pytinydns.conf: the script for the small dns server (used by riaps-mn-dns.ctrl), and its configuration files.

- sshd.py: starts mininet with a 4 node network, each node running sshd. Used for mininet-based testing.
