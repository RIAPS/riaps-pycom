from pytest import raises
import riaps.rfab
r = riaps.rfab.api.riaps
from unittest.mock import Mock
from riaps.rfab.api.task import SkipResult



def test_resettask(connection, monkeypatch):
    
    def mockrun(c,**kwargs):
        return SkipResult(c,"command","test message")
    
    def t(c,**kwargs):
        print("IN MOCKTESTED FUNCION\n1\n1\n1\n1")
        return SkipResult(c,"command","test message")

    
    monkeypatch.setattr(connection,"run",mockrun)
    monkeypatch.setattr(connection,"sudo",mockrun)
    # connection.sudo.return_value = SkipResult(connection,"command","test message")
    task = r.ResetTask([connection])

    monkeypatch.setattr(task,"start_deplo",t)
    task.run()