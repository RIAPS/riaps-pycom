'''
sudo operations
Created on Jan 19, 2018

@author: riaps
'''

import os
import subprocess
# import traceback

is_su_flag = '?'

 
def is_su():
    global is_su_flag
    if is_su_flag == '?': is_su_flag = (os.getuid() == 0)
    return is_su_flag

 
def riaps_sudo(cmd, timeout=None):
    try:
        if is_su(): 
            # full = ['sudo'] + cmd.split(' ')
            full = cmd.split(' ')
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

