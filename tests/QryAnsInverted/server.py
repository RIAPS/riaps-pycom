# riaps:keep_import:begin
from riaps.run.comp import Component
import spdlog
import capnp
# import invertQryAns_capnp


# riaps:keep_import:end

class server(Component):

# riaps:keep_constr:begin
    def __init__(self):
        super(server, self).__init__()
        self.peer_list = {}
        self.msg_num = 0
        self.logger.info(f"Controller ready")
# riaps:keep_constr:end

# riaps:keep_ans_port:begin
    def on_ans_port(self):
        msg = self.ans_port.recv_pyobj()
        self.logger.info(f"server received message: {msg} "
                         f"from: {self.ans_port.identity}")

        self.peer_list[msg["name"]] = self.ans_port.identity

        self.logger.info(str(self.peer_list))


        reply = {"ack": msg['msg_num']}
        self.ans_port.send_pyobj(reply)
        reply = {"ack": msg['msg_num'] + 1}
        self.ans_port.send_pyobj(reply)

        self.poller.activate()
# riaps:keep_ans_port:end

# riaps:keep_poller:begin
    def on_poller(self):
        now = self.poller.recv_pyobj()

        self.msg_num += 1
        msg = {"command": self.msg_num}

        for peer in self.peer_list:
            self.ans_port.identity = self.peer_list[peer]
            self.ans_port.send_pyobj(msg)

        # self.logger.info(f"server poll")
# riaps:keep_poller:end

# riaps:keep_impl:begin

    def handleActivate(self):
        self.logger.info(f"server handleActivate()")
        self.poller.deactivate()

# riaps:keep_impl:end