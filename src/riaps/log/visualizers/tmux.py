import libtmux
import subprocess
from riaps.log.visualizers.base_view import BaseView


class View(BaseView):

    def __init__(self, session_name):
        super(View, self).__init__(session_name)
        self.server = libtmux.Server()
        session = self.get_session()
        self.window = session.attached_window
        self.pane = self.window.panes[0]
        self.set_pane(self.pane, node_name="host")
        self.write_display(node_name="host", msg="echo 'Start session'")

    def set_pane(self, pane, node_name=None):
        pane_id = pane.get("pane_id")
        pane_tty = pane.get("pane_tty")
        pane_name = node_name if node_name else f"pane_{pane_id}"
        self.nodes[pane_name] = {"tty": pane_tty,
                                 "obj": pane}
        subprocess.run(["tmux", "select-pane", "-t", f"{pane_id}", "-T", f"{pane_name}"])

    def add_node_display(self, node_name):
        pane = self.window.split_window(attach=False,
                                        vertical=False)
        self.set_pane(pane, node_name=node_name)
        pane.window.select_layout(layout="tiled")
        return pane

    def write_display(self, node_name, msg):
        pane_tty = self.nodes[node_name]["tty"]
        subprocess.check_output(f"echo '{msg}' > {pane_tty}", shell=True)

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

    def close_session(self):
        subprocess.run(["tmux", "kill-server"])
