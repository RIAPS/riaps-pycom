Required packages that should be installed manually
===================================================

redis
url = http://redis.io/
version = http://download.redis.io/releases/redis-5.0.1.tar.gz


capnproto:
url = https://capnproto.org/
version = https://capnproto.org/capnproto-c++-1.0.1.1.tar.gz

rpyc:
url = https://github.com/tomerfiliba/rpyc
version = rpyc-master (i.e. the version on github, not the release!)

PYGObject:
url = https://wiki.gnome.org/action/show/Projects/PyGObject
version = jammy (22.04LTS)

#Other Packages Required

bcrypt>=4.0.1
butter >= 0.13.1
cgroups >= 0.1.0
cgroupspy >= 0.2.2
cryptography >= 3.4.8
czmq >= 4.2.1
fabric >= 3.2.2
filelock==3.15.4
gitpython >= 3.1.37 (due to gitdb and gitdb2 changes)
graphviz >= 0.20.1
hiredis >= 2.3.2
Jinja2 >= 3.1.2
libtmux>=0.23.2
lmdb >= 1.4.1
netifaces2 >= 0.0.9
paramiko >= 3.4.0
parse>=1.19.1
psutil >= 5.9.0
pybind11 >= 2.11.1
pycapnp >= 2.0.0b2
pycryptodomex >= 3.19.0 (python3-crypto and python3-keyrings.alt must be removed)
pydot >= 1.4.2
pymultigen >= 0.2.0
pyroute2 >= 0.7.2
python-magic >= 0.4.27
PyYAML >= 5.4.1
pyzmq >= 25.1.2
redis >= 5.0.1
spdlog==2.0.6
textX >= 3.1.1
toml >= 0.10.2
zyre >= 2.0.1

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
