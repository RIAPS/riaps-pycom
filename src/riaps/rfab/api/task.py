'''
- Some tasks will have a step that requires output from a prior step
'''

import functools
from threading import Thread
import time
from invoke.exceptions import UnexpectedExit
from riaps.rfab.api.helpers import RFabGroupResult
import socket
from fabric import Result as FabResult
import logging

class Result(FabResult):
    def to_log(self):
        log = [f"Command: {self.command}",
               f"Exited: {self.exited}"]
        for t,stream in zip(["STDOUT","STDERR"],[self.stdout,self.stderr]):
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

from enum import Enum, auto
class STATE(Enum):
    INIT = auto()
    SUCCEEDED = auto()
    FAILED = auto()
    EXCEPTED = auto()

class _step_factory:
    def __init__(self,func,**kwargs):
        self.__name__ = func.__name__
        self.func = func
        self.kwargs = kwargs

    def __call__(self,owner):
        '''
        owner: a _ctx instance
        '''
        class _step:
            '''Single command
            Customizeable pass/fail test
            Accepts kwargs for Connection command?
            Leaf instances are in a specific _conntext
            '''
            def __init__(self,func,owner,**kwargs):
                functools.update_wrapper(self,func)
                self.func = func
                self.input_iter = None
                self.owner = owner
                if input := kwargs.get('input',None):
                    try:
                        self.input_iter = iter(input)
                    except TypeError:
                        self.input_iter = iter([input])

            def __call__(self,*args,**kwargs):
                if self.input_iter:
                    kwargs = {**kwargs , **{i.__name__ : self.owner.results.get(i.__name__) for i in self.input_iter}}
                return self.func(*args,**kwargs)
        return _step(self.func,owner,**self.kwargs)

def SkipResult(connection,command,msg):
    return Result(connection=connection,command=command,stdout=msg,stderr='',exited=0)


def _make_ctx_factory(steps: dict): #dict[str,_step_factory]
    def ctx_factory(conn,logger,**kwargs):
        class _ctx:
            '''A single Connection object's context, instances of steps
            '''
            def __init__(self,conn,logger,**kwargs):
                self.conn = conn
                self.kwargs = kwargs
                self.steps = {k:v(self) for k,v in steps.items()} #dict[str,_step]
                self.results = {n:None for n in self.steps.keys()}

                self.s = STATE.INIT
                self._step_gen = (iter(self.steps.keys()))
                self.curr_step: str = next(self._step_gen)
                self.final_res = None
                self.logger = logger

            def run_one(self) -> bool:
                sfunc = self.steps[self.curr_step]
                self.logger.info(f"Running {sfunc.func.__qualname__}...")
                try:
                    res: Result = sfunc(self.conn,self.logger,**kwargs)
                    self.logger.info(Result.to_log(res))
                    self.results[self.curr_step] = res
                    self.curr_step = next(self._step_gen)
                    return True
                except StopIteration:
                    self.final_res = self.results[self.curr_step]
                    self.s = STATE.SUCCEEDED
                except UnexpectedExit as e:
                    self.final_res = self.results[self.curr_step] = e.result
                    self.s = STATE.FAILED
                    self.logger.warn(Result.to_log(e.result))
                    self.logger.warn(f"{sfunc.func.__qualname__} FAILED")
                except Exception as e:
                    self.final_res = self.results[self.curr_step] = e
                    self.s = STATE.EXCEPTED
                    self.logger.error(f"{sfunc.func.__qualname__} EXCEPTION")
                    self.logger.exception(e)
                return False

            def run_all(self):
                while(more_steps := self.run_one()):
                    pass
            
            def done(self) -> bool:
                return self.s != STATE.INIT

        return _ctx(conn,logger,**kwargs)
    return ctx_factory


from pathlib import Path
from shutil import rmtree
class Task(dict): # dict[Connection,_ctx]
    '''Base class for Rfab tasks, executes N steps for M connections
    All M connections must be able to execute all N steps. If more complicated
    patterns are needed, use multiple Tasks.
    - Multi-threaded: yes/no
        - If multithreaded, lock-step yes/no
    - Stop on problem or keep going
    '''
    _steps = {} # Must be filled by subclass
    _make_ctx = None


    def step(func=None, **kwargs):
        if func: # Case where step() decorator is used without args
            return _step_factory(func)
        else: # Decorator has args passed
            def wrapper(func):
                return _step_factory(func,**kwargs)
            return wrapper

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        cls._steps = {name:f for name,f in cls.__dict__.items() if isinstance(f,_step_factory)}
        cls._make_ctx = staticmethod(_make_ctx_factory(cls._steps))

    def __init__(self,
        connections,
        **kwargs,
    ):
        """Creates instance with instantiated contexts for each connection

        Parameters:
            connections (list[fabric.Connection]): Connections to each targeted host
            kwargs: kwargs passed to each connection-context
        """
        self.connections = connections
        self.kwargs = kwargs
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel("INFO")
        logdir = Path("/tmp",self.__class__.__name__)
        if logdir.exists():
            rmtree(logdir)
        logdir.mkdir()
        for c in self.connections:
            logger = self.logger.getChild(c.host)
            logger.propagate = False
            logger.addHandler(logging.FileHandler(Path(logdir,c.host)))
            self[c] = self._make_ctx(c,logger,**self.kwargs)


    def run(self):
        #TODO: Enable configuration of serial/stepped execution
        self._run_parallel()


    def _run_parallel(self):
        #TODO: Possible move to asyncio?
        threads = [Thread(None,ctx.run_all,name=f"thread_{c.host}") for c,ctx in self.items()]
        [t.start() for t in threads]
        running = True
        while(running):
            time.sleep(1)
            waitlist = ', '.join([t.name for t in threads if t.is_alive()])
            if len(waitlist) == 0:
                break
            # print(f"Waiting on: {waitlist}")
        

    def _run_serial(self):
        for _, ctx in self.items():
            ctx.run_all()
    
    def pretty_print(self):
        _succeeded = {c:ctx for c,ctx in self.items() if ctx.s == STATE.SUCCEEDED}
        _failed = {c:ctx for c,ctx in self.items() if ctx.s == STATE.FAILED}
        _excepted = {c:ctx for c,ctx in self.items() if ctx.s == STATE.EXCEPTED}
        for c, ctx in self.items():
            try:
                assert(ctx.done())
            except AssertionError:
                print(f"NOT DONE FOR {c.host}")
        
        if _succeeded:
            print(f"Succeeded ({len(_succeeded)}):")
            for c,ctx in _succeeded.items():
                r = ctx.final_res
                RFabGroupResult._print_multiline(f"{c.host}:",r.stdout,2)
        if _failed:
            print(f"Failed ({len(_failed)}):")
            for c,ctx in _failed.items():
                r: Result = ctx.final_res
                print(f"  {c.host}:")
                print(f"  {r.command}")
                RFabGroupResult._print_multiline(f"STDOUT:",r.stdout,4)
                RFabGroupResult._print_multiline(f"STDERR:",r.stderr,4)
        if _excepted:
            print(f"Excepted ({len(_excepted)}):")
            for c,ctx in _excepted.items():
                r: f = ctx.final_res
                hint=None
                exception_hints=[(socket.gaierror,"No known address for host")]
                for eh in exception_hints:
                    T, h = eh
                    if isinstance(r,T):
                        hint = h
                RFabGroupResult._print_multiline(f"{c.host}.exception:",str(r),2)
                if hint is not None:
                    RFabGroupResult._print_multiline(f"^^^ HINT:",hint,2)

        
        
            
