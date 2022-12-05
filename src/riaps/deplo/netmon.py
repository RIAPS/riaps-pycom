'''
Resource monitors

Created on Nov 23, 2017

@author: riaps
'''

# Based on https://github.com/raboof/nethogs
# By Philip Semanchuk (psemanchuk@caktusgroup.com) November 2016
# Copyright waived; released into public domain as is.

import os
import stat
import time
import ctypes
import signal
import datetime
import psutil
import threading
from threading import RLock
import logging
import traceback

import zmq
from zmq import devices
from zmq.error import ZMQError

from riaps.consts.defs import *
from riaps.run.exc import *
from riaps.proto import deplo_capnp
from riaps.utils.sudo import riaps_sudo
from riaps.utils.config import Config
from riaps.utils.names import *

#######################
# BEGIN CONFIGURATION #
#######################

# You can use this to monitor only certain devices, like:
# device_names = ['enp4s0', 'docker0']
# device_names = []

# LIBRARY_NAME has to be exact, although it doesn't need to include the full path.
# The version tagged as 0.8.5 (download link below) builds a library with this name.
# https://github.com/raboof/nethogs/archive/v0.8.5.tar.gz
# LIBRARY_NAME = 'libnethogs.so.master'

# EXPERIMENTAL: Optionally, specify a capture filter in pcap format (same as
# used by tcpdump(1)) or None. See `man pcap-filter` for full information.
# Note that this feature is EXPERIMENTAL (in libnethogs) and may be removed or
# changed in an incompatible way in a future release.
# example:
# FILTER = 'port 80 or port 8080 or port 443'
# FILTER = None

#####################
# END CONFIGURATION #
#####################

# Here are some definitions from libnethogs.h
# https://github.com/raboof/nethogs/blob/master/src/libnethogs.h
# Possible actions are NETHOGS_APP_ACTION_SET & NETHOGS_APP_ACTION_REMOVE
# NHAction REMOVE is sent when nethogs decides a connection or a process has died. There are two
# timeouts defined, PROCESSTIMEOUT (150 seconds) and CONNTIMEOUT (50 seconds). AFAICT, the latter
# trumps the former so we see a REMOVE action after ~45-50 seconds of inactivity.
class NHAction():
    SET = 1
    REMOVE = 2

    MAP = {SET: 'SET', REMOVE: 'REMOVE'}

class NHLoopStatus():
    """Return codes from nethogsmonitor_loop()"""
    OK = 0
    FAILURE = 1
    NO_DEVICE = 2

    MAP = {OK: 'OK', FAILURE: 'FAILURE', NO_DEVICE: 'NO_DEVICE'}

# The sent/received KB/sec values are averaged over 5 seconds; see PERIOD in nethogs.h.
# https://github.com/raboof/nethogs/blob/master/src/nethogs.h#L43
# sent_bytes and recv_bytes are a running total
class NHMonitorRecord(ctypes.Structure):
    """ctypes version of the struct of the same name from libnethogs.h"""
    _fields_ = (('record_id', ctypes.c_int),
                ('name', ctypes.c_char_p),
                ('pid', ctypes.c_int),
                ('uid', ctypes.c_uint32),
                ('device_name', ctypes.c_char_p),
                ('sent_bytes', ctypes.c_uint64),
                ('recv_bytes', ctypes.c_uint64),
                ('sent_kbs', ctypes.c_float),
                ('recv_kbs', ctypes.c_float),
                )


# def signal_handler(signal, frame):
#     print('SIGINT received; requesting exit from monitor loop.')
#     lib.nethogsmonitor_breakloop()


# def dev_args(devnames):
#     """
#     Return the appropriate ctypes arguments for a device name list, to pass
#     to libnethogs ``nethogsmonitor_loop_devices``. The return value is a
#     2-tuple of devc (``ctypes.c_int``) and devicenames (``ctypes.POINTER``)
#     to an array of ``ctypes.c_char``).
# 
#     :param devnames: list of device names to monitor
#     :type devnames: list
#     :return: 2-tuple of devc, devicenames ctypes arguments
#     :rtype: tuple
#     """
#     devc = len(devnames)
#     devnames_type = ctypes.c_char_p * devc
#     devnames_arg = devnames_type()
#     for idx, val in enumerate(devnames):
#         devnames_arg[idx] = (val + chr(0)).encode('ascii')
#     return ctypes.c_int(devc), ctypes.cast(
#         devnames_arg, ctypes.POINTER(ctypes.c_char_p)
#     )


