Required packages that should be installed manually
===================================================

redis
url = http://redis.io/
version = http://download.redis.io/releases/redis-4.3.4.tar.gz


capnproto:
url = https://capnproto.org/
version = https://capnproto.org/capnproto-c++-0.8.0.tar.gz

rpyc:
url = https://github.com/tomerfiliba/rpyc
version = rpyc-master (i.e. the version on github, not the release!)

PYGObject:
url = https://wiki.gnome.org/action/show/Projects/PyGObject
version = focal (20.04LTS)

#Other Packages Required

textX >= 3.0.0
redis >= 4.3.4
hiredis >= 2.0.0
pyzmq >= 23.2.1
pycapnp >= 1.0.0
netifaces >= 0.11.0
paramiko >= 2.11.0
cryptography >= 3.3.2
python-magic >= 0.4.27
cgroups >= 0.1.0
cgroupspy >= 0.2.2
psutil >= 5.9.2
pydot >= 1.4.2
butter >= 0.13.1
lmdb >= 1.3.0
fabric3 >= 1.14.post1
pyroute2 >= 0.7.2
czmq >= 4.2.1
zyre >= 2.0.1
graphviz >= 0.20.1
gitpython >= 3.1.27 (due to gitdb and gitdb2 changes)
pymultigen >= 0.2.0
Jinja2 >= 3.1.2
pybind11 >= 2.10.0
toml >= 0.10.2
pycryptodomex >= 3.15.0 (python3-crypto and python3-keyrings.alt must be removed)
PyYAML >= 6.0 (must use --ignore-installed since this is upgrading a distribution package which can not be uninstalled)
libtmux>=0.15.7
parse>=1.19.0
bcrypt>=3.2.2

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
