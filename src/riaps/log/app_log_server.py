import socketserver
import visualizers.tmux as visualizer


class MyTCPHandler(socketserver.StreamRequestHandler):
    """
    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def setup(self) -> None:
        global viewer
        super(MyTCPHandler, self).setup()

    def handle(self):
        while True:
            data_bytes = self.rfile.readline().strip()
            if not data_bytes:
                break
            data_string = data_bytes.decode("utf-8")
            data = f"{data_string}: client_address: {self.client_address}"
            node_name = self.client_address[0]
            if self.client_address[0] not in viewer.nodes:
                print(f"client address: {self.client_address[0]}")
                viewer.add_node_display(node_name=node_name)
            viewer.write_display(node_name=node_name, msg=data)


if __name__ == "__main__":
    # HOST, PORT = "192.168.137.139", 12345
    HOST, PORT = "172.21.20.70", 12345
    # HOST, PORT = "localhost", 12345

    viewer = visualizer.View(session_name="componentLogger")

    with socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
