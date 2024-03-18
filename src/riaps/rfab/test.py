import riaps.rfab.api
from fabric import Connection
c = riaps.rfab.api.riaps.ResetTask([Connection("riaps-bcf6.local")])
c.run()
c.pretty_print()