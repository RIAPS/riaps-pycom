'''
Constants for the run-time system
Created on Oct 20, 2016

@author: riaps
'''
import riaps.consts.const as const

# Name of endpoint for actor-disco communication
const.discoEndpoint = 'tcp://127.0.0.1:9700'    # 'ipc:///tmp/riaps-disco'
# Timeout for actor-disco communication (-1: wait forever)
const.discoEndpointRecvTimeout = -1
const.discoEndpointSendTimeout = -1

# Name of endpoint for actor-depl communication
const.deplEndpoint = 'tcp://127.0.0.1:9780'     # 'ipc:///tmp/riaps-depl'
# Timeout for actor-depl communication (-1: wait forever)
const.deplEndpointRecvTimeout = 10000 
const.deplEndpointSendTimeout = 10000  

# Name of endpoint for actor-devm communication
# const.devmEndpoint = 'tcp://127.0.0.1:9790'     # 'ipc:///tmp/riaps-devm
# # Timeout for actor-depl communication (-1: wait forever)
# const.devmEndpointRecvTimeout = 10000  
# const.devmEndpointSendTimeout = 10000
  
# Timeout for deplo internal communications
const.depmRecvTimeout = 3000
const.depmSendTimeout = 3000

# Fault monitor endpoints
const.fmNICMonitorEndpoint = 'inproc://fm-nic'
const.fmMonitorEndpoint = 'inproc://fm-riaps'

# Default host for disco redis host
const.discoRedisHost = 'localhost'
# Default port number for disco redis host
const.discoRedisPort = 6379

# Default host for the Controller
const.ctrlNode = 'localhost'
# Default port number for the Controller
const.ctrlPort = 8888

# Control service name
const.ctrlServiceName = 'RIAPSControl'
# Name of private key file
const.ctrlPrivateKey = 'id_rsa.key'
# SSH port
const.ctrlSSHPort = 22
# Control/deplo delay (in msec) - time allowed for recovered apps to start
const.ctrlDeploDelay = 1000

# Log service name
const.logServiceName = 'RIAPSLog'
# Log service configuration
const.logServiceConfig = {"allow_public_attrs": True, "allow_pickle": True}

# Nethog
const.nethogLibrary = 'libnethogs.so'

# Quota system scanning timeout
const.spcMonitorTimeout = 10.0

# App database
const.appDb = 'riaps-apps.lmdb'     # Under RIAPSAPPS
const.appDbSize = 16                # Mbytes 

