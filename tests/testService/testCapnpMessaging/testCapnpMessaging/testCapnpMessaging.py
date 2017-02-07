import zmq
import capnp
import disco_capnp
from riaps.consts.defs import *
import logging
from riaps.utils.ifaces import getNetworkInterfaces
import sys
import os

# Set up the logger
logpath = '/tmp/testCapnpMessaging_' + sys.argv[1]
try:
    os.remove(logpath)
except OSError:
    pass

testlogger = logging.getLogger(__name__)
testlogger.setLevel(logging.DEBUG)
fh = logging.FileHandler(logpath)
fh.setLevel(logging.DEBUG)
testlogger.addHandler(fh)

(globalIPs,globalMACs,localIP) = getNetworkInterfaces()
assert len(globalIPs) > 0 and len(globalMACs) > 0
globalMAC = globalMACs[0]
macAddress = globalMAC

context = zmq.Context()
socket = context.socket(zmq.REQ)
endpoint = 'ipc:///tmp/riaps-disco' + macAddress
socket.connect(endpoint)

testlogger.info("registerApp")
reqt = disco_capnp.DiscoReq.new_message()
appMessage = reqt.init('actorReg')
appMessage.appName = "Service testApp"
appMessage.version = '0.0.0'
appMessage.actorName = "Service test"

msgBytes = reqt.to_bytes()
try:
    socket.send(msgBytes)
except Exception as e:
    testlogger.error("Unable to register app with discovery: %s" % e.args)
    socket.close()
    socket = None
    exit(-1)

try:
    respBytes = socket.recv()
except Exception as e:
    testlogger.error("No response from discovery service: %s" % e.args)
    socket.close()
    socket = None
    exit(-1)

resp = disco_capnp.DiscoRep.from_bytes(respBytes)

which = resp.which()
if which == 'actorReg':
    respMessage = resp.actorReg
    status = respMessage.status
    port = respMessage.port

    testlogger.info("Disco response: " + str(respMessage.status))

    if status != 'ok':
        testlogger.error("Error response from disco service at app registration")
else:
    testlogger.error("Unexpected response from disco service at app registration")


