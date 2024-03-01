from riaps.rfab.api.riaps import ResetTask
from fabric import Connection
c = ResetTask([Connection("1.2.3.4"),Connection("5.6.7.8")])
c.run()