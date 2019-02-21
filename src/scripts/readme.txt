Files in this folder are for running various parts of riaps by the riaps APP developers.
These scripts are usually installed in a folder that is accessible via the PATH on the app developer's machine
(e.g. /usr/local/bin). The scripts assume that the environment variables RIAPSHOME and RIAPSAPPS are set up.

These scripts are used only when mininet is used:
- riaps-dev.mn : launches the simple mininet configuration, uses sshd.py (which should be in the path)
- riaps-dev.ctrl: script to be run on the 'lead' node of mininet, launches the registry and the controller
- riaps-dev.node: script to be run on the 'slave' nodes of mininet, launches the deplo manager
- sshd.py: starts mininet with a 4 node network, each node running sshd.

The scripts listed below are used by all riaps installations (both on a development machine and the
embedded targets):
- riaps_actor:     the actor
- riaps_ctrl:      the controller
- riaps_ctrl_host: retrieves IP address(es) of RIAPS control host
- riaps_depll:     the deployment language processor
- riaps_deplo:     the deployment manager
- riaps_device:    the device
- riaps_disco:     the discovery service
- riaps_gviz:      a graphical visualizer for an application model
- riaps_lang:      the modeling language processor
- rpyc_registry:   background communication between the controller and the deployment manager

The following scripts are available for developers to utilize:
- riaps_gen:       component code generation tool
- riaps_gen_cert:  generate public/private key pair and self-signed certificate
