# riaps:keep_import:begin
import time

from riaps.run.comp import Component
import spdlog
import capnp
# import invertQryAns_capnp

# riaps:keep_import:end

class client(Component):

# riaps:keep_constr:begin
    def __init__(self, name):
        super(client, self).__init__()
        self.name = name
        self.msg_num = 0
        self.connected = False


# riaps:keep_constr:end

# riaps:keep_qry_port:begin
    def on_qry_port(self):
        msg = self.qry_port.recv_pyobj()
        self.logger.info(f"client received answer: {msg}")
        self.connected = True
# riaps:keep_qry_port:end

# riaps:keep_poller:begin
    def on_poller(self):
        now = self.poller.recv_pyobj()
        self.logger.info(f"client poll")

        # make sure qry/ans ports are connected before proceeding
        if self.qry_port.connected() == 0:
            self.logger.info('Not yet connected!')
            return

        if self.connected:
            self.poller.deactivate()
            self.logger.info(f"client connected - Deactivate poller")
            return None

        self.msg_num += 1
        msg = {"name": self.name,
               "status": "ready",
               "msg_num": self.msg_num}
        self.qry_port.send_pyobj(msg)



# riaps:keep_poller:end

# riaps:keep_impl:begin

    def handleActivate(self):
        self.logger.info(f"client handleActivate()")


# riaps:keep_impl:end
