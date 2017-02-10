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


# Get global interface
(globalIPs,globalMACs,localIP) = getNetworkInterfaces()
assert len(globalIPs) > 0 and len(globalMACs) > 0
globalMAC = globalMACs[0]
macAddress = globalMAC
globalIP = globalIPs[0]

context = zmq.Context()
socket = context.socket(zmq.REQ)
endpoint = 'ipc:///tmp/riaps-disco' + macAddress
socket.connect(endpoint)

# Register actor
appName = "ServiceTestApp"
actorName = "ServiceTestActor"

reqt = disco_capnp.DiscoReq.new_message()
appMessage = reqt.init('actorReg')
appMessage.appName = appName
appMessage.version = '0.0.0'
appMessage.actorName = actorName

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
        socket.close()
        socket = None
        exit(-1)
else:
    testlogger.error("Unexpected response from disco service at app registration")
    socket.close()
    socket = None
    exit(-1)


# register a service
msgType = 'testMessageType'
req = disco_capnp.DiscoReq.new_message()
reqMsg = req.init('serviceReg')
reqMsgPath = reqMsg.path
reqMsg.socket.host = globalIP
reqMsg.socket.port = 1111
reqMsgPath.appName = appName
reqMsgPath.msgType = msgType
reqMsgPath.kind = 'pub'
reqMsgPath.scope = 'global'
msgBytes = req.to_bytes()
socket.send(msgBytes)

try:
    repBytes = socket.recv()
except Exception as e:
    testlogger.error("No response from discovery service: %s" % e.args)
    socket.close()
    socket=None
    sys.exit(-1)
rep = disco_capnp.DiscoRep.from_bytes(repBytes)
which = rep.which()
returnValue = []
if which == 'serviceReg':
    repMessage = rep.serviceReg
    status = repMessage.status
    testlogger.info("Disco serviceReg response: " + str(respMessage.status))
    if status != 'ok':
        testlogger.error("Error response from disco service at service registration")
        socket.close()
        socket = None
        exit(-1)
else:
    testlogger.error("Unexpected response from disco service at service registration")
    socket.close()
    socket = None
    exit(-1)

# query service, expecting the results later (async behavior)
'''
req = disco_capnp.DiscoReq.new_message()
reqMsg = req.init('serviceLookup')
reqMsgPath = reqMsg.path
reqMsgPath.appName = appName
reqMsgPath.msgType = msgType
reqMsgPath.kind = 'sub'
reqMsgPath.scope = 'global'
reqMsgClient = reqMsg.client
reqMsgClient.actorHost = globalIP
reqMsgClient.actorName = actorName
reqMsgClient.instanceName = 'dummypart'
reqMsgClient.portName = 'dummyport'

msgBytes = req.to_bytes()
socket.send(msgBytes)
try:
    repBytes = socket.recv()
except Exception as e:
    raise SetupError("No response from disco service : {1}".format(e.errno, e.strerror))
    raise
rep = disco_capnp.DiscoRep.from_bytes(repBytes)
which = rep.which()
returnValue = []
if which == 'serviceLookup':
    repMessage = rep.serviceLookup
    status = repMessage.status
    if status == 'err':
        raise SetupError('Unable to lookup service')
    sockets = repMessage.sockets
    for sock in sockets:
        host = sock.host
        port = sock.port
        returnValue.append((partName, portName, host, port))
    else:
        pass
else:
    raise SetupError("Service lookup error - bad response")
'''

socket.close()
socket = None
