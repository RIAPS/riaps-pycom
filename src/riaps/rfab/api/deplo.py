from fabric import Group
from riaps.rfab.api.task import Task
from invoke.exceptions import UnexpectedExit

class DeploStart(Task):
    def deplo_start(self):
        return self.sudo('systemctl start riaps-deplo.service')

class DeploStartManual(Task):
    def deplo_start_manual(self):
        return self.sudo('riaps_deplo >~/riaps-$(hostname).log 2>&1 &',pty=True)

class DeploRestart(Task):
    def deplo_restart(self):
        return self.sudo('systemctl restart riaps-deplo.service')

class DeploStop(Task):
    def deplo_stop(self):
        return self.sudo('systemctl stop riaps-deplo.service')
    
class DeploEnable(Task):
    def deplo_enable(self):
        return self.sudo('systemctl enable riaps-deplo.service')

class DeploDisable(Task):
    def deplo_disable(self):
        return self.sudo('systemctl disable riaps-deplo.service')

class DeploStatus(Task):
    num_lines = " -n 10"
    grep_pattern = ''

    @classmethod
    def configure(cls,n,grep):
        cls.num_lines = f" -n {n}"
        if grep != '':
            grep=f" | grep {grep}"
        cls.grep_pattern = grep

    def deplo_status(self):
        try:
            return self.sudo(f"systemctl status riaps-deplo --no-pager{self.num_lines}{self.grep_pattern}")
        except UnexpectedExit as e:
            if str(e.result.exited) in ('1','2','3'): # Don't "Fail" for certain return codes
                return e.result
            else:
                raise e


class DeploJournal(Task):
    num_lines = " -n 10"
    grep_pattern = ''

    @classmethod
    def configure(cls,n,grep):
        cls.num_lines = f" -n {n}"
        if grep != '':
            grep=f" | grep {grep}"
        cls.grep_pattern = grep

    def deplo_journal(self):
        return self.sudo(f"journalctl -u riaps-deplo.service --no-pager{self.num_lines}{self.grep_pattern}")
