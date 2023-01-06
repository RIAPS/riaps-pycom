# 
# Fault simulation
#

import ctypes
import os


def exit():
    '''
    process exit
    '''
    os._exit(0)
    
def crash():
    ''' 
    process crash 
    '''
    ctypes.string_at(0)
    
def kill(s):
    ''' 
    process kill
    '''
    os.system("pkill -SIGKILL -f %s" % s)

def panic():
    '''
    kernel panic - use with extreme care
    '''
    os.system('sync')
    os.system('echo 1 > /proc/sys/kernel/sysrq')
    os.system('echo c > /proc/sysrq-trigger')


