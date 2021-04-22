'''
Created on Dec 16, 2017

@author: riaps
'''
import traceback
import pydevd
from riaps.utils.config import Config


def riaps_trace_setup(debug):
    pair = debug.split(':')
    try:
        if len(pair) == 1:  # We got a hostname, no port
            pydevd.settrace(str(pair[0]))
        elif len(pair) == 2:  # Correct host:port pair
            (host, port) = pair
            host = None if len(host) == 0 else host
            port = 5678 if len(port) == 0 else int(port)  # Default pydevd debug port
            print('Waiting on debug server using \'%s:%s\'' % (str(host), str(port)))
            pydevd.settrace(host=host, port=port)
            return True
        else:
            print('Invalid debug argument: %s - ignored' % debug)
            return False
    except:
        traceback.print_exc()
        print('Unable to connect debug server using \'%s\' - no tracing' % debug)
        return False

    
def riaps_trace(debug=None, prog=None):
    ''' Setup trace mode and wait for the debug server.
    
    @debug: Debug server control string of the form 'hostname:portname', 
            both of which are optional, ':' defaulting to localhost:5678
            
    @prog:  Label for the program, looked up in the riaps configuration file.
    
    First, it attempts to connect to the debug server using the debug argument (if present).
    Second, it tries to connect to the debug server using the information from the configuration file.
    If the config file argument is empty, it silently returns.  
    Returns: True of False depending on whether the program is running in trace mode.
     
    '''
    ok = False
    if debug != None: ok = riaps_trace_setup(debug)
    if not ok and prog != None and hasattr(Config, prog):
        debug = getattr(Config, prog)
        if len(debug) > 0: 
            ok = riaps_trace_setup(debug)
    return ok

