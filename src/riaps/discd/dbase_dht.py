'''
Discovery server database interface
Created on Oct 19, 2016

@author: riaps
'''

import typing
import re
import sys
import functools
import copy
import threading
import os
from os.path import join
from threading import RLock
import parse
import sched,time

from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.Hash import SHA256

import opendht as dht

import ctypes
import czmq
import zyre
from zyre import Zyre, ZyreEvent

import lmdb

try:
    import cPickle
    pickle = cPickle
except:
    cPickle = None
    import pickle

from riaps.consts.defs import *
from riaps.run.exc import *
from riaps.utils.ifaces import get_random_port
from riaps.utils.config import Config
from .dbase import DiscoDbase
import logging

class DhtPeerMon(threading.Thread):
    def __init__(self,context,hostAddress,riapsHome,dhtDbase,dhtPort):
        threading.Thread.__init__(self,daemon=False)
        self.logger = logging.getLogger(__name__)
        self.context = context
        self.hostAddress = hostAddress
        self.riapsHome = riapsHome
        self.control = None
        self.dhtDbase = dhtDbase
        self.dhtPort = dhtPort
        self.peers  = { }       # uuid : address - all peers
        self.peerGroup = set()  # set(uuid) of peer group members
        self.uuid = None
        self.logger.info('DhtPeerMon:__inited__')
    
    def setup(self):
        self.logger.info('DhtPeerMon:setup()')
        self.control = self.context.socket(zmq.PAIR)
        self.control.bind(const.discoDhtPeerMonEndpoint)
        return self.control

    def terminate(self):
        if self.control != None:
            self.control.send_pyobj(('stop',))
        else:
            self.setup()
            time.sleep(0.1)
            self.control.send_pyobj(('stop',))
    
    def peerHeaderKey(self,ipAddress):
        return b'riaps_disco@' + ipAddress.encode('utf-8')
    
    PEERMARK = b'CAFE'
    PEERGROUP = b'riaps_disco'
    PEERGROUP_STR = PEERGROUP.decode('utf-8')
    
    def run(self):
        self.zyre = Zyre(None)
        if self.logger.level == logging.DEBUG:
            self.zyre.set_verbose()
        else:
            pass
        self.uuid = self.zyre.uuid()
        self.zyre.set_interface(Config.NIC_NAME.encode('utf-8'))
        if Config.SECURITY:
            certFile = os.path.join(self.riapsHome,"keys",const.zmqCertificate)
            cert = czmq.Zcert.load(ctypes.c_char_p(certFile.encode('utf-8')))
            self.zyre.set_zcert(cert) 
        self.zyre.set_evasive_timeout(const.peerEvasiveTimeout)
        self.zyre.set_expired_timeout(const.peerExpiredTimeout)
        self.zyre.set_header(self.peerHeaderKey(self.hostAddress),self.PEERMARK)
        self.command = self.context.socket(zmq.PAIR)
        self.command.connect(const.discoDhtPeerMonEndpoint)
        self.zyre.start()
        self.zyre.join(self.PEERGROUP)
        self.zyreSocket = self.zyre.socket()
        self.poller = czmq.Zpoller(zyre.c_void_p(self.command.underlying),self.zyreSocket,0)
        while True:
            reader = self.poller.wait(-1)   # Wait forever
            if self.poller.terminated():
                self.logger.info("DhtPeerMon.run - poller terminated")
                break
            if type(reader) == zyre.c_void_p and reader.value == self.command.underlying:
                msg = self.command.recv_pyobj()
                self.logger.info('DhtPeerMon.run - command: %s' % str(msg))
                cmd = msg[0]
                if cmd == 'stop':
                    break 
                else:
                    pass                        # Should be error
            elif reader == self.zyreSocket:
                event = ZyreEvent(self.zyre)
                eType = event.type()
                _pName = event.peer_name()
                pUUID = event.peer_uuid()
                pAddr = event.peer_addr()
                group = event.group()
                _headers = event.headers()
                msg = event.get_msg()
                # if eType != b'EVASIVE':
                #     print("# %s %s %s %s %s %s %s" 
                #           % (str(eType),str(_pName),str(pUUID),str(pAddr),
                #              str(group),str(_headers),str(msg)))
                if eType == b'ENTER':
                    self.logger.info("DhtPeerMon.ENTER %s from %s" % (pUUID.decode('utf-8'),pAddr.decode('utf-8')))
                    try:
                        pAddrStr = pAddr.decode('UTF-8')
                        (peerIP,peerPort) = parse.parse("tcp://{}:{}",pAddrStr)
                        peerHeaderKey =  self.peerHeaderKey(peerIP)
                        _value = _headers.lookup(peerHeaderKey)
                        if (_value):
                            try:
                                value = ctypes.cast(_value,ctypes.c_char_p).value
                                assert value == self.PEERMARK
                                self.peers[pUUID] = (peerIP,peerPort)
                                self.logger.info("DhtPeerMon.ENTER valid peer")
                            except:
                                self.logger.info("DhtPeerMon.ENTER header value mismatch")
                        else:
                            self.logger.info("DhtPeerMon.ENTER header key mismatch")
                    except:
                        self.logger.info("DhtPeerMon.ENTER peer addr parsing error")
                elif pUUID not in self.peers:   # Skip the rest if this is not a peer
                    continue
                elif eType == b'JOIN':
                    groupName = group.decode()
                    peer = pUUID
                    self.logger.info("DhtPeerMon.JOIN %s from %s" % (groupName, pUUID.decode('utf-8'))) 
                    if group != self.PEERGROUP:
                        self.logger.info("DhtPeerMon.JOIN another group")
                        pass     
                    else:
                        self.peerGroup.add(peer)
                        self.zyre.whispers(peer,("%s://%d" % (self.PEERGROUP_STR,self.dhtPort)).encode('utf-8'))
                elif eType == b'SHOUT' or eType == b'WHISPER':
                    arg = msg.popstr().decode()
                    self.logger.info("DhtPeerMon.SHOUT %s = %s " % (pUUID.decode('utf-8'), arg))
                    try:
                        # pAddrStr = pAddr.decode('UTF-8')
                        # (peerIp,_peerPort) = parse.parse("tcp://{}:{}",pAddrStr)
                        # assert peerIp == self.peers[pUUID]
                        (peerIP,peerPort) = self.peers[pUUID]
                        (peerDhtPort,) = parse.parse("%s://{}" % self.PEERGROUP_STR,arg)
                        if peerDhtPort:
                            self.logger.info("DhtPeerMon.bootstrap %s:%s" % (peerIP,peerDhtPort))
                            self.dhtDbase.bootstrap(str(peerIP),str(peerDhtPort))
                    except:
                        self.logger.error("DhtPeerMon.bootstrap failed %r", sys.exc_info()[0])
                elif eType == b'LEAVE':
                    groupName = group.decode()
                    self.logger.info("DhtPeerMon.LEAVE %s from %s" % (pUUID.decode('utf-8'),groupName))
                    if group != self.PEERGROUP:
                        self.logger.info("DhtPeerMon.LEAVE another group")
                        pass 
                    else:
                        self.peerGroup.discard(pUUID)
                elif eType == b'EXIT':
                    self.logger.info("DhtPeerMon.EXIT %s " % (str(pUUID)))
                    if pUUID in self.peers: 
                        del self.peers[pUUID]
                        self.peerGroup.discard(pUUID)       
                else:
                    pass
        self.command.close()
        self.zyre.leave(self.PEERGROUP)
        self.zyre.stop()


