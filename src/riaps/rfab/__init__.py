from typing import List
from invoke import Program, Argument, Collection
from invoke.parser import Argument
from invoke.exceptions import Exit
from fabric import ThreadingGroup, Config
from riaps.rfab.api import utils
from .invoke import system
from .invoke import riaps
from .invoke import timesync
from .invoke import deplo


ns = Collection()
ns.add_collection(Collection.from_module(system))
ns.add_collection(Collection.from_module(riaps))
ns.add_collection(Collection.from_module(timesync))
ns.add_collection(Collection.from_module(deplo))

# class RfabConfig(Config):
#     def __init__(self,*args,**kwargs):
#         super().__init__(*args,**kwargs)
#         riapsHome = os.getenv('RIAPSHOME')
#         if riapsHome is None:
#             riapsHome = os.getcwd()
#             print(f"RIAPS Configuration - RIAPSHOME is not set, using {riapsHome}")
#         riapsApps = os.getenv('RIAPSAPPS')
#         if riapsApps is None:
#             riapsApps = '/home/riaps/riaps_apps'
#             print(f"RIAPS Configuration - RIAPSAPPS  is not set, using {riapsApps}")
#         self._set(riapsHome=riapsHome)
#         self._set(riapsApps=riapsApps)

class RfabProgram(Program):
    def core_args(self) -> List[Argument]:
        core_args = super().core_args()
        extra_args = [Argument(names=('role','r'), help = "RIAPS role name to run command for",default="remote"),
                      Argument(names=('v'), kind=bool, help = "Show remote output"),
                      Argument(names=('host','H'),help = "Run command on host (repeatable)",kind=list),
                      Argument(names=('hostfile'),help="Path to a riaps-hosts.conf file",kind=str)]
        return core_args + extra_args
    
    def update_config(self, merge: bool = True) -> None:
        if self.args.host.got_value:
            if self.args.role.got_value:
                raise Exit(f"ERROR: cannot set both \"role\" and \"host\"")
            if self.args.hostfile.got_value:
                raise Exit(f"ERROR: cannot set both \"hostfile\" and \"host\"")
            self.config._set(hosts=ThreadingGroup(*self.args.host.value))
            self.config._set(role="hostlist")
        else:
            self.config._set(role=self.args.role.value)
            self.config._set(hosts=utils.load_role(self.args.role.value,hostfile=self.args.hostfile.value))
        self.config._set(hide=not self.args.v.value)
        super().update_config(merge)
    
_program = RfabProgram(version='0.0.1',namespace=ns)