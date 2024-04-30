from fabric import Group
from riaps.rfab.api.task import Task
from .helpers import *

class TimeConfig(Task):
    mode = None

    @classmethod
    def configure(cls, mode):
        assert(mode in ['standalone','slave','master'])
        cls.mode = mode

    def get_config(self):
        if self.mode is None:
            raise Exception("TimeConfig must be configure(d) with a mode")
        return self.sudo(f"timesyncctl config {self.mode}")

class TimeStatus(Task):
    def get_status(self):
        return self.sudo("timesyncctl status")

class TimeRestart(Task):
    def restart(self):
        return self.sudo("timesyncctl restart")

class TimeDate(Task):
    def get_date(self):
        return self.run("date")

class TimeRdate(Task):
    def run_rdate(self):
        return self.sudo("rdate -s -n -4 time.nist.gov")