class DhtBackup(object):
    '''
    Dht registration backup database. 
    The database is a collection of key:str -> [value:bytes] pairs 
    '''
    RIAPSAPPS = 'RIAPSAPPS'
    def __init__(self):
        '''
        Constructor
        '''
        self.logger = logging.getLogger(__name__)
        self.create = False
        self.dbase = None
        appFolder = os.getenv(DhtBackup.RIAPSAPPS, './')
        dbPath = join(appFolder,const.regDb) 
        mapSize = const.appDbSize * 1024 * 1024
        if os.path.exists(dbPath) and not os.access(dbPath,os.W_OK):
            raise BuildError("regDb is not writeable")
        self.dbLock = RLock() 
        while True:
            try:
                self.dbase = lmdb.open(dbPath,
                                       map_size = mapSize,
                                       metasync=True, 
                                       sync=True, 
                                       map_async=False,
                                       mode=0o700, 
                                       readahead=True, 
                                       create = self.create,
                                       writemap=False)
                self.logger.info('regDb opened (create = %s)' % str(self.create))
                break
            except lmdb.Error:
                self.create = True
            except:
                raise 
            
    def closeDbase(self):
        self.logger.info("regdDb closing")
        with self.dbLock:
            with self.dbase.begin() as txn:
                with txn.cursor() as curs:
                    go = True
                    while go:
                        go = curs.delete()
            self.dbase.close()
        self.logger.info('regDb closed')
    
    @staticmethod
    def unpickle(vl):
        res = pickle.loads(vl)
        return res if res else []          
    
    def getAllKeyValues(self):
        with self.dbLock:
            with self.dbase.begin() as txn:
                raw = list(txn.cursor().iternext())
                return [(k.decode('UTF-8'),[v for v in self.unpickle(vl)] if vl else []) 
                        for (k,vl) in raw]
    
    def clearDbase(self):
        with self.dbLock:
            with self.dbase.begin() as txn:
                with txn.cursor() as curs:
                    go = True
                    while go: go = curs.delete()
    
    def getKeyValues(self,key,default = None):
        assert self.dbase != None
        value = default
        if type(key) == str: key = key.encode('utf-8')
        with self.dbLock:
            with self.dbase.begin() as txn:
                _value = txn.get(key)
                if _value != None:
                    value = self.unpickle(_value)
        return value
    
    def addKeyValue(self,key,value):
        assert self.dbase != None
        res = False
        if type(key) == str: key = key.encode('utf-8')
        with self.dbLock:
            with self.dbase.begin(write=True) as txn:
                values = []
                _values = txn.get(key)
                if _values != None:
                    values = self.unpickle(_values)
                values += [value]
                _values = pickle.dumps(values)
                res = txn.put(key,_values)
        return res
    
    def delKey(self,key):
        assert self.dbase != None
        res = False
        if type(key) == str: key = key.encode('utf-8')
        with self.dbLock:
            with self.dbase.begin(write=True) as txn:
                res = txn.delete(key)
        return res
    
    def delKeyValue(self,key,value):
        assert self.dbase != None
        res = False
        if type(key) == str: key = key.encode('utf-8')
        with self.dbLock:
            with self.dbase.begin(write=True) as txn:
                values = []
                _values = txn.get(key)
                if _values != None:
                    values = self.unpickle(_values)
                values = values.remove(value) if value in values else values
                _values = pickle.dumps(values)
                res = txn.put(key,_values)
        return res

