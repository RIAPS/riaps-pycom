Running RIAPS Applications      
==========================

There are three ways to launch and run a riaps application, described below. The file
launch/readme.txt describes the various launch configurations that can be used from 
within Eclipse. 

1. Running a riaps app solely in the development environment
------------------------------------------------------------
 
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

Debugging an application
------------------------

To debug the application, we have to use the 'Pydev Remote Debugger', described on this page: 
http://www.pydev.org/manual_adv_remote_debugger.html
Note that the application runs as a separate process - as a riaps actor - launched by the 
riaps deployment manager, hence the need for the 'remote debugger'. While this process may seem 
complex, it can also be used to debug applications running on any node(s) of a network.   

The debugger works as follows
(1) The program to be debugged must include the statement
      import pydevd			# This is at the beginning of the file
      
      ....
      	pydevd.settrace()	# This must be placed somewhere in the component code.
      ....
     A typical good place for the settrace() statement is the component constructor.  
     
(2) In the Eclipse environment a 'Debug server' must be started (see the url above). 
(3) The application should be started as described above (registry,ctrl,deplo)
(4) When the component code is running and it reaches the settrace() statement, it stops and 
    links up with the debug server running in Eclipse. From this point one can control the 
    execution of the component code: can set breakpoints, single step, etc. - just like 
    in a normal debugging session. 
 
2. Running a riaps app in the development environment on a virtual network
--------------------------------------------------------------------------

While the above method to run an application works well it has a few serious shortcoming: it 
can run only single copies of actors and all the actors share the same network interface of 
the host machine. In other words there is no way to run an application on a 'network' on 
separate nodes. However, Linux has a tool called 'mininet' that emulates a 'virtual network'
in a running operating system. The tool sets up a network of virtual hosts (processes), each
having its own (virtual) network interface - and these hosts can communicate via those 
interfaces. This means is that application processes (actors) executing on the (virtual) nodes
of the emulated network run concurrently and communicate as if they were running on a network
of physical nodes connected by a physical network. 

Mininet can configure the virtual network with an arbitrary topology and routing (see 
http://mininet.org/ for details). Additionally, mininet  requires administrator privileges,
so when it is started the administrator (superuser) password needs to be provided. 

We assume below that all RIAPS environment variables are set. 
To start a mininet-based test, the following steps need to be taken:
(1) Change to the folder where RIAPS is located and execute the shell command:
      riaps-dev.mn
      
    These will launch a mininet command line tool with a virtual network of 4 nodes.
    The nodes have the IP addresses 10.0.0.1 - 10.0.0.4, connected via (virtual) network switch.
    The host machine is also on this network - it has the IP address 10.123.123.1
     
    Each node will run an 'ssh' service that is needed for transferring the application files 
    from the 'controller' node to the 'application' nodes. For this transfer to succeed the
    keys have to be properly configured. For this, the ssh public key needs to be installed 
    in ~/.ssh (as the app files are transferred using sftp from the virtual CTRL node to the 
    virtual SLAVE nodes.
    To add the public key:
      cat src/ssh/id_rsa.pub >>~/.ssh/authorized_keys
    Make sure that authorized_keys has permissions set 644, and the ~/.ssh folder has 755. 
(2) Launch an xterm terminal on each of the four hosts using the command at the at the mininet command prompt:
      xterm h1 h2 h3 h4
(3) The xterm windows are running a privileged mode shell and you can start the various processes as follows:
    On h1 (on 10.0.0.1) start 
      riaps-dev.ctrl 
    This starts the controller.
    On h2 (h3,h4) (i.e. 10.0.0.2-3-4) start
       riaps-dev.node
    At this point we have one (virtual) node running the controller, and 3 (virtual)
    nodes running the deplo service. 
    Note that the above commands start a terminal window where one can see the log messages
    generated by the various processes.
(3) Use the controller gui to start the application, as described above. 
(4) To stop the application use the 'Stop' button on the GUI, then CTRL-C/CTRL-D on each virtual
    node - this will terminate first the deplo then the terminal. Finally, exit mininet 
    using CTRL-D - this will dismantle the virtual network. 
 
The above method is useful for running an application but for debugging the Eclipse remote debugger
should be used. The process is the same as above (start the dbeug server on Eclipse), but the 
call to the settrace() function in the application code must now include the IP address of the
host the debug server is running on, as show below:   
 	pydevd.settrace(host='10.123.123.1',port=5678)
Note that while the riaps controller and deplo tools are started manually (within mininet), the 
application component code - when executed - will connect to the Eclipse debug server via a (virtual)
network connection. 

3. Running a riaps app on a network of bbb nodes connected to a physical network 
--------------------------------------------------------------------------------


 
      
