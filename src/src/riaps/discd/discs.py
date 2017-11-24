'''
Discovery Service main class
Created on Oct 19, 2016

@author: riaps
'''
import zmq
import capnp
import time
import sys
import re
import os

from .dbase import DiscoDbase
from riaps.proto import disco_capnp
from riaps.consts.defs import *
from riaps.utils.ifaces import getNetworkInterfaces
from riaps.run.exc import DatabaseError
import logging

class DiscoService(object):
    '''
    Discovery service main class. 
    '''
    
    def __init__(self,dbase):
        self.logger = logging.getLogger(__name__)
        self.context = zmq.Context()
        self.setupIfaces()
        self.suffix = self.macAddress
        self.dbase = DiscoDbase(self.context,dbase)
        self.registrations = {}
    
    def setupIfaces(self):
        '''
        Find the IP addresses of the (host-)local and network(-global) interfaces
        '''
        (globalIPs,globalMACs,localIP) = getNetworkInterfaces()
        try:
            assert len(globalIPs) > 0 and len(globalMACs) > 0
        except:
            self.logger.error("Error: no active network interface")
            raise
        globalIP = globalIPs[0]
        globalMAC = globalMACs[0]
        self.hostAddress = globalIP
        self.macAddress = globalMAC
        
    def start(self):
        self.logger.info("starting")
        self.server = self.context.socket(zmq.REP)              # Create main server socket for client requests
        endpoint = const.discoEndpoint + self.suffix
        self.server.bind(endpoint)
        
        self.dbase.start()                                      # Start database
        time.sleep(0.0001)                                      # Yield to database so that it can start
        
        self.poller = zmq.Poller()                              # Set up initial poller (only on the main server socket)  
        self.poller.register(self.server,zmq.POLLIN)
        self.portMap = { }
        self.clients = { }  
        self.clientUpdates = []
    
    def run(self):
        '''
        Main loop of the discovery service
        '''
        self.logger.info("running")
        while 1:
            self.clientUpdates = []
            sockets = dict(self.poller.poll(1000.0))            # Poll client messages, with timeout 1 sec
            if len(sockets) == 0:                               # If no message but timeout expired, 
                try: 
                    self.clientUpdates = self.dbase.fetchUpdates()  # then fetch updates from database
                except DatabaseError:
                    self.logger.info("reconnecting database")
                    self.dbase.start()
                    time.sleep(0.0001)     
            elif self.server in sockets:                        # else check if there is a server request, handle it 
                msg = self.server.recv()
                self.handle(msg)
                del sockets[self.server]
            else:
                pass
            for note in self.clientUpdates:                     # Handle all client updates (received from the 
                self.handleNote(note)                           # database and generated by the server requests

    def appActorName(self,appName,appActorName):
        return "%s/%s" % (repr(appName),repr(appActorName)) 
    
    def setupClient(self,appName,appVersion,appActorName):
        '''
        Set up a new client of the discovery service. The client actors are to register with
        the service using the 'server' (REQ/REP) socket. The service will then create a dedicated
        (PAIR) socket for the client to connect to. This socket is used as a private communication
        channel between a specific client actor and the service.   
        '''
        sock = self.context.socket(zmq.PAIR)
        port = sock.bind_to_random_port('tcp://127.0.0.1')
        clientKeyBase = "/" + appName + '/' + appActorName + "/"
        self.clients[clientKeyBase] = sock
        clientKeyLocal = clientKeyBase + self.macAddress
        self.clients[clientKeyLocal] = port
        clientKeyGlobal = clientKeyBase + self.hostAddress
        self.clients[clientKeyGlobal] = port
        self.registrations[self.appActorName(appName,appActorName)] = []
        return port
    
    def unsetupClient(self,appName,appVersion,appActorName):
        '''
        Remove a client   
        '''
        clientKeyBase = "/" + appName + '/' + appActorName + "/"
        sock = self.clients[clientKeyBase]
        clientKeyLocal = clientKeyBase + self.macAddress
        port = self.clients[clientKeyLocal]
        clientKeyGlobal = clientKeyBase + self.hostAddress
        # port = self.clients[clientKeyGlobal] # Must have the same value
        sock.unbind('tcp://127.0.0.1:' + str(port))
        # TODO: remove all services registered by this client  
        del self.clients[clientKeyBase]
        del self.clients[clientKeyLocal]
        del self.clients[clientKeyGlobal]
        registration = self.registrations[self.appActorName(appName,appActorName)]
        for (key,value) in registration:
            self.dbase.remove(key, value)
        return port
    
    def handleActorReg(self,msg):
        '''
        Handle the registration of an application actor with the service. 
        '''
        actReg = msg.actorReg
        appName = actReg.appName
        appVersion = actReg.version   
        appActorName = actReg.actorName
         
        self.logger.info("handleActorReg: %s %s" % (appName, appActorName))
        
        clientPort = self.setupClient(appName,appVersion,appActorName)
        
        # OptionL store in db host.app.vers.actr -> port? 
        
        rsp = disco_capnp.DiscoRep.new_message()
        rspMessage = rsp.init('actorReg')
        rspMessage.status = "ok"
        rspMessage.port = clientPort
        rspBytes = rsp.to_bytes()
        self.server.send(rspBytes)
    
    def handleActorUnreg(self,msg):
        '''
        Handle the unregistration of an application actor with the service. 
        '''
        actReg = msg.actorUnreg
        appName = actReg.appName
        appVersion = actReg.version   
        appActorName = actReg.actorName
         
        self.logger.info("handleActorUnreg: %s %s" % (appName, appActorName))
        
        clientPort = self.unsetupClient(appName,appVersion,appActorName)
        
        # OptionL store in db host.app.vers.actr -> port? 
        
        rsp = disco_capnp.DiscoRep.new_message()
        rspMessage = rsp.init('actorUnreg')
        rspMessage.status = "ok"
        rspMessage.port = clientPort
        rspBytes = rsp.to_bytes()
        self.server.send(rspBytes)
        
    def buildInsertKeyValuePair(self,appName,msgType,kind,scope,host,port):
        '''
        Construct a database key,value pair to be used when a service is registered.
        The key allows the identifying the specific object in the actor the service
        is provided through. The value is a host:port pair.
        '''
        key = '/' + appName + '/' + msgType + '/' + kind
        if scope == "local":
            key = key + ":" + str(self.macAddress)
        value = str(host) + ':' + str(port)
        return (key,value)
    
    def buildLookupKey(self,appName,msgType,kind,scope,clientHost,clientActorName,clientInstanceName,clientPortName):
        '''
        Construct a key used to lookup a service. Construct also a string that identifies the client of the lookup 
        '''
        kindMap = { "sub" : "pub" , "clt" : "srv", "req" : "rep", "rep" : "req"} # Map the requestor's kind into the provider's kind
        key = '/' + appName + '/' + msgType + '/' + kindMap[kind]
        if scope == "local":                        # If the request is host-local, add the mac address to the end. Used to 
            key = key + ":" + str(self.macAddress)  # distinguish node-specific local requests. (The database is shared!)
        
        client = '/' + appName + '/' + clientActorName + '/' + clientHost + '/' + clientInstanceName + '/' + clientPortName 
        if scope == "local":
            client = client + ":" + str(self.macAddress)
        return (key,client)

    def handleServiceReg(self,msg):
        '''
        Handle the service registration message
        '''
        reqMsg = msg.serviceReg                             # Parse the message
        path = reqMsg.path
        appName = path.appName 
        appActorName = path.actorName
        msgType = path.msgType
        kind = str(path.kind)
        scope = str(path.scope)
        
        socket = reqMsg.socket
        host = socket.host
        port = socket.port
        
        self.logger.info("handleServiceReg: %s,%s,%s,%s,%s,%s" % (appName,msgType,kind,scope,host,port))
        (key,value) = self.buildInsertKeyValuePair(appName, msgType, kind, scope,host, port)
        clients = self.dbase.insert(key,value)
        
        self.registrations[self.appActorName(appName, appActorName)].append((key,value))
        
        rep = disco_capnp.DiscoRep.new_message()            # Construct response
        repMsg = rep.init('serviceReg')
        repMsg.status = "ok"
        repBytes = rep.to_bytes()
        self.server.send(repBytes)
        
        if len(clients) != 0:
            self.clientUpdates = [(key,(value),clients)]
    
    def handleServiceLookup(self,msg):
        '''
        Handle a service lookup message
        '''
        reqMsg = msg.serviceLookup                          # Parse the message
        path = reqMsg.path
        appName = path.appName
        msgType = path.msgType
        kind = str(path.kind)
        scope = str(path.scope)
        client = reqMsg.client
        clientActorHost = client.actorHost
        clientActorName = client.actorName
        clientInstanceName = client.instanceName
        clientPortName = client.portName
        client = (appName,clientActorHost,clientActorName,clientInstanceName,clientPortName)

        self.logger.info("handleServiceLookup:%s,%s,%s,%s,%s" 
                            % (appName,msgType,kind,scope,clientInstanceName))
        (key,client) = self.buildLookupKey(appName, msgType, kind, scope,
                                           clientActorHost, clientActorName, 
                                           clientInstanceName,clientPortName)
        result = self.dbase.fetch(key,client)
        
        rep = disco_capnp.DiscoRep.new_message()            # Construct the response: all providers of the requested service
        repMsg = rep.init('serviceLookup')
        repMsg.status = "ok"
        sockets = repMsg.init('sockets',len(result))
        i = 0
        for elt in result:
            pair = str(elt.decode('utf-8')).split(':')
            sockets[i].host = str(pair[0])
            sockets[i].port = int(pair[1])
            i += 1
        repBytes = rep.to_bytes()
        self.server.send(repBytes)
    
    def handle(self,msgBytes):
        '''
        Dispatch the request based on the message type
        '''
        msg = disco_capnp.DiscoReq.from_bytes(msgBytes)
        which = msg.which()
        if which == 'actorReg':
            self.handleActorReg(msg)
        elif which == "serviceReg":
            self.handleServiceReg(msg)
        elif which == "serviceLookup":
            self.handleServiceLookup(msg)
        elif which == 'actorUnreg':
            self.handleActorUnreg(msg)
        else:
            pass
        
    def handleNote(self,msg):
        '''
        Handle a notification message received from the database.
        The notification triggers the notification of client actors about the new service provider
        '''
        self.logger.info("handleNote: %s",str(msg))
        (key,value,clients) = msg                       # Parse notification message
        pair = re.split(':',value)
        host = pair[0]
        port = pair[1]
        for client in clients:                          # For each client:
            clientString = client.decode('utf-8')           # Parse the client string
            spl = re.split('/',clientString)
            skip = spl[0]
            appName = spl[1]
            actorName = spl[2]
            actorHost = spl[3]
            instanceName = spl[4]
            portMacPair = re.split(':',spl[5])
            portName = portMacPair[0]
            if len(portMacPair) > 1:
                macAddr = portMacPair[1]
            else:
                macAddr = None
            clientKeyBase = "/" + appName + '/' + actorName + "/"
            if clientKeyBase not in self.clients:
                continue
            if self.hostAddress != actorHost:
                continue
            clientSocket = self.clients[clientKeyBase]

            updMsg = disco_capnp.DiscoUpd.new_message() # Construct the notification message to be sent to the client actor
            updMsgPortUpd = updMsg.portUpdate
            updMsgClient = updMsgPortUpd.client
            updMsgClient.actorHost = actorHost
            updMsgClient.actorName = actorName
            updMsgClient.instanceName = instanceName
            updMsgClient.portName = portName
            updMsgPortUpd.scope = 'local' if macAddr != None else 'global'
            updMsgPortUpd.socket.host = host 
            updMsgPortUpd.socket.port = int(port)
            
            msgBytes = updMsg.to_bytes()
            self.logger.info("send update to actor %s.%s.%s:%s %s:%s" 
                             % (actorHost,actorName,instanceName,portName,str(host),str(port)))
            clientSocket.send(msgBytes)                     # Send message to client 

    def terminate(self):
        self.logger.info("terminating")
        # Clean up everything
        self.context.destroy()
        time.sleep(1.0)
        self.logger.info("terminated")
        os._exit(0)

    