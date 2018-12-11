import os
import re

class FileSync:
    def __init__(self, model):
        self.capnp_rules = []
        self.model = model

    def sync_capnp(self, output_dir):
        old_path = os.path.join(os.path.dirname(__file__), f'{output_dir}_bak/{self.model["appname"].lower()}.capnp')
        new_path = os.path.join(os.path.dirname(__file__), f'{output_dir}/{self.model["appname"].lower()}.capnp')

        for message in self.model['messages']:
            capnp_regex = r"(?:# riaps:keep_{}:begin)(.+)(?:# riaps:keep_{}:end)".format(message.lower(), message.lower())
            self.capnp_rules.append(capnp_regex)
        self.apply_capnp_rules(old_path, new_path)

    def apply_capnp_rules(self, orig_filepath, new_filepath):
        if not os.path.exists(orig_filepath) or not os.path.exists(new_filepath):
            return

        rules = self.capnp_rules

        orig_content = open(orig_filepath, "r+").read()

        with open(new_filepath, "r+") as f:
            new_content = f.read()
            for rule in rules:
                orig_match = re.search(rule, orig_content, re.DOTALL)
                new_match = re.search(rule, new_content, re.DOTALL)
                if orig_match == None or new_match == None:
                    continue
                orig_snipet = orig_match.group(1)
                startIdx = new_match.start(1)
                endIdx = new_match.end(1)
                new_content = f"{new_content[0:startIdx]}{orig_snipet}{new_content[endIdx:new_content.__len__()]}"
            f.seek(0)
            f.truncate(0)
            f.write(new_content)