'''
Created on Apr 23, 2020

@author: riaps
'''

from riaps.run.comp import Component
from enum import Enum
import inspect
import functools
from threading import RLock
try:
    import cPickle
    pickle = cPickle
except:
    cPickle = None
    import pickle
    
import traceback
    
# import pprint

        
class FSM(Component):
    '''
    Finite-State Machine component base class.
    '''
    _MSG_ = '_msg_'
    _MSG_GET_ = 'msg'
    _MSG_GET_PYOBJ_ = 'msg_pyobj'
    
    fsmLock = RLock()
    
    def __init__(self, initial=None):
        super(FSM, self).__init__()
        cls = self.__class__
        with FSM.fsmLock:
            if not hasattr(cls, '__fsm__'):
                # Collect states
                assert hasattr(cls, 'states'), 'class %r does not have any states' % cls
                states = cls.states
                assert inspect.isclass(states), '%r is not a class' % states
                assert issubclass(states, Enum), '%r is not an Enum' % states
                cls._state_map_ = cls.states._member_map_
                # Collect events
                assert hasattr(cls, 'events'), 'class %r does not have any events' % cls
                events = cls.events
                assert inspect.isclass(events), '%r is not a class' % events
                assert issubclass(events, Enum), '%r is not an Enum' % events
                cls._event_map_ = cls.events._member_map_  
                cls._e2name_map_ = { }  
                # Collect entries
                cls._entry_map_ = { }
                for _name, state in cls._state_map_.items():
                    if hasattr(state, '__entry__'):
                        cls._entry_map_[id(state)] = state.__dict__['__entry__']
                # Collect exits
                cls._exit_map_ = { }
                for _name, state in cls._state_map_.items():
                    if hasattr(state, '__exit__'):
                        cls._exit_map_[id(state)] = state.__dict__['__exit__']
                # Collect transitions
                cls._event_list_ = elist = cls._event_map_.values()
                cls._state_list_ = slist = cls._state_map_.values()
                cls._trans_map_ = { }
                assert initial in cls._state_list_, 'State %r is not among states'
                cls._initial_ = initial
                for _name, event in cls._event_map_.items():
                    assert event in elist, 'Event %r is not among events(%r)' % (event, elist) 
                    cls._e2name_map_[id(event)] = _name
                    if hasattr(event, '__on__'):
                        on_map = { }
                        states = event.__on__
                        for state in states:
                            assert state in slist, 'State %r not among states(%r)' % (state, slist)
                            assert id(state) in event.__dict__, 'State %r is not known for event %r' % (state, event)
                            tlist = event.__dict__[id(state)]
                            for trans in tlist: 
                                guard = trans['__guard__']
                                assert callable(guard), 'Guard %r is not callable' % guard
                                then = trans['__then__']
                                assert then == None or then in slist, 'Next state %r is not among states(%r)' % (then, slist) 
                            on_map[id(state)] = tlist
                        cls._trans_map_[id(event)] = on_map             
                # pprint.pprint(cls._trans_map_)
                setattr(cls, '__fsm__', True)
        # Add event handlers
        for name, event in cls._event_map_.items():
            hname = 'on_' + name
            functor = functools.partial(self._update, event)
            # setattr(cls,hname,functor)
            setattr(self, hname, functor)
        self._current_ = cls._initial_
    
    @property     
    def state(self):
        return self._current_
    
    @state.setter
    def state(self, _state):
        assert _state in self.__class__._state_list_
        self._current_ = _state
    
    def _recv(self, port):
        return getattr(port, FSM._MSG_)
    
    def _recv_pyobj(self, port):
        return pickle.loads(getattr(port, FSM._MSG_))    
        
    def _port_setup(self, port):
        if not hasattr(port, FSM._MSG_):
            setattr(port, FSM._MSG_, None)
            get_msg = functools.partial(self._recv, port)
            setattr(port, FSM._MSG_GET_, get_msg)
            get_pyobj = functools.partial(self._recv_pyobj, port)
            setattr(port, FSM._MSG_GET_PYOBJ_, get_pyobj)

    def _recv_message(self, cls, event):
        try:
            port = getattr(self, cls._e2name_map_[id(event)])
            self._port_setup(port)
            setattr(port, FSM._MSG_, port.recv())
        except:
            traceback.print_exc()
            pass
               
    def _update(self, event):
        cls = self.__class__
        cid = id(self._current_)
        # print("%r" % event)
        on_map = cls._trans_map_.get(id(event))
        self._recv_message(cls, event)
        if on_map:
            tlist = on_map.get(cid)
            if tlist:
                fired, prev = False, self._current_
                for trans in tlist: 
                    guard = trans['__guard__']
                    then = trans['__then__']
                    func = trans['__func__']
                    cond = guard(self)
                    if (cond):
                        if fired:
                            self.handleNondeterminism(event, prev)
                        else:
                            exit_func = cls._exit_map_.get(cid)
                            if exit_func: exit_func(self)
                            func(self)
                            next_ = then if then else self._current_
                            entry_func = cls._entry_map_.get(id(next_))
                            if entry_func: entry_func(self)
                            self._current_ = next_
                            fired = True
                    else:
                        continue
            else:
                self.handleUnhandledEvent(event, self._current_)
        else:
            self.handleNoTransition(event)
    
    def handleNondeterminism(self, event, state):
        self.logger.error('Event %r in state %r has non-deterministic behavior' % (event, state))
        
    def handleUnhandledEvent(self, event, state):
        self.logger.info('Event %r is not handled in state %r' % (event, state))
        
    def handleNoTransition(self, event):
        self.logger.info('Event %r has no "on" transitions' % event)    
    
    class entry(object):

        def __init__(self, state):
            # type of state is states?
            self.state = state
        
        def __call__(self, f):

            def wrapped(*args):
                f(*args)

            self.state.__dict__['__entry__'] = wrapped
            return wrapped
    
    class exit(object):

        def __init__(self, state):
            self.state = state
        
        def __call__(self, f):

            def wrapped(*args):
                f(*args)

            self.state.__dict__['__exit__'] = wrapped
            return wrapped
                
    class on(object):

        def __init__(self, event, state, guard=None, then=None):
            self.event = event
            self.state = state
            self.guard = guard if guard else lambda self: True 
            self.then = then
            
        def __call__(self, f):

            def wrapped(*args):
                f(*args)

            if not hasattr(self.event, '__on__'): self.event.__on__ = [ ]
            self.event.__on__ += [self.state]
            if id(self.state) not in self.event.__dict__: self.event.__dict__[id(self.state)] = []
            self.event.__dict__[id(self.state)] += [{ '__guard__': self.guard, '__then__': self.then, '__func__': wrapped}]
            return wrapped

