# Helper methods for wrapping built-in Fabric methods
from fabric import api
from fabric.api import task, env, put, get, settings
from fabric.context_managers import hide

# Wrapper for fabric.api.run to capture and combine and console output
def run(command):
    with hide('everything'), settings(warn_only=True):
        result = api.run(command)
        print("["+env.host+"] " + command)
        if result != '':
            print(result)
        return result

# Wrapper for fabric.api.sudo to capture and combine any console output
def sudo(command):
    with hide('everything'), settings(warn_only=True):
        result = api.sudo(command)
        print("["+env.host+"] sudo " + command)
        if result != '':
            print(result)
        return result

def getFile(fileName,localPrefix=''):
    """Transfer file from hosts (BBBs) to control host"""
    get(env.nodePath + fileName, env.localPath+localPrefix)

# If transferring to a RIAPS account directory, use_sudo=False. 
# If transferring to a system location, use_sudo=True
def putFile(fileName, localPrefix='', use_sudo=False):
    """Transfer file to hosts (BBBs) from control host"""
    put(env.localPath + localPrefix + fileName, env.nodePath + fileName, use_sudo)