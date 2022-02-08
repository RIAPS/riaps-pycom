'''
Created on Oct 10, 2016

@author: riaps
'''

import zmq


class RIAPSError(Exception):

    def __init__(self, message):
        super(RIAPSError, self).__init__(message)


class BuildError(RIAPSError):

    def __init__(self, message):
        super(BuildError, self).__init__(message)


class SetupError(RIAPSError):

    def __init__(self, message):
        super(SetupError, self).__init__(message)


class StateError(RIAPSError):

    def __init__(self, message):
        super(StateError, self).__init__(message)

        
class ControlError(RIAPSError):

    def __init__(self, message):
        super(ControlError, self).__init__(message)


class DatabaseError(RIAPSError):

    def __init__(self, message):
        super(DatabaseError, self).__init__(message)

        
class OperationError(RIAPSError):

    def __init__(self, message):
        super(OperationError, self).__init__(message)

        
class PortError(RIAPSError):
    EAGAIN = zmq.EAGAIN  # Timeout on recv/send
    EPROTO = zmq.EFSM  # Protocol error on req/rep
    ETERM = zmq.ETERM  # Context terminated    
    EFAULT = zmq.EFAULT  # Invalid message
    EROUTE = zmq.EHOSTUNREACH  # Routing failed

    def __init__(self, message, errno):
        super(PortError, self).__init__(message)
        self.errno = errno
    