# def run_monitor_loop(lib, devnames):
#     # Create a type for my callback func. The callback func returns void (None), and accepts as
#     # params an int and a pointer to a NHMonitorRecord instance.
#     # The params and return type of the callback function are mandated by nethogsmonitor_loop().
#     # See libnethogs.h.
#     CALLBACK_FUNC_TYPE = ctypes.CFUNCTYPE(
#         ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(NHMonitorRecord)
#     )
# 
#     filter_arg = FILTER
#     if filter_arg is not None:
#         filter_arg = ctypes.c_char_p(filter_arg.encode('ascii'))
# 
#     if len(devnames) < 1:
#         # monitor all devices
#         rc = lib.nethogsmonitor_loop(
#             CALLBACK_FUNC_TYPE(network_activity_callback),
#             filter_arg
#         )
#     else:
#         devc, devicenames = dev_args(devnames)
#         rc = lib.nethogsmonitor_loop_devices(
#             CALLBACK_FUNC_TYPE(network_activity_callback),
#             filter_arg,
#             devc,
#             devicenames,
#             ctypes.c_bool(False)
#         )
# 
#     if rc != NHLoopStatus.OK:
#         print('nethogsmonitor_loop returned {}'.format(NHLoopStatus.MAP[rc]))
#     else:
#         print('exiting monitor loop')

# def network_activity_callback(action, data):
#     print(datetime.datetime.now().strftime('@%H:%M:%S.%f'))
# 
#     # NHAction type is either SET or REMOVE. I have never seen nethogs send an unknown action
#     # type, and I don't expect it to do so.
#     action_type = NHAction.MAP.get(action, 'Unknown')
# 
#     print('NHAction: {}'.format(action_type))
#     print('Record id: {}'.format(data.contents.record_id))
#     print('Name: {}'.format(data.contents.name))
#     print('PID: {}'.format(data.contents.pid))
#     print('UID: {}'.format(data.contents.uid))
#     print('Device name: {}'.format(data.contents.device_name.decode('ascii')))
#     print('Sent/Recv bytes: {} / {}'.format(data.contents.sent_bytes, data.contents.recv_bytes))
#     print('Sent/Recv kbs: {} / {}'.format(data.contents.sent_kbs, data.contents.recv_kbs))
#     print('-' * 30)

#############       Main begins here      ##############

# signal.signal(signal.SIGINT, signal_handler)
# signal.signal(signal.SIGTERM, signal_handler)
# 
# lib = ctypes.CDLL(LIBRARY_NAME)
# 
# monitor_thread = threading.Thread(
#     target=run_monitor_loop, args=(lib, device_names,)
# )
# 
# monitor_thread.start()
# 
# done = False
# while not done:
#     monitor_thread.join(0.3)
#     done = not monitor_thread.is_alive()

