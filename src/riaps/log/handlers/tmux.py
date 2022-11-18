import logging
import sys

import libtmux
import libtmux.exc
import subprocess
# from riaps.log.visualizers.base_view import BaseView
from riaps.log.handlers.base_handler import BaseHandler
import logging


class ServerLogHandler(BaseHandler):

    def __init__(self, handler_type, session_name):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        super().__init__(handler_type)
        self.session_name = session_name
        self.server = libtmux.Server()
        session = self.get_session()
        self.window = session.attached_window
        self.pane = self.window.panes[0]
        self.set_pane(self.pane, node_name="host")
        self.write_display(node_name="host", msg="echo 'Start session'")

    def handle(self, msg):
        node_name = msg["node_name"]
        if node_name not in self.nodes:
            self.logger.info(f"Add new node: {node_name}")
            self.add_node_display(node_name=node_name)
        self.write_display(node_name=node_name, msg=msg["data"])

    def set_pane(self, pane, node_name=None):
        pane_id = pane.get("pane_id")
        pane_tty = pane.get("pane_tty")
        pane_name = node_name if node_name else f"pane_{pane_id}"
        self.nodes[pane_name] = {"tty": pane_tty,
                                 "obj": pane}
        subprocess.run(["tmux", "select-pane", "-t", f"{pane_id}", "-T", f"{pane_name}"])

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
        pane_tty = self.nodes[node_name]["tty"]
        try:
            output = subprocess.check_output(f"echo '{msg}' > {pane_tty}", shell=True)
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Was the Tmux session closed?")
            sys.exit(1)

    def start_session(self):
        subprocess.run(["tmux", "new-session", "-d", "-s", f"{self.session_name}", "-n", "main"])
        subprocess.run(["tmux", "set", "-g", "pane-border-status", "top"])
        # libtmux.server.Server.new_session()

    def get_session(self):
        if not self.server.has_session(target_session=self.session_name):
            self.start_session()

        sessions = self.server.list_sessions()
        session = self.server.find_where({"session_name": self.session_name})
        return session

    def close(self):
        self.logger.info("close_session")
        self.server.kill_session(self.session_name)
        # subprocess.run(["tmux", "kill-server"])
