'''
Constants for the run-time system
Created on Oct 20, 2016

@author: riaps
'''
import riaps.consts.const as const

# Name of endpoint for actor-disco communication
const.discoEndpoint = 'ipc:///tmp/riaps-disco'
# Timeout for actor-disco communication (-1: wait forever)
const.discoEndpointTimeout = -1

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
