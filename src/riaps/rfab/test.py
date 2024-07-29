
from fabric import Connection
import socket
from threading import Thread
import time
from pathlib import Path
from shutil import rmtree
import logging
from riaps.rfab.api.riaps import PycomInstallTask, ResetTask,UpdateNodeKey
from riaps.rfab.api.utils import make_log_folder
from riaps.rfab.api.deplo import DeploStartManual
from riaps.rfab.api.task import TaskRunner
from functools import partial

kwargs = {'dry':False,'hide':False,'pty':True}

runner = TaskRunner([Connection('riaps-22d9.local')],DeploStartManual,**kwargs)
runner.set_log_folder(make_log_folder("test"))
runner.run()