RIAPS development using Mininet
-------------------------------

Mininet is tool that can create a virtual network in a Linux environmen. This README is for 
platform and application developers who want to run RIAPS in a mininet environment. The 
environment is useful for developing and testing distributed applications, as one can work
with multiple virtual RIAPS nodes, each acting as if it were a separate system.
Note that Mininet virtualizes the network interface -- the file system is still shared among
the virtual network nodes. 

Caveat: 
We assume that the reader is familiar with mininet, what it does, and how to use it.
The Mininet has to be installed on the Linux machine and it has to have the Python3 API 
support installed. 

To start the environment:
(1) If you are working on the RIAPS platform itself, in the root folder of this workspace execute
 		source setup
 		cd mn
 		./riaps-mn
 	These commands will set up some environment variables and launch the mininet system.
(2) If you are a RIAPS app developer and RIAPS is already installed on your development VM, do   
 	cd mn
	./riaps-mn
 	These commands launch the mininet system that will use the existing RIAPS installation. 

The last command requires root privileges. The same command takes an optional integer argument 
(default=4) that determines the number of virtual hosts created on the mininet network. The virtual 
network will have hosts named h1, ..., hN (where N is the number of hosts, default = 4). 
The hosts h1..hN will have IP addresses 192.168.57.1 ... 192.168.57.N and each host runs an sshd. 
The last command results in staring the mininet command line interpreter, where the usual 
mininet commands can be executed. 

The command to start the riaps_ctrl on node h1
	h1 xterm -T "Control"  -e ./riaps-mn.ctrl &
This script will also start the rpyc_registry on node h1

The command to start the riaps_deplo on node h2
	h2 xterm -T h2 -e ./riaps-mn.node &
The started riaps_deplo will login to the riaps_ctrl and respond to commands.  

The above commands launch an xterm window where you can see the stdout/stderr messages.
After launching the riaps_ctrl it can be used to select an application for downloading 
and running it on the virtual hosts on which the riaps_deplo is running. 

To shutdown the experiment, stop the application with riaps_ctrl, kill the riaps_deplo(s),
and quit riaps_ctrl. Finally, exit the Mininet CLI. This should remove the virtual network.
If something goes wrong, the development machine should be rebooted. 


