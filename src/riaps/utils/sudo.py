'''
sudo operations
Created on Jan 19, 2018

@author: riaps
'''

import os
import re
import stat
import time
import signal
import subprocess
import psutil
import threading
import traceback

import fabric
from fabric import tasks
from fabric.api import run
from fabric.api import env
from fabric.network import disconnect_all
 
from socket import gethostname
 
import functools
import atexit
 
# Local host
env.hosts = [gethostname()]
 
# THIS SHOULD BE IMPORTED FROM A SECURED SOURCE
# Standard riaps setup
env.user = 'riaps'
env.password = 'riaps@isis'
#env.sudo_password = 'riaps@isis'
# END OF IMPORT
# Shell
env.shell = "/bin/bash -l -i -c"
 
def run(cmd):
    res = fabric.operations.sudo(cmd)
    return res
 
def sudo(cmd):
    exe = functools.partial(run,cmd=cmd)
    res = tasks.execute(exe)
    return res
 
def cleanup():
    fabric.network.disconnect_all()
 
atexit.register(cleanup)

is_su_flag = '?'
 
def is_su():
    global is_su_flag
    if is_su_flag == '?' : is_su_flag = (os.getuid() == 0)
    return is_su_flag
 
def riaps_sudo(cmd,timeout=None):
    try:
        if is_su(): 
            full = ['sudo'] + cmd.split(' ')
            proc = subprocess.Popen(full)
            proc.wait(timeout)
            return proc.returncode
        else:
            # res = sudo(cmd)
            print ('IGN: sudo ' + cmd)
            res = False
            return res
    except:
        # traceback.print_exc()
        print("sudo '%s' failed" % cmd)
    return None

