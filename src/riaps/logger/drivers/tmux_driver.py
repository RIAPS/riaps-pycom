#
# tmux log driver
#
import logging
import sys
import os

import libtmux
from riaps.logger.drivers.base_driver import BaseDriver
import logging


class ServerLogDriver(BaseDriver):

    def __init__(self, driver_type, session_name):
        super().__init__(driver_type)      
        self.nodes = {}
        self.session_name = session_name
        self.server = libtmux.Server()
        session = self.get_session()
        self.window = session.attached_window
        self.pane = self.window.panes[0]
        self.set_pane(self.pane, node_name="host")
        self.write_display(node_name="host", msg="riaps_logger: start session'")

    def handle(self, msg):
        node_name = msg["client"]
        if node_name not in self.nodes:
            self.logger.info(f"driver: add new node: {node_name}")
            self.add_node_display(node_name=node_name)
        self.write_display(node_name=node_name, msg=msg["data"])

    def set_pane(self, pane, node_name=None):
        pane_id = pane.get("pane_id")
        pane_name = node_name if node_name else f"pane_{pane_id}"
        _tty = pane.get("pane_tty")
        pane_tty = os.open(_tty, os.O_NOCTTY | os.O_WRONLY)
        self.nodes[pane_name] = { "tty" : pane_tty, "pane" : pane }
        pane.cmd("select-pane", '-t', f"{pane_id}", "-T", f"{pane_name}")

    def add_node_display(self, node_name):
        try:
            pane = self.window.split_window(attach=False,
                                            vertical=False)
            self.set_pane(pane, node_name=node_name)
            pane.window.select_layout(layout="tiled")
            return
        except libtmux.exc.LibTmuxException as e:
            self.logger.error(e)

    def write_display(self, node_name, msg):
        try:
            pane_tty = self.nodes[node_name]["tty"]
            _msg = ("[%s.%s]%s\n" % (node_name, self.session_name, msg)).encode('UTF-8')
            os.write(pane_tty, _msg)
        except Exception as e:
            self.logger.error(f"driver: tmux session closed")
            os._exit(0)

    def start_session(self):
        self.server.new_session(session_name=self.session_name, attach=False, window_name="main")
        self.server.cmd("set", "-g", "pane-border-status", "top")

    def get_session(self):
        if not self.server.has_session(target_session=self.session_name):
            self.start_session()
        session = self.server.find_where({"session_name": self.session_name})
        return session

    def close(self):
        self.logger.info("driver: close_session")
        self.server.kill_session(self.session_name)
