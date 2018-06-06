# Fabric tasks for transftering files to and from hosts
from .util import putFile, getFile
from fabric.api import env, task

@task
def get(fileName,localPrefix=''):
    """Transfer file from hosts (BBBs) to control host"""
    getFile(fileName, localPrefix)

# If transferring to a RIAPS account directory, use_sudo=False. 
# If transferring to a system location, use_sudo=True
@task
def put(fileName, localPrefix='', use_sudo=False):
    """Transfer file to hosts (BBBs) from control host"""
    putFile(fileName, localPrefix, use_sudo)