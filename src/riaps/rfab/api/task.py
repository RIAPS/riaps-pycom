import logging.handlers
from threading import Thread
import time
from invoke.exceptions import UnexpectedExit
import socket
from fabric import Result as FabResult
from fabric.connection import Connection
from fabric.transfer import Result as TransferResult
import logging
import sys
from pathlib import Path
from shutil import rmtree


def Result_to_log(res):
    log = [f"Command: {res.command}",
            f"Exited: {res.exited}"]
    for t,stream in zip(["STDOUT","STDERR"],[res.stdout,res.stderr]):
        if len(stream) > 0:
            # out = stream.splitlines()
            # if len(out) > 1:
            #     lines =  "\n".join([f"{t}:",]+out)
            #     log.extend(lines)
            # else:
            #     lines = f"{t}: {out[0]}"
            #     log.append(lines)
            log.append(f"{t}: {stream}")
    return "\n".join(log)
    
def TransferResult_to_log(res):
    log = [f"TRANSFER FILE",
           f"Local  (rel): {res.orig_local}",
           f"Local  (abs): {res.local}",
           f"Remote (rel): {res.orig_remote}",
           f"Remote (abs): {res.remote}"]
    return "\n".join(log)

from enum import Enum, auto
class STATE(Enum):
    INIT = auto()
    SUCCEEDED = auto()
    FAILED = auto()
    EXCEPTED = auto()

class SkipResult(FabResult):
    def __init__(self,connection,command,stdout,stderr='',exited=0):
        super().__init__(connection=connection,command=command,stdout=stdout,stderr=stderr,exited=exited)

class Result(FabResult): pass

class BadExit(UnexpectedExit):
    def __init__(self,exc: UnexpectedExit,msg=None):
        super().__init__(exc.result,exc.reason)
        self.msg = msg or ""

class Task:
    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        cls._steps = {}
        cls._params = {}
        for name,f in cls.__dict__.items():
            if name[0:2] != '__':
                if callable(f):
                    cls._steps[name] = f
                else:
                    cls._params[name] = f

    def __init__(self,
        connection,
        **kwargs,
    ):
        """Creates instance with instantiated contexts for each connection

        Parameters:
            connections (list[fabric.Connection]): Connections to each targeted host
            kwargs: kwargs passed to each connection-context
        """
        self.connection : Connection = connection
        self.kwargs = kwargs
        self.kwargs['hide'] = True
        self.results = {name:None for name in self._steps.values()}
        self.state = STATE.INIT
        self.final_res = None
        parentlogger = logging.getLogger(self.__class__.__name__)
        self.logger = parentlogger.getChild(self.connection.host)
        self.logger.setLevel("INFO")
        self._step_gen = (iter(self._steps.keys()))
        self.curr_step: str = next(self._step_gen)

    def _run_one(self):
        func = self._steps[self.curr_step]
        self.logger.info(f"Running {self.curr_step}...")
        try:
            res = func(self)
            if isinstance(res,TransferResult):
                self.logger.info(TransferResult_to_log(res))
                res = Result(connection=res.connection,stdout=f"{res.local} <--> {res.remote}")
            elif isinstance(res,FabResult):
                self.logger.info(Result_to_log(res))
            self.results[self.curr_step] = res
            self.curr_step = next(self._step_gen)
            return True
        except StopIteration:
            self.final_res = self.results[self.curr_step]
            self.state = STATE.SUCCEEDED
        except UnexpectedExit as e:
            if not isinstance(e,BadExit):
                e = BadExit(e)
            self.final_res = self.results[self.curr_step] = e
            self.state = STATE.FAILED
            self.logger.warn(Result_to_log(e.result))
            if len(e.msg):
                self.logger.warn(f"Hint: {e.msg}")
            self.logger.warn(f"{func.__qualname__} FAILED")
        except Exception as e:
            self.final_res = self.results[self.curr_step] = e
            self.state = STATE.EXCEPTED
            self.logger.error(f"{func.__qualname__} EXCEPTION")
            self.logger.exception(e)
        return False
    
    def _run_all(self):
        while(more_steps := self._run_one()):
            pass

    def done(self) -> bool:
        return self.state != STATE.INIT

    def put(self, file, **kwargs):
        return self.connection.put(file,**kwargs)
    
    def get(self, remote, local, **kwargs):
        return self.connection.get(remote,local,**kwargs)
                
    def sudo(self,cmd,**kwargs):
        kw = self.kwargs | kwargs
        fail_msg = kwargs.pop("fail_msg",None)
        try: 
            return self.connection.sudo(cmd,**kw)
        except UnexpectedExit as e:
            if fail_msg:
                raise BadExit(e,fail_msg)
            raise e
    
    def run(self,cmd,**kwargs):
        fail_msg = kwargs.pop("fail_msg",None)
        kw = self.kwargs | kwargs
        try:
            return self.connection.run(cmd,**kw)
        except UnexpectedExit as e:
            if fail_msg:
                raise BadExit(e,fail_msg)
            raise e


