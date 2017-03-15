Files in this folder are for running various parts of riaps by the riaps developers (not APP developers)

The scripts are as follows:
- riaps.mn: launches a simple mininet configuration, uses sshd.py. RIAPS environment variables must be set.  
- riaps-mn.ctrl: script to be run on the 'lead' node of mininet, launches the registry and the controller
- riaps-mn-dns.ctrl: similar to the riaps-mn.ctrl, but it also launches a small dns server so that
  symbolic names can be used to access the mininet nodes. NOT RECOMMENDED.
- riaps-mn.node : script to be run on the 'slave' nodes of mininet, launches the deplo manager
- pytinydns.py, pytinydns.host, pytinydns.conf: the script for the small dns server (used by riaps-mn-dns.ctrl),
  and its configuration files.
- sshd.py: starts mininet with a 4 node network, each node running sshd. Used for mininet-based testing.
