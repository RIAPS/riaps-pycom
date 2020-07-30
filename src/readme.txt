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

textX >= 1.7.1
redis >= 2.10.5
hiredis >= 0.2.0
pyzmq >= 16
pycapnp >= 0.5.12
netifaces >= 0.10.7
paramiko >= 2.6.0
cryptography >= 2.7
python-magic >= 0.4.13
cgroups >= 0.1.0
cgroupspy >= 0.1.6
psutil >= 5.4.2
pydot >= 1.2.4
butter >= 0.12.6
lmdb >= 0.94
fabric3 >= 1.14.post1
pyroute2 >= 0.5.2
czmq >= 0.1 (git tag v4.1.1)
zyre >= 0.1 (git commit#7b27a42ed490e20b39a8be0bc7b84151483d7d9d)
graphviz >= 0.5.2
gitpython >= 3.0.4 (due to gitdb and gitdb2 changes)
pymultigen >= 0.2.0
Jinja2 >= 2.10
pybind11 >= 2.2.4
toml >= 0.10.0
pycryptodomex >= 3.7.3 (python3-crypto and python3-keyrings.alt must be removed)
PyYAML >= 5.1.1 (must use --ignore-installed since this is upgrading a distribution package which can not be uninstalled)

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
