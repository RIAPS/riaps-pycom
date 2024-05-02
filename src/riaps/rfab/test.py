import riaps.rfab.api
from fabric import Connection
# c = riaps.rfab.api.riaps.ResetTask([Connection("riaps-bcf6.local")])
# c.run()
# c.pretty_print()
from riaps.rfab.api.task import STATE, TaskRunner
import socket
from threading import Thread
import time
from pathlib import Path
from shutil import rmtree
import logging
from riaps.rfab.api.riaps import PycomInstallTask, ResetTask,UpdateNodeKey
from riaps.rfab.api.utils import make_log_folder
from functools import partial

kwargs = {'dry':False,'hide':False,'pty':False}

runner = TaskRunner([Connection('riaps-c189.local')],UpdateNodeKey,**kwargs)
runner.set_log_folder(make_log_folder("updateNodeKey"))
runner.run()
runner.pretty_print()