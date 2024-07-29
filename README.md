# riaps-pycom

## Security Note

**The riaps pycom repository contains a set of default RSA keys. These keys are used for testing the system and create images. In both the development vm images and the beaglebone image these keys are to be replaced upon install.
DO NOT USE THESE KEYS IN ANY PRODUCTION SYSTEM!** 

## Prerequisites

1) Set up a Development Environment using VirtualBox:  https://github.com/RIAPS/riaps-integration/tree/master/riaps-x86runtime

2) Log in as the RIAPS app developer:  

```
	Username:  riaps
	Password:  riaps
```

1) Install RIAPS on target nodes (Beaglebone Black devices):  https://github.com/RIAPS/riaps-integration/tree/master/riaps-node-runtime

## Files Application Developer Writes

Files you need to write when creating your applications are:

- **yourModel.riaps** to define how your system works
- **yourDeployModel.depl** to define the deployment (which actors are on which target nodes and the location of the nodes)
- Component Model code in ComponentX.py files for each component defined in **yourModel.riaps**

## Running RIAPS Applications

There are three ways to launch and run a RIAPS application, described below.
https://github.com/RIAPS/riaps-pycom/tree/master/tests includes examples of various test applications that utilize
different features of the platform.

### Running a RIAPS App Solely in the Development Environment

This method runs the entire app on the development machine and all actors use a single network interface to communicate with each other. This means that all actor run on the same **node**.

Suppose we created a project called **pro**, with model file **pro.riaps** and deployment file **pro.depl**. The latter should be such that actor(s) run on **all** nodes (i.e. the only node we have). The model may declare multiple actors (say a1,a2,a3) and components, but the deployment plan should place them on 'all' node, as follows:

```
on all a1,a2,a3
```

To run this application execute the following operations in Eclipse
- launch 'riaps ctrl'
- launch 'riaps deplo'

> Note: ***rpyc_registry*** will be running as a service in the background.

To run this from a command line in the development environment, run the following commands in different terminal sessions

```
riaps_ctrl
sudo -E riaps_deplo
```

Then use the 'RIAPS Control' app gui to

1) Select the application folder (.../pro)

2) Select the model file (pro.riaps)

3) Select the deployment file (pro.depl)

4) Click the 'Launch' button on to start the actor(s) of the app.

This last step will transfer the application's files to the RIAPS deplo manager that in turn will start the actor(s) of the application.

Once the application is running, it can be stopped using 'Stop' button on the
gui. This will instruct the deplo manager to terminate all actors. Then the RIAPS controller can be terminated (by closing its window) and all the other process launched (using the Eclipse 'teminate all' button or Ctl C in each terminal window).  

### Running a RIAPS App on a Network of Hardware Nodes Connected to a Physical Network

This method runs the control application on a development machine and applications on separate hardware nodes that are attached to the same local network using a router.

As indicated in the previous method, create the project (***pro***), model file (***pro.riaps***) and deployment file (***pro.deplo***).  This deployment file will identify the IP address (xxx.xxx.xxx.xxx) or hostname (riaps-xxxx.local) of the hardware nodes that each actor will run.  If the actor is intended run on **all** nodes, utilize the ***all*** keyword.  The hostname is configured to be the last four digits of the hardware MAC address, be sure to include the .local added to the end.  An example of the possible node identification forms are shown below
```
on 192.168.1.103 a1
on riaps-1234.local a2
on all a3
```

To run this application execute the following operations in Eclipse on the development environment
- launch ***riaps ctrl***

> Note: ***rpyc_registry*** will be running as a service in the background.

To run this from a command line in the development environment, run the following commands in different terminal sessions

```
riaps_ctrl
```

Once each hardware node is registered in the control application, then use the 'RIAPS Control' app gui to

1) Select the application folder (.../pro)

2) Select the model file (pro.riaps)

3) Select the deployment file (pro.depl)

4) Click the **Load** button to transfer the application's files to the RIAPS deplo manager of each node
   
5) Once the application transfer is complete, a button will appear with the application name in the "App" column which contains the controls for running the application (**Launch**, **Stop**, **Remove**)
   
6)  Select **Launch** to start the actor(s) of the application on the nodes

7)  Once the application is running, it can be stopped using **Stop** button on the gui. This will instruct the deplo manager to terminate all actors.  All application files and any log files created by the application are still available on the nodes.

8)  To pull any application log data to the development machines, open a new terminal window and run ```riaps_fab riaps.getAppLogs```.  This command will pull all the log files from each node and place them in a `./logs` folder with a subfolder for each node.
   
9)  When use of the application is complete, the application should be removed using **Remove** option found when hitting the specific application button.

Then the RIAPS controller can be terminated (by closing its window) and all the other process launched (using the Eclipse **teminate all** button or **Ctl C** in each terminal window).  


#### Debugging an Application on Remote Nodes

To debug the application, we have to use the **Pydev Remote Debugger**, described on this page: http://www.pydev.org/manual_adv_remote_debugger.html.

Note that the application runs as a separate process - as a RIAPS actor - launched by the RIAPS deployment manager, hence the need for the **remote debugger**. While this process may seem complex, it can also be used to debug applications running on any node(s) of a network.   

The debugger works as follows

1) The program to be debugged must include the statement, with the IP address of the development machine
```
import pydevd			# This is at the beginning of the file

...
pydevd.settrace(host='xxx.xxx.xxx.xxx',port=5678)	# This must be placed somewhere in the component code.
...
```      

A typical good place for the **settrace()** statement is the component constructor.  

2) In the Eclipse environment a **debug server** must be started (see the url above).

3) The application should be started as described above (ctrl,deplo)

4) When the component code is running and it reaches the settrace() statement, it stops and links up with the debug server running in Eclipse. From this point one can control the execution of the component code: can set breakpoints, single step, etc. - just like in a normal debugging session.

## [RIAPS on a single VM Host](mininet.md)

See [mn/README.md](https://github.com/RIAPS/riaps-pycom/tree/master/mn)