def _print_multiline(log_func,header_str,stream,indent=0):
        lines = stream.splitlines()
        if len(lines) == 1:
            log_func(f"{' '.rjust(indent)}{header_str} {lines[0]}")
            return
        log_func(f"{' '.rjust(indent)}{header_str}")
        [log_func(f"{' '.rjust(indent+2)}{l}") for l in lines]

class TaskRunner:
    def __init__(self,hosts,task,**kwargs):
        super().__init__()
        self.taskClass = task
        self.hosts = hosts
        self.rootlogger = logging.getLogger("TaskRunner")
        self.rootlogger.addHandler(logging.StreamHandler(sys.stdout))
        self.rootlogger.setLevel("WARN")
        if kwargs.pop('verbose',False):
            self.rootlogger.setLevel("INFO")
        self.log_folder = kwargs.pop('log_folder',None)
        self.logger = self.rootlogger.getChild('task-runner')
        self.kwargs = kwargs
        self.ctxs = {c:task(c,**kwargs) for c in hosts}

    def set_log_folder(self,path):
        logdir = Path(path)
        assert logdir.exists(), f"Log folder does not exist: {logdir.absolute()}"
        for conn,ctx in self.ctxs.items():
            ctx.logger.addHandler(logging.FileHandler(Path(logdir,conn.host)))
            ctx.logger.propagate = False
        self.logger.addHandler(logging.FileHandler(Path(logdir,"task-runner")))

    def run(self):
        self._run_parallel()
        self.pretty_print()

    def _run_parallel(self):
        #TODO: Possible move to asyncio?
        threads = [Thread(None,ctx._run_all,name=f"thread_{c.host}") for c,ctx in self.ctxs.items()]
        [t.start() for t in threads]
        running = True
        while(running):
            time.sleep(1)
            waitlist = ', '.join([t.name for t in threads if t.is_alive()])
            if len(waitlist) == 0:
                break
            # print(f"Waiting on: {waitlist}")

    def ok(self) -> bool:
        return all([ctx.state == STATE.SUCCEEDED for ctx in self.ctxs.values()])

    def pretty_print(self):
        _succeeded = {c:ctx for c,ctx in self.ctxs.items() if ctx.state == STATE.SUCCEEDED}
        _failed = {c:ctx for c,ctx in self.ctxs.items() if ctx.state == STATE.FAILED}
        _excepted = {c:ctx for c,ctx in self.ctxs.items() if ctx.state == STATE.EXCEPTED}
        for c, ctx in self.ctxs.items():
            try:
                assert(ctx.done())
            except AssertionError:
                self.logger.error(f"NOT DONE FOR {c.host}")
        
        if _succeeded:
            self.logger.info(f"Succeeded ({len(_succeeded)}):")
            for c,ctx in _succeeded.items():
                r = ctx.final_res
                _print_multiline(self.logger.info,f"{c.host}:",r.stdout,2)
        if _failed:
            self.logger.error(f"Failed ({len(_failed)}):")
            for c,ctx in _failed.items():
                e: BadExit = ctx.final_res
                self.logger.error(f"  host: {c.host}:")
                self.logger.error(f"  cmd:  {e.result.command}")
                self.logger.error(f"  exit code: {e.result.exited}")
                if len(e.msg):
                    self.logger.error(f"  Hint: {e.msg}")
                if len(e.result.stdout):
                    _print_multiline(self.logger.error,f"STDOUT:",e.result.stdout,4)
                if len(e.result.stderr):
                    _print_multiline(self.logger.error,f"STDERR:",e.result.stderr,4)
        if _excepted:
            self.logger.error(f"Excepted ({len(_excepted)}):")
            for c,ctx in _excepted.items():
                r = ctx.final_res
                hint=None
                exception_hints=[(socket.gaierror,"No known address for host")]
                for eh in exception_hints:
                    T, h = eh
                    if isinstance(r,T):
                        hint = h
                _print_multiline(self.logger.error,f"{c.host}.exception:",str(r),2)
                if hint is not None:
                    _print_multiline(self.logger.error,f"^^^ HINT:",hint,2)