class DhtDbase(DiscoDbase):
    '''
    Discovery service database implemented using opendht
    '''
    def __init__(self,context_,hostAddress,dbaseLoc):
        '''
        Construct the dht  object.
        '''
        super().__init__(context_, dbaseLoc)
        self.logger = logging.getLogger(__name__)
        global theDiscoBase
        theDiscoBase = self
        self.context = context_ 
        self.hostAddress = hostAddress
        self.root = dbaseLoc
        self.riapsHome = os.getenv('RIAPSHOME', './')
        
        self.dht = None
        self.dhtPort = None
                      
        self.dataLock = RLock()
        self.updates = []
        self.clients = { }
        self.listeners = { }
        self.cancelled = []
        self.deletedMap = { }
        self.noClientsMap = { }
        
        self.republishMap = { }
        self.republisherStart = threading.Event()
        self.republisherDelay  = threading.Event()
        self.republisherDelayFunc = functools.partial(self.republisherDelay.wait)
        self.republisher = sched.scheduler(time.time,self.republisherDelayFunc)
        self.republisherThread = threading.Thread(name='dhtRepublisher',
                                                  target=self.dhtRepublishWorker,
                                                  daemon=False)
        self.republisherStop = False
        self.republishLock = RLock()

        self.regDb = DhtBackup()
        self.private_key = None
        self.cipher_rsa = None
        if Config.SECURITY:
            private_key_name = join(self.riapsHome,"keys/" + str(const.ctrlPrivateKey))
            with open(private_key_name, 'rb') as f: key = f.read()
            self.private_key = RSA.importKey(key)
            self.cipher_rsa = PKCS1_OAEP.new(self.private_key)
        self.peerMon = None
    
    def cleanupRegDb(self):
        keyValues = self.regDb.getAllKeyValues()
        if keyValues:
            self.logger.info("cleanup regdb")
            for (key,values) in keyValues:
                for value in values:
                    self.dhtRemove(key,value)
            self.regDb.clearDbase()
    
    def start(self):
        '''
        Start the database: connect to the root dht
        '''
        if self.root != None:
            pair = re.split(":",self.root)                      # Root host, probably run by control
            bootHost = str(pair[0])
            bootPort = int(pair[1])
        else:
            bootHost = const.discoDhtHost                       # Default host, 
            bootPort = const.discoDhtPort
        try:    
            self.logger.info("launching dht")
            config = dht.DhtConfig()
            config.setBootstrapMode(True)
            if Config.SECURITY:
                config.setIdentity(dht.Identity.generate("riaps-disco"))
            self.dht = dht.DhtRunner()
            self.dhtPort = get_random_port()
            self.dht.run(port=self.dhtPort,config=config)  # Run on a random, free port
        except Exception:
            raise DatabaseError("dht.start: %s" % sys.exc_info()[0])

        if const.discoDhtBoot and bootHost and bootPort:
            try:    
                self.logger.info("dht.bootstrap on %s:%s" % (str(bootHost),str(bootPort)))
                self.dht.bootstrap(str(bootHost),str(bootPort))
            except Exception:
                raise DatabaseError("dht.bootstrap: %s" % sys.exc_info()[0])
        # Create and start peer monitor    
        self.peerMon = DhtPeerMon(self.context,self.hostAddress,self.riapsHome,self.dht,self.dhtPort)
        self.peerMon.setup()  
        self.peerMon.start()
        time.sleep(0.1)
        self.cleanupRegDb()                                     # If something in the backup db, discard from the dht
        self.republisherThread.start()                          # Start republisher
    
    def bootstrap(self,peerIP:str,peerDhtPort:str):
        self.dht.boostrape(peerIP,peerDhtPort)
    
    def fetchUpdates(self):
        '''
        Check and fetch the updated values of the subscribed keys if any
        Called from another thread
        '''
        with self.dataLock:
            if len(self.updates) == 0: return []
            try:
                res = []
                for (key,value) in set(self.updates):
                    clients = self.clients.get(key,None)
                    if clients: 
                        res.append((key,value,clients))
                    else:
                        self.noClientsMap = list(set(self.noClientsMap.get(key,[]) + [value]))
                self.updates = []
                return res
            except Exception:
                raise DatabaseError("dht: fetch %s" % sys.exc_info()[0])
            except OSError:
                raise DatabaseError("OS error")
    
    def encryptData(self,data : bytes) -> bytes:
        '''
        Encrypt data with RSA cipher, if security is enabled
        '''
        return self.cipher_rsa.encrypt(data) if Config.SECURITY else data
    
    def decryptData(self,data : bytes) -> bytes:
        '''
        Decrypt data with RSA cipher, if security is enabled
        '''
        return self.cipher_rsa.decrypt(data) if Config.SECURITY else data
    
    def dhtValue(self,value : str) -> dht.Value:
        '''
        Convert a string value to bytes (wiht optional encryption) then to a dht.Value
        '''
        return dht.Value(self.encryptData(value.encode('UTF-8')))
    
    def strValue(self,value : dht.Value) -> str:
        '''
        Retrieve the raw bytes from a dht.Value, optionally decrypt it, then covert it into a str. 
        '''
        return self.decryptData(value.data).decode('UTF-8')
            
    @staticmethod
    def delValue(value: str) -> str:
        return '-' + value
    
    @staticmethod
    def orgValue(value : str) -> str:
        return value[1:] if value[0] == '-' else value
    
    @staticmethod
    def isDelValue(value: str) -> bool:
        return value[0] == '-'

    @staticmethod
    def filterDelValues(values : [str]) -> [str]:
        out = [v[1:] for v in values if v[0] == '-']
        return [v for v in values if v[0] != '-' and v not in out]
    
    def dhtGet(self,key : str) -> [str]:
        '''
        Retrieve values belonging to a key. Lowest level op.
        '''
        def wrapper(gen):                   # Filter values where decryption fails 
            while True:
                try:
                    yield next(gen)
                except StopIteration:
                    break
                except ValueError:
                    pass
        keyhash = dht.InfoHash.get(key)
        dhtValues = self.dht.get(keyhash)
        values = list(wrapper(map(self.strValue,dhtValues)))
        self.logger.info('dhtGet[%s]: %r' % (key,values))
        return values
    
    def dhtPut(self,key : str,value : str) -> bool:
        '''
        Add a value to key. Lowest level op. Note: one key may have multiple values. 
        '''
        keyhash = dht.InfoHash.get(key)
        res = self.dht.put(keyhash,self.dhtValue(value))
        self.logger.info('dhtPut[%s]:= %r (%r)' % (key,value,res))
        return res
                       
    def dhtValueCallback(self, key : str, value : bytes, expired : bool) -> bool:
        '''
        ValueCallback - called when a key's value get updated. 
        '''
        with self.dataLock:
            if key in self.cancelled:
                self.logger.info('dhtValueCallback[%s]: cancelled' % key)
                token = self.listeners.get(key,None)
                if token:
                    # self.dht.cancelListen(token)
                    del self.listeners[key]
                self.cancelled.remove(key)
                return False
            if key not in self.listeners:
                self.logger.error('dhtValueCallback[%r] - already cancelled ' % key)
                return False
            try:
                value_ = self.strValue(value)
            except ValueError:
                self.logger.error('dhtValueCallback[%s]: <INVALID>(%r)' % (key,expired))
                return True
            self.logger.info('dhtValueCallback[%s].value: %r(%r)' % (key,value_,expired))
            if expired or self.isDelValue(value_) or \
                (key,value_) in self.republishMap or \
                self.deletedMap.get(key,None) == value_:
                pass
            else:
                self.updates += [(key,value_)]
            if expired or self.isDelValue(value_):
                _value = self.orgValue(value_)
                self.deletedMap[key] = _value
                self.updates = [(k,v) for (k,v) in self.updates if k != key and v != _value]
            return True
    
    def dhtListen(self,key):
        '''
        Set up a listener for the key. 
        The listener will call the ValueCallback with the key + other 
        arguments supplied by dht. 
        Return a listener token. 
        '''
        keyhash = dht.InfoHash.get(key)
        token = self.dht.listen(keyhash,
                                functools.partial(self.dhtValueCallback,key))
        return token 

    def dhtRemove(self,key,value):
        '''
        Remove a specific k/v pair from the dht.
        Because we cannot delete it, we add a 'deleted' version of the value to the key.
        The original k/v will eventually expire, because it will not be republished. 
        '''
        self.logger.info('dhtRemove[%s]=%r' % (key,value))
        values = self.dhtGet(key)
        if value in values: 
            _res = self.dhtPut(key,self.delValue(value))
            self.deletedMap[key] = value
        return list(set(values) - set([value]))
                    
    def dhtAddClient(self,key,client):
        '''
        Add a client to the key. Clients are local service clients
        (app/actor/component/ports) that need to connect to the providers.
        '''
        with self.dataLock:
            self.clients[key] = list(set(self.clients.get(key,[]) + [client]))
            if key not in self.listeners:
                self.listeners[key] = self.dhtListen(key)
            if key in self.noClientsMap:
                values = self.noClientsMap.get(key,[])
                for value in values:
                    self.updates += [(key,value)]
                del self.noClientsMap[key]
    
    def dhtDelClient(self,key,client):
        '''
        '''
        self.logger.info('dhtdelClient(%s,%r)' % (key,client))
        with self.dataLock:
            if client in self.clients.get(key,[]):
                self.clients[key].remove(client)
                if not self.clients[key]:
                    listener = self.listeners.get(key,None)
                    if listener:
                        self.cancelled += [key]
                        # self.dht.cancelListen(listener)
                        # del self.listeners[key]

    def dhtDelete(self,key):
        '''
        Delete all the values of a key.
        Cancel the listener (if any), mark all values as deleted  
        '''
        self.logger.info('dhtDelete[%s]' % (key,))
        with self.dataLock:
            values = self.dhtGet(key)
            clients = self.clients.get(key,[])
            if clients: del self.clients[key]
            listener = self.listeners.get(key,None)
            if listener:
                self.cancelled += [key]
                # self.dht.cancelListen(listener)
                # del self.listeners[key]
            for value in values:
                _res = self.dhtPut(key,self.delValue(value))
                self.deletedMap[key] = value
        return values
    
    def dhtRepublishWorker(self):
        '''
        Worker thread that runs the 'republisher' scheduler.
        '''
        self.republisherDelay.clear()
        while True:
            self.republisherStart.wait()                # Wait for re(start)
            self.republisher.run()                      # Run scheduler
            self.republisherStart.clear()
            if self.republisherStop: break              # Stop when flag is set 
            self.logger.info('republisher cycle')
            
    def dhtRepublish(self,key,value):           
        '''
        Do the actual republishing. Called by the scheduler.
        '''
        self.logger.info('dhtRepublish[%s]=%r' % (key,value))
        if self.republisherStop: return
        with self.republishLock:
            event = self.republishMap.get((key,value),None)     # Check if this republisher is still active
            if event:
                self.dhtPut(key,value)                          # Republish k/v pair on the dht
                self.republishMap[(key,value)] = \
                    self.republisher.enter(const.discoDhtRepublishTimeout,
                                           1,
                                           self.dhtRepublish,[key,value])       # Re-register for the next cycle. 
        
    def addToRepublish(self,key,value):
        '''
        Add a k/v pair to the republisher
        '''
        self.logger.info('dhtAddToRepublish[%s]=%r' % (key,value))
        with self.republishLock:
            event = self.republisher.enter(const.discoDhtRepublishTimeout,
                                           1,
                                           self.dhtRepublish,
                                           [key,value])
            self.republishMap[(key,value)] = event
            self.republisherStart.set()
    
    def delFromRepublish(self,key,value):
        '''
        Remove a k/v pair from the republisher. 
        '''
        self.logger.info('dhtDelFromRepublish[%s]=%r' % (key,value))
        with self.republishLock:
            event = self.republishMap.get((key,value),None)
            if event:
                self.republisher.cancel(event)
                del self.republishMap[(key,value)]

    def delFromRepublishAll(self,key,values):
        '''
        Remove all k/v pair/s from the republisher. 
        '''
        self.logger.info('dhtRemoveFromRepublish[%s]=%r' % (key,str(values)))
        with self.republishLock:
            for value in values:
                event = self.republishMap.get((key,value),None)
                if event:
                    self.republisher.cancel(event)
                    del self.republishMap[(key,value)]
                    
    def stopRepublisher(self):
        self.republisherStop = True
        with self.republishLock:
            for (_pair,event) in self.republishMap.items():
                if event:
                    self.republisher.cancel(event)
        self.republisherStart.set()
        self.republisherDelay.set()
        self.republisherThread.join()
        self.logger.info("dht.republisher stopped")
                    
    def insert(self,key:str,value:str) -> [str]:
        '''
        Insert value under key and return list of clients of value (if any). 
        A key may have multiple values associated with it.
        '''
        assert self.dht != None
        self.logger.info("dht.insert[%r] := %r" % (key,value))
        try:
            _values = self.dhtGet(key)
            clientsToNotify = []
            if value not in _values:  
                _res = self.dhtPut(key,value)
                self.regDb.addKeyValue(key, value)              # Save k/v into backup db
                self.addToRepublish(key,value)                  # Add k/v to republisher
                clientsToNotify = self.clients.get(key,[])      # Return interested clients
            return clientsToNotify
        except Exception:
            raise DatabaseError("dht.insert: %s" % sys.exc_info()[0])
        except OSError:
            raise DatabaseError("OS error")

    def fetch(self,key:str,client:str) -> [str]:
        '''
        Fetch value(s) under key. 
        Retrieve values, remove deleted values from result, add client to list of clients interested in updates
        '''
        self.logger.info("dht.fetch[%r] -> %r" % (key,client))
        try:
            self.dhtAddClient(key,client)
            values = self.filterDelValues(self.dhtGet(key))
            self.logger.info("dht.fetch[%r] = %r" % (key,values))
            return values
        except Exception:
            raise DatabaseError("dht.fetch: %s" % sys.exc_info()[0])
        except OSError:
            raise DatabaseError("OS error")
          
        
    def remove(self,key:str,value:str) -> [str]:
        '''
        Remove value from values under key.
        '''
        self.logger.info("dht.remove[%r]:%r" % (key,value))
        try:
            self.delFromRepublish(key,value)                    # Delete k/v from republisher
            self.regDb.delKeyValue(key, value)                  # Delete k/v from db
            values = self.dhtRemove(key,value)
            return values
        except Exception:
            raise DatabaseError("dht.remove: %s" % sys.exc_info()[0])
        except OSError:
            raise DatabaseError("OS error")
        
    def detach(self, key:str, target:str):
        '''
        Detach actor (updates) from keys
        '''
        self.logger.info("dht.detach: %s : %r " % (key,target))
        self.dhtDelClient(key,target)
        
    def terminate(self):
        self.logger.info("dht.terminate")
        self.regDb.closeDbase()
        self.stopRepublisher()
        if self.peerMon: 
            self.peerMon.terminate()
            self.logger.info("peerMon terminated")
        time.sleep(1)
        if self.dht:
            self.dht.join() 
            self.dht.shutdown()
        self.logger.info("dht.terminated")
           
    

