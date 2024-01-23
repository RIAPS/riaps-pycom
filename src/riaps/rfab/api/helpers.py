from fabric import Group, GroupResult, Result
from fabric.exceptions import GroupException
from fabric.transfer import Result as TransferResult
from invoke.exceptions import UnexpectedExit

class RFabGroupResult(dict):
    def __init__(self, fabResult: GroupResult, test=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update(fabResult)
        self._succeeded = {}
        self._failed = {}
        self._excepted = {}
        if test is None:
            def test(result: Result):
                return result.return_code == 0
        self._test = test

    def _split(self):
        if self._succeeded or self._failed or self._excepted:
            return
        for key, value in self.items():
            if isinstance(value, UnexpectedExit):
                value = value.result
            if isinstance(value, BaseException):
                self._excepted[key] = value
            elif self._test(value):
                self._succeeded[key] = value
            else:
                self._failed[key] = value

    @property
    def excepted(self):
        self._split()
        return self._excepted
    
    @property
    def failed(self):
        self._split()
        return self._failed
    
    @property
    def succeeded(self):
        self._split()
        return self._succeeded
    
        
    def pretty_print(self, exception_hints: list = []):
        if self.succeeded:
            print(f"Succeeded ({len(self.succeeded)}):")
            for c,r in self.succeeded.items():
                print(f"   {c.host}: {r.stdout.strip()}")
        if self.failed:
            print(f"Failed ({len(self.failed)}):")
            for c,r in self.failed.items():
                print(f"   {c.host}: {r.stdout.strip()}")
        if self.excepted:
            print(f"Excepted ({len(self.excepted)}):")
            for c,r in self.excepted.items():
                for eh in exception_hints:
                    T, hint = eh
                    if isinstance(r,T):
                        r = hint
                        break
                print(f"   {c.host}: {r}")

def _fabricGroupRun(sudo: bool, cmd: str, group: Group, test: callable, **kwargs):
    res = None
    hide = kwargs.pop("hide",False)
    try:
        if sudo:
            res: GroupResult = group.sudo(cmd,hide=hide,**kwargs)
        else:
            res: GroupResult = group.run(cmd,hide=hide,**kwargs)
    except GroupException as e:
        res = e.result
    return RFabGroupResult(res,test=test)

def groupRun(cmd: str, group: Group, test: callable = None, **kwargs):
    return _fabricGroupRun(False,cmd,group,test,**kwargs)

def groupSudo(cmd: str, group: Group, test: callable = None, **kwargs):
    return _fabricGroupRun(True,cmd,group,test,**kwargs)

def groupPut(group: Group, fileName, remote_dir) -> TransferResult:
    res = None
    try:
        res: TransferResult = group.put(fileName, remote_dir)
    except Exception:
        raise
    return res

def groupGet(group: Group, remote_file, local_path = '') -> TransferResult:
    res = None
    if len(group) > 1:
        local_path += "{host}/{basename}"
    if len(local_path) == 0:
        local_path = None
    try:
        res: TransferResult = group.get(remote_file,local=local_path)
    except Exception:
        raise
    return res

def _check_result_success(r):
        if isinstance(r,Result):
            return (r.exited == 0, r)
        return (True,r)

def run_step(step,test=None):
    if test is None:
        test = _check_result_success
    func, kwargs, args = step[0], step[1], step[2:]
    # cmd = f"{func.__name__}({', '.join(map(str,args))})"
    try:
        r = func(*args,**kwargs)
        return test(r)
    except UnexpectedExit as e:
        r = e.result
        return test(r)
    except BaseException as e:
        return (False, e)

def run_multiple_steps(steplist):
    results = []
    for step in steplist:
            func, kwargs, args = step[0], step[1], step[2:]
            cmd = f"{func.__name__}({', '.join(map(str,args))})"
            # print(cmd)
            try:
                ok, res = _check_result_success(func(*args,**kwargs))
                if not ok:
                    results.append((cmd,res))
            except UnexpectedExit as e:
                r = e.result
                ok, res = _check_result_success(r)
                if not ok:
                    results.append(cmd,res)
            except BaseException as e:
                results.append((cmd,e))
                break
    return results

def multi_step_print_errors(resultList) -> bool:
    ok = True
    for cmd,res in resultList:
        if isinstance(res,BaseException):
            print(f"\nEXCEPTION:")
            print(f"\"{cmd}\" returned:\n{res}")
        elif isinstance(res,Result):
            if res.exited != 0:
                print(f"\nERROR FOR {res.connection.host}")
                print(f"{cmd} returned:\n{res}")
        else:
            print(f"ERROR: Unknown result\n{res}")
        ok = False
    return ok
            