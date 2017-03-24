Required packages that should be installed manually

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


use: apt install python3-pip python3-dev libhiredis-dev libcapnp-dev libssl-dev libffi-dev glade python3-gi


Alternative: use the vagrant riaps devbox