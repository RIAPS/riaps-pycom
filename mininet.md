
### Running a RIAPS App in the Development Environment on a Virtual Network

While the above method to run an application works well it has a few serious shortcoming: it can run only single copies of actors and all the actors share the same network interface of the host machine. In other words, there is no way to run an application on a **network** on separate nodes. However, Linux has a tool called **mininet** that emulates a **virtual network** in a running operating system. The tool sets up a network of virtual hosts (processes), each having its own (virtual) network interface - and these hosts can communicate via those interfaces. This means is that application processes (actors) executing on the (virtual) nodes of the emulated network run concurrently and communicate as if they were running on a network of physical nodes connected by a physical network.

#### RIAPS - Mininet

This is for RIAPS developers - **NOT for APP developers**.

Mininet can configure the virtual network with an arbitrary topology and routing (see
http://mininet.org/ for details). Additionally, mininet requires administrator privileges, so when it is started the administrator (superuser) password needs to be provided.

1) Install mininet using the native installation from source instructions (section 3.1) to run the RIAPS tools on mininet:  https://github.com/mininet/mininet/blob/master/INSTALL

2) The ssh public key needs to be installed in **~/.ssh** as the app files are
transferred using sftp from the virtual CTRL node to the virtual SLAVE nodes.
To add the public key:

```
cat src/ssh/id_rsa.pub >>~/.ssh/authorized_keys
```

Make sure that authorized_keys has permissions set 644, and the **~/.ssh** folder has 755.

3) Use the shell commands:
```
source setup		# Sets up environment variables
bin/riaps.mn		# Starts up mininet with topo=single,4 and sshd on each node
```

4) At the mininet prompt:

Start up the RIAPS Controller on the lead node (h1) (registry,dbase,ctrl):
```
h1 xterm -e bin/riaps-mn.ctrl &
```

Start up the RIAPS Deployment Manager on host hX (X = 2,3,4)
```
hX xterm -e bin/riaps-mn.node &
```

5) If necessary, update const.ctrlNode in riaps-pycom/src/riaps/consts/defs.py to match the address of the mininet node that will run riaps_ctrl
- from a mininet xterm:  set const.ctrlNode equal to the value of inet addr, e.g. 10.0.0.1

```
ifconfig
```  

4) If necessary, update self.server in riaps-pycom/src/riaps/ctrl/ctrlsrv.py to match the Bcast address of the mininet node that will run riaps_ctrl

- set ip in UDP.RegistryClient(ip= "Bcast address") e.g.
- self.server = ThreadedServer(ControllerService,port=self.port,registrar=rpyc.utils.registry.UDPRegistryClient(ip="10.255.255.255"),auto_register=True)

5) Then follow the steps for running the application described in the 'Running a RIAPS app on a network of hardware nodes connected to a physical network' section

#### Mininet with DNS

If the deployment model has DNS names for the mininet nodes (instead of the default IP addresses: 10.0.0.[1-4]) a local DNS server can be used on the virtual network.

Launching the controller start script
```
bin/riaps-mn-dns.ctrl
```
on the first node (h1) will reconfigure the DNS resolver by switching to a custom /etc/resolv.conf file.

This script also starts a small DNS server configured for the following DNS names and IP addresses:
- ctrl.:10.0.0.1
- bbb1.:10.0.0.2
- bbb2.:10.0.0.3
- bbb3.:10.0.0.4

If this script is used, the deployment models can use the names: ctrl., bbb1., bbb2., bb3. instead of the
IP addresses.

If the controller program crashes then the original DNS resolver configuration must be restored as follows:
```
sudo mv /etc/resolv.conf.org /etc/resolv.conf
```

If the controller terminates correctly, the script will automatically restores this.

#### Debugging with Mininet

The mininet configuration setup by the **bin/riaps.mn** script sets up interfaces on both the outer host VM as well on the internal emulated network that can be used for debugging Python code. The pydevd debugger can be used as follows:

1) On the host VM start Eclipse,  select the Debug view, start the PydevD Debug server (optionally set the port).

2) Start up the emulated virtual network as shown above. This will create a new virtual network interface on the host; usually called root-eth0, usually with the IP address 10.123.123.1. We can verify that this interface is functional by checking ```ifconfig``` on the host VM, and pinging the IP address from an emulated host (e.g. h1) on the virtual network.

3) Start a Python program on a mininet host - the program should contain the following lines
```
import pydevd
pydevd.settrace('10.123.123.1',port=5678)  # Connect to the debug server on host
```

When the **settrace** line is reached, the program will attempt to connect to the debug server on the host. It will proceed only after the debugger allows it to do so.

Note that while the RIAPS controller and deplo tools are started manually (within mininet), the application component code - when executed - will connect to the Eclipse debug server via a (virtual) network connection.

#### Mininet Network

If the VM's host is running a socket-enabled sim, the guest VM is able to communicate with that via a host-only network interface. This can be extended to virtual hosts inside a mininet network as show below.

The **outer** network is 192.168.56.0/24, the **inner** (mininet) network is 192.168.57.0/24.
The commands below show how to configure the network interfaces.   

1) VM Host - VBox host-only network:
```
IP=192.168.56.254; 255.255.254.0;
DHCP=192.168.56.200; 255.255.255.0;201-250
```
```
# Setup route to inner network (-p: persistence)
> route -p add 192.168.57.0 mask 255.255.255.0 192.168.56.201
```

2) Guest VM: enable forwarding
```
sysctl -w net.ipv4.ip_forward=1
```

3) Mininet
- ipBase = 192.168.57.0/24
- root switch ip = 192.168.57.126/32
- routes = 192.168.57.0/24

4) hX
```
ip route add 192.168.56.0/24 via 192.168.57.126
```

Result:
- VM host can ping 192.168.56.X (as in hX)
