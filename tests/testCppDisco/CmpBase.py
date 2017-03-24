import uuid

class CmpBase:
    def __init__(self):
        super(CmpBase, self).__init__()
        self.componentId = str(uuid.uuid1())
        self.others = set()
        self.publisherPorts = []

    def on_update_base(self, updateMsg):
        self.others.add(updateMsg['me'])
        for othername in updateMsg['others']:
            self.others.add(othername)

    def introduce(self):
        # introduces itself
        msg = {'me': self.componentId, 'others': []}

        # introduce others
        for othername in self.others:
            msg['others'].append(othername)

        for pubPortName in self.publisherPorts:
            if (hasattr(self, pubPortName)):
                port = getattr(self, pubPortName)
                port.send_pyobj(msg)