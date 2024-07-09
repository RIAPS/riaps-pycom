'''
Created on June 14, 2024

Based on code from pyzmq

@author: riaps

'''


import time
import sys
import os
import logging

import threading
import errno

import traceback
import time

from threading import Thread
from typing import Any, Callable, List, Optional, Tuple
import zmq

from zmq import ENOTSOCK, ETERM, PUSH, QUEUE, ZMQBindError, ZMQError, device

class Relay(threading.Thread):
    """A variant for the 0MQ ThreadProxySteerable.
       Ports:
       - in: DEALER (with identity = appName.actorName.PID). 
             Connected to resource/fault/etc. monitors and depm control socket for this actor.
       - out: PAIR. Actor connects to it.
       - mon: PUB.  depm monitor socket connects to it.
       - ctrl:PAIR. Used to stop relay thread. 
       Flows:
       - in -> (out,mon) : 
       - -> ctrl: manages (stops, etc.) relay thread
       - out ->  


    You do not pass Socket instances to this, but rather Socket types::

        Relay(in_socket_type, out_socket_type, mon_socket_type, ctrl_socket_type)

    For instance::

        dev = Device(zmq.QUEUE, zmq.DEALER, zmq.ROUTER)

    Similar to zmq.device, but socket types instead of sockets themselves are
    passed, and the sockets are created in the work thread, to avoid issues
    with thread safety. As a result, additional bind_{in|out} and
    connect_{in|out} methods and setsockopt_{in|out} allow users to specify
    connections for the sockets.

    Parameters
    ----------
    {in|out|mon|ctrl}_type : int
        zmq socket types, to be passed later to context.socket(). e.g.
        zmq.PUB, zmq.SUB, zmq.REQ. If out_type is < 0, then in_socket is used
        for both in_socket and out_socket.

    Methods
    -------
    bind_{in|out|mon|ctrl}(iface)
        passthrough for ``{in|out|mon|ctrl}_socket.bind(iface)``, to be called in the thread
    connect_{in|out|mon|ctrl}(iface)
        passthrough for ``{in|out|mon|ctrl}_socket.connect(iface)``, to be called in the
        thread
    setsockopt_{in|out|mon|ctrl}(opt,value)
        passthrough for ``{in|out|mon|ctrl}_socket.setsockopt(opt, value)``, to be called in
        the thread

    Attributes
    ----------
    daemon : bool
        sets whether the thread should be run as a daemon
        Default is true, because if it is false, the thread will not
        exit unless it is killed
    context_factory : callable (class attribute)
        Function for creating the Context. This will be Context.instance
        due to implementation via threads..
    """
    in_type: int
    out_type: int
    mon_type: int
    ctrl_type: int

    _in_binds: List[str]
    _in_connects: List[str]
    _in_sockopts: List[Tuple[int, Any]]
    _out_binds: List[str]
    _out_connects: List[str]
    _out_sockopts: List[Tuple[int, Any]]
    _mon_binds: List[str]
    _mon_connects: List[str]
    _mon_sockopts: List[Tuple[int, Any]]
    _ctrl_binds: List[str]
    _ctrl_connects: List[str]
    _ctrl_sockopts: List[Tuple[int, Any]]
    _random_addrs: List[str]
    _sockets: List[zmq.Socket]

    def __init__(
        self,
        context,
        name : str,
        in_type: Optional[int] = None,
        out_type: Optional[int] = None,
        mon_type: Optional[int]= None,
        ctrl_type: Optional[int] = None
    ) -> None:
        threading.Thread.__init__(self,name = f'Relay-{name}',daemon=False)
        self.name = f'Relay{name}'        
        self.logger = logging.getLogger(__name__)
        self.context = context
        
        if in_type is None:
            raise TypeError("in_type must be specified")

        self.in_type = in_type
        self._in_binds = []
        self._in_connects = []
        self._in_sockopts = []
 
        if out_type is None:
            raise TypeError("out_type must be specified")   
        self.out_type = out_type
        self._out_binds = []
        self._out_connects = []
        self._out_sockopts = []
 
        self.mon_type = mon_type
        self._mon_binds = []
        self._mon_connects = []
        self._mon_sockopts = []

        self.ctrl_type = ctrl_type
        self._ctrl_binds = []
        self._ctrl_connects = []
        self._ctrl_sockopts = []
        
        self._random_addrs = []
        self.daemon = True
        self.done = False
        self._sockets = []

    def bind_in(self, addr: str) -> None:
        self._in_binds.append(addr)

    def bind_in_to_random_port(self, addr: str, *args, **kwargs) -> int:
        port = self._reserve_random_port(addr, *args, **kwargs)
        self.bind_in('%s:%i' % (addr, port))
        return port
    
    def connect_in(self, addr: str) -> None:
        self._in_connects.append(addr)

    def setsockopt_in(self, opt: int, value: Any) -> None:
        self._in_sockopts.append((opt, value))

    def bind_out(self, addr: str) -> None:
        self._out_binds.append(addr)

    def bind_out_to_random_port(self, addr: str, *args, **kwargs) -> int:
        port = self._reserve_random_port(addr, *args, **kwargs)
        self.bind_out('%s:%i' % (addr, port))
        return port

    def connect_out(self, addr: str):
        self._out_connects.append(addr)

    def setsockopt_out(self, opt: int, value: Any):
        self._out_sockopts.append((opt, value))

    def bind_mon(self, addr):
        self._mon_binds.append(addr)

    def bind_mon_to_random_port(self, addr, *args, **kwargs):
        port = self._reserve_random_port(addr, *args, **kwargs)
        self.bind_mon('%s:%i' % (addr, port))
        return port

    def connect_mon(self, addr):
        self._mon_connects.append(addr)

    def setsockopt_mon(self, opt, value):
        self._mon_sockopts.append((opt, value))

    def bind_ctrl(self, addr):
        self._ctrl_binds.append(addr)

    def bind_ctrl_to_random_port(self, addr, *args, **kwargs):
        port = self._reserve_random_port(addr, *args, **kwargs)
        self.bind_ctrl('%s:%i' % (addr, port))
        return port

    def connect_ctrl(self, addr):
        self._ctrl_connects.append(addr)

    def setsockopt_ctrl(self, opt, value):
        self._ctrl_sockopts.append((opt, value))

    def _reserve_random_port(self, addr: str, *args, **kwargs) -> int:
        with self.context as ctx:
            with ctx.socket(PUSH) as binder:
                for i in range(5):
                    port = binder.bind_to_random_port(addr, *args, **kwargs)
                    new_addr = '%s:%i' % (addr, port)
                    if new_addr in self._random_addrs:
                        continue
                    else:
                        break
                else:
                    raise ZMQBindError("Could not reserve random port.")
                self._random_addrs.append(new_addr)
        return port

    def _setup_sockets(self) -> Tuple[zmq.Socket, zmq.Socket, zmq.Socket, zmq.Socket]:
        ctx = self.context
        
        # create the sockets
        ins = ctx.socket(self.in_type)
        self._sockets.append(ins)
        
        if self.out_type < 0:
            outs = ins
        else:
            outs = ctx.socket(self.out_type)
            self._sockets.append(outs)

        # set sockopts (must be done first, in case of zmq.IDENTITY)
        for opt, value in self._in_sockopts:
            ins.setsockopt(opt, value)
        for opt, value in self._out_sockopts:
            outs.setsockopt(opt, value)

        for iface in self._in_binds:
            ins.bind(iface)
        for iface in self._out_binds:
            outs.bind(iface)

        for iface in self._in_connects:
            ins.connect(iface)
        for iface in self._out_connects:
            outs.connect(iface)

        if self.mon_type is not None:
            mons = ctx.socket(self.mon_type)
            self._sockets.append(mons)
    
            # set sockopts (must be done first, in case of zmq.IDENTITY)
            for opt, value in self._mon_sockopts:
                mons.setsockopt(opt, value)
    
            for iface in self._mon_binds:
                mons.bind(iface)
    
            for iface in self._mon_connects:
                mons.connect(iface)
        else:
            mons = None
        
        if self.ctrl_type is not None:
            ctrls = ctx.socket(self.ctrl_type)
            self._sockets.append(ctrls)
    
            for opt, value in self._ctrl_sockopts:
                ctrls.setsockopt(opt, value)
    
            for iface in self._ctrl_binds:
                ctrls.bind(iface)
            
            for iface in self._ctrl_connects:
                ctrls.connect(iface)
        else:
            ctrls = None
            
        return ins, outs, mons, ctrls

    def _close_sockets(self):
        """Cleanup sockets we created"""
        for s in self._sockets:
            if s and not s.closed:
                s.close()

    def run(self) -> None:
        """wrap run_device in try/catch ETERM"""
        try:
            self.run_device()
        except ZMQError as e:
            if e.errno in {ETERM, ENOTSOCK}:
                # silence TERM, ENOTSOCK errors, because this should be a clean shutdown
                pass
            else:
                raise
        finally:
            self.done = True
            self._close_sockets()

    def run_device(self):
        ins, outs, mons, ctrls = self._setup_sockets()
        self.poller = zmq.Poller()
        self.poller.register(ins,zmq.POLLIN)
        self.poller.register(outs,zmq.POLLIN)
        if ctrls:
            self.poller.register(ctrls,zmq.POLLIN)
        while True:
            sockets = dict(self.poller.poll())
            if len(sockets) == 0: break
            if ins in sockets:
                _msg = ins.recv()
                outs.send(_msg)
                if mons: mons.send(_msg)
                self.logger.info(f"relay {self.name}: msg to actor")
            if outs in sockets:
                _msg = outs.recv()
                if mons: mons.send(_msg)
                ins.send(_msg)
                self.logger.info(f"relay {self.name}: msg from actor")
            if ctrls in sockets:
                _msg = ctrls.recv()
                if _msg == b'TERMINATE': break
                else: pass
        self.logger.info(f"relay {self.name}: terminated")
        