class NetMonitorThread(threading.Thread):

    def __init__(self,parent):
        threading.Thread.__init__(self,name='NetMonitor',daemon=False)
        self.logger = logging.getLogger(__name__)
        self.parent = parent
        self.context = self.parent.context
        self.terminated = threading.Event()  # Set when the monitor is to be terminated
        self.terminated.clear()
        self.running = threading.Event()  # Cleared when the monitor is not to run
        self.running.set()
        self.stopped = threading.Event()  # Set if the monitor is stopped
        self.stopped.clear()
        self.alive = False
        self.rlock = RLock()
        self.device_names = [Config.NIC_NAME]
        self.lib = ctypes.CDLL(const.nethogsLibrary)
        assert const.nethogsTimeout >= 0 
        self.notifier = None
        self.notifierPort = None
        self.devices = { }              # app.actor -> (device,pid)
        self.pid2Key = { }              # pid -> app.actor
        self.pid2Rate = { }             # pid -> rate
        
    
    def addProc(self, appName,actName,proc):
        self.logger.info("addProc %s.%s [%d]" % (appName,actName,proc.pid))
        with self.rlock:
            self.pid2Key[proc.pid] = '???'
            self.pid2Rate[proc.pid] = 0
        
    def delProc(self,appName,actName,proc):
        with self.rlock:
            fullName = appName + '.' + actName
            del self.devices[fullName]
            del self.pid2Key[proc.pid]
            del self.pid2Rate[proc.pid]

    def addClientDevice(self,appName,actorName,device,proc,rate):
        while self.notifierPort == None:
            time.sleep(0.1)
        try:
            rate = int(rate)    # Rate in bits/sec
        except:
            rate = 0         
        self.logger.info("adding client %s.%s [%i] %i" % (appName,actorName,proc.pid,rate))  
        with self.rlock:
            key = str(appName) + "." + str(actorName)
            device.connect_in('tcp://127.0.0.1:%i' % self.notifierPort)
            identity = actorIdentity(appName,actorName,proc.pid)
            self.logger.info("zmqdev id = %s" % identity)
            self.devices[key] = (device,identity)
            self.pid2Key[proc.pid] = key
            self.pid2Rate[proc.pid] = rate
    
    def is_running(self):
        return self.alive
    
    def restart(self):
        self.stopped.clear()
        self.running.set()

    def dev_args(self,devnames):
        """
        Return the appropriate ctypes arguments for a device name list, to pass
        to libnethogs ``nethogsmonitor_loop_devices``. The return value is a
        2-tuple of devc (``ctypes.c_int``) and devicenames (``ctypes.POINTER``)
        to an array of ``ctypes.c_char``).
    
        :param devnames: list of device names to monitor
        :type devnames: list
        :return: 2-tuple of devc, devicenames ctypes arguments
        :rtype: tuple
        """
        devc = len(devnames)
        devnames_type = ctypes.c_char_p * devc
        devnames_arg = devnames_type()
        for idx, val in enumerate(devnames):
            devnames_arg[idx] = (val + chr(0)).encode('ascii')
        return ctypes.c_int(devc), ctypes.cast(
            devnames_arg, ctypes.POINTER(ctypes.c_char_p)
        )

    def network_activity_callback(self,_action, data):
        # NHAction type is either SET or REMOVE. 
        # _action_type = NHAction.MAP.get(_action, 'Unknown')
        # _record_id = data.contents.record_id
        _name = data.contents.name
        _pid = data.contents.pid
        _uid = data.contents.uid
        if ((_pid == 0) or (_uid == 0)): return
        # _device_name = data.contents.device_name.decode('ascii')
        _sent_bytes = data.contents.sent_bytes
        _recv_bytes = data.contents.recv_bytes
        _sent_kbs = data.contents.sent_kbs  # KBytes/sec
        _recv_kbs = data.contents.recv_kbs  # KBytes/sec

        with self.rlock:
            # print("callback %i,%i" % (int(_uid), int(_pid)),flush=True)
            if _pid in self.pid2Key:
                key = self.pid2Key[_pid]
                rate = self.pid2Rate[_pid]
                _sent_kbs = int(_sent_kbs * 10 * 1024)  # Convert to kbits/sec
                self.logger.info("checking [%d] %i > %i" % (_pid,_sent_kbs,rate))
                if (rate != 0) and (_sent_kbs > rate):
                    self.logger.info("%s exceeded rate limit %i kbps" % (key,rate/10))
                    msg = deplo_capnp.DeplCmd.new_message()
                    msgCmd = msg.init('resourceMsg')
                    msgMessage = msgCmd.init('resNetX')
                    msgMessage.msg = "X"
                    msgBytes = msg.to_bytes()
                    payload = zmq.Frame(msgBytes)
                    _device,identity = self.devices[key]
                    header = identity.encode(encoding='utf-8')
                    self.notifier.send_multipart([header,payload])
                    self.logger.info("XNet sent to [%d]" % (_pid))
                    time.sleep(0.1)  
        
    def run(self):
        self.name = 'NetMonitor-%r' % self.ident
        self.notifier = self.context.socket(zmq.ROUTER)
        # self.notifier.setsockopt(zmq.SNDTIMEO,const.deplEndpointSendTimeout)
        self.notifierPort = self.notifier.bind_to_random_port('tcp://127.0.0.1') 
        self.alive = True
        self.logger.info("NetMonitor started")
        time.sleep(0.001)
        
        # Create a type for my callback func. The callback func returns void (None), and accepts as
        # params an int and a pointer to a NHMonitorRecord instance.
        # The params and return type of the callback function are mandated by nethogsmonitor_loop().
        # See libnethogs.h.
        CALLBACK_FUNC_TYPE = ctypes.CFUNCTYPE(
            ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(NHMonitorRecord)
            )

        # filter_arg = FILTER
        # if filter_arg is not None:
        #    filter_arg = ctypes.c_char_p(filter_arg.encode('ascii'))
        
        filter_arg = None
        try:
            while True:
                if not self.running.is_set():
                    self.stopped.set()
                    self.running.wait()
                if self.terminated.is_set(): break
                self.logger.info("starting nethogsmonitor_loop")
                devc, devicenames = self.dev_args(self.device_names)
                rc = self.lib.nethogsmonitor_loop_devices(
                        CALLBACK_FUNC_TYPE(self.network_activity_callback),
                        filter_arg,
                        devc,
                        devicenames,
                        ctypes.c_bool(False),
                        ctypes.c_int(const.nethogsTimeout)
                    )
                if rc != NHLoopStatus.OK:
                    self.logger.info('nethogsmonitor_loop returned {}'.format(NHLoopStatus.MAP[rc]))
                    break
                else:
                    self.logger.info('exiting monitoring loop') 
                                     
                if not self.running.is_set(): continue
                if self.terminated.is_set(): break
        except:
            self.logger.error("NetMonitorThread failure")
            traceback.print_exc()     
        self.logger.info("NetMonitorThread stopped")
        
    def stop(self):
        self.lib.nethogsmonitor_breakloop()
        self.running.clear()
        self.stopped.wait()
        
    def terminate(self):
        self.logger.info("terminating")
        self.lib.nethogsmonitor_breakloop()
        self.terminated.set()
        self.logger.info("terminated")
