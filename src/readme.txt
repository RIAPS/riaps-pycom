Required packages that should be installed manually
===================================================

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

#Other Packages Required

textX >= 1.4
redis >= 2.10.5
hiredis >= 0.2.0
pyzmq >= 16
pycapnp >= 0.5.9
netifaces >= 0.10.5
paramiko >= 2.0.2
cryptography >= 1.5.3
python-magic >= 0.4.13
cgroups >= 0.1.0
cgroupspy >= 0.1.6
psutil >= 3.4.2
pydot >= 1.2.4

use: apt install python3-pip python3-dev libhiredis-dev libcapnp-dev libssl-dev libffi-dev glade python3-gi

CGroups
=======

cgroups implements a command 'user_groups' that need to be run at every boot to 
establish a cgroup called as and owned by 'riaps'. This is the only command used from
that package. 

cgroupspy is the library used to configure the specific cgroups for the applications.   

At boot time, the riaps cgroup should be created by root:
# user_cgroups riaps

Each app has a folder under each cgroup category, e.g. cpu:riaps/APP, and each actor of each app 
has a folder under that, e.g. cpu:riaps/APP/ACTOR

When necessary, the riaps cgroup (or any subgroup of it) can be deleted by root (e.g. for the cpu:
# cgdelete -r cpu:riaps/

 

Launch configurations
=====================

Launch configurations for the various RIAPS processes:
  actor, ctrl, depll, deplo, device, devm, disco, lang 
and tests are kept in their respective folders. 
Launch configurations for external programs: redis and
rpyc registry are kept under the bin folder. 

These files are for RIAPS developer for use in the Eclipse environment, 
when RIAPS is not installed in its canonical location. 
There are two types of files: 
(1) run/debug configurations - these are for running Python programs in a configured environment
(2) external tool configurations - these for running arbitrary program
While Python programs can be run by (2), they can be debugged only if they run as (1).

The files are as follows (the number after the name indicates the type):
- riaps ctrl (1): Start the riaps controller app
- riaps dbase start (2) : Start the redis database server
- riaps dbase stop (2) : Stop the redis database server
- riaps depll (1) : Run the deployment language parser (that translates .depl files) 
  on the DistributedEstimator's sample.depl file
- riaps deplo (1) : Run the deployment manager (deplo)
- riaps disco (1) : Run the discovery service (disco)
- riaps lang (1) : Run the riaps modeling language parser (that translates 
  .riaps files) on the DistributedEstimator's sample.riaps file
- riaps run Aggregator (1) : Run the Aggregator actor of the DistributedEstimator test app
- riaps run DAverager (1) : Run the Averager actor of the DistributedAverager test app
- riaps run Estimator (1) : Run the Estimator actor of the DistributedEstimator test app 
- rpyc_registry (2) : Run the registry process (used by the riaps controller and deplo manager)

Type (1) launchers can be started from Eclipse run or debug menus, while type (2) 
launchers must be started as an 'external tool' from Eclipse. 

------------------------

