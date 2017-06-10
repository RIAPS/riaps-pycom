[![Build Status](https://travis-ci.com/RIAPS/riaps-pycom.svg?token=pyUEeBLkG7FqiYPhyfxp&branch=master)](https://travis-ci.com/RIAPS/riaps-pycom)

# pycom


## Running RIAPS Applications

There are three ways to launch and run a riaps application, described below. The file
launch/readme.txt describes the various launch configurations that can be used from 
within Eclipse. 

### Running a riaps app solely in the development environment
 
This method runs the entire app on the development machine and all actors use a single network
interface to communicate with each other. This means that all actor run on the same 'node'.

Suppose we created a project called 'pro', with model file 'pro.riaps' and deployment file 
'pro.depl'. The latter should be such that actor(s) run on 'all' nodes (i.e. the only node we 
have). The model may declare multiple actors (say a1,a2,a3) and components, but the deployment 
plan should place them on 'all' node, as follows:
	on all a1,a2,a3

To run this application execute the following operations in Eclipse
- launch 'rpyc_registry'
- launch 'riaps ctrl'
- launch 'riaps deplo' 

Then use the 'RIAPS Control' app gui to 
(1) Select the application folder (.../pro)
(2) Select the model file (pro.riaps)
(3) Select the deployment file (pro.depl)
(4) Click the 'Launch' button on to start the actor(s) of the app.

This last step will transfer the application's files to the riaps deplo manager that in turn 
will start the actor(s) of the application. 

Once the application is running, it can be stopped using 'Stop' button on the 
gui. This will instruct
the deplo manager to terminate all actors. Then the riaps controller can be terminated (by 
closing  its window) and all the other process launched (using the Eclipse 'teminate all' button).  

#### Debugging an application


To debug the application, we have to use the 'Pydev Remote Debugger', described on this page: 
http://www.pydev.org/manual_adv_remote_debugger.html
Note that the application runs as a separate process - as a riaps actor - launched by the 
riaps deployment manager, hence the need for the 'remote debugger'. While this process may seem 
complex, it can also be used to debug applications running on any node(s) of a network.   

The debugger works as follows
(1) The program to be debugged must include the statement
```
      import pydevd			# This is at the beginning of the file
      
      ....
      	pydevd.settrace()	# This must be placed somewhere in the component code.
      ....
```      
A typical good place for the `settrace()` statement is the component constructor.  
     
(2) In the Eclipse environment a 'Debug server' must be started (see the url above). 
(3) The application should be started as described above (registry,ctrl,deplo)
(4) When the component code is running and it reaches the settrace() statement, it stops and 
    links up with the debug server running in Eclipse. From this point one can control the 
    execution of the component code: can set breakpoints, single step, etc. - just like 
    in a normal debugging session. 
 
### Running a riaps app in the development environment on a virtual network


While the above method to run an application works well it has a few serious shortcoming: it 
can run only single copies of actors and all the actors share the same network interface of 
the host machine. In other words there is no way to run an application on a 'network' on 
separate nodes. However, Linux has a tool called 'mininet' that emulates a 'virtual network'
in a running operating system. The tool sets up a network of virtual hosts (processes), each
having its own (virtual) network interface - and these hosts can communicate via those 
interfaces. This means is that application processes (actors) executing on the (virtual) nodes
of the emulated network run concurrently and communicate as if they were running on a network
of physical nodes connected by a physical network. 

#### RIAPS - Mininet

This is for riaps developers - NOT for APP developers. 

To run the riaps tools on mininet
1. The ssh public key needs to be installed in `~/.ssh` as the app files are 
transferred using sftp from the virtual CTRL node to the virtual SLAVE nodes.
To add the public key:
    `cat src/ssh/id_rsa.pub >>~/.ssh/authorized_keys`
Make sure that authorized_keys has permissions set 644, and the `~/.ssh` folder has 755.

2. Use the shell commands: 
```
 source setup		# Sets up environment variables
 bin/riaps.mn		# Starts up mininet with topo=single,4 and sshd on each node
```

3. At the mininet prompt:

Start up the RIAPS Controller on the lead node (h1) (registry,dbase,ctrl):
```
h1 xterm -e bin/riaps-mn.ctrl &
``` 

Start up the RIAPS Deployment Manager on host hX (X = 2,3,4)
```
hX xterm -e bin/riaps-mn.node &
``` 


#### mininet with DNS

If the deployment model has DNS names for the mininet nodes (instead of the default IP addresses:
10.0.0.[1-4]) a local DNS server can be used on the virtual network. Launching the controller start script
```
  bin/riaps-mn-dns.ctrl
``` 
on the first node (h1) will reconfigure the DNS resolver by switching to a custom /etc/resolv.conf file. 
This script also starts a small DNS server configured for the following DNS names and IP addresses: 
ctrl.:10.0.0.1
bbb1.:10.0.0.2
bbb2.:10.0.0.3
bbb3.:10.0.0.4
If this script is used, the deployment models can use the names: ctrl. , bbb1. , bbb2. , bb3. instead of the 
IP addresses. 
 
If the controller program crashes then the original DNS resolver configuration must be restored as follows:
```
 sudo mv /etc/resolv.conf.org /etc/resolv.conf
```

If the controller terminates correctly, the script will automatically restores this.
  

 
The above method is useful for running an application but for debugging the Eclipse remote debugger
should be used. The process is the same as above (start the dbeug server on Eclipse), but the 
call to the settrace() function in the application code must now include the IP address of the
host the debug server is running on, as show below:   
 	pydevd.settrace(host='10.123.123.1',port=5678)
Note that while the riaps controller and deplo tools are started manually (within mininet), the 
application component code - when executed - will connect to the Eclipse debug server via a (virtual)
network connection. 

### Running a riaps app on a network of bbb nodes connected to a physical network 

To be written...
      
## Required packages that should be installed manually

```
redis
url = http://redis.io/
version = http://download.redis.io/releases/redis-3.2.5.tar.gz


capnproto: 
url = https://capnproto.org/
version = https://capnproto.org/capnproto-c++-0.5.3.tar.gz

rpyc:
url = https://github.com/tomerfiliba/rpyc
version = rpyc-master (i.e. the version on github, not the release!)

PYGObject:
url = https://wiki.gnome.org/action/show/Projects/PyGObject
version = xenial (16.04LTS)
```

Other required packages:
````
textX >= 1.4
redis >= 2.10.5
hiredis >= 0.2.0
pyzmq >= 16
pycapnp >= 0.5.9
netifaces >= 0.10.5
paramiko >= 2.0.2
cryptography >= 1.5.3
```

To install: 
```
apt install python3-pip python3-dev libhiredis-dev libcapnp-dev libssl-dev libffi-dev glade python3-gi
```

Alternative: use the vagrant riaps devbox
