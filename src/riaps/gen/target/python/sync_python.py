import os
import re

class FileSync:

    def __init__(self, model):
        self.py_rules     = []
        self.model     = model

    def sync_code(self, output_dir):
        py_markers     = ['keep_import', 'keep_impl', 'keep_constr']
        base_py_rules = []

        for py_marker in py_markers:
            new_rule = rf"(?:# riaps:{py_marker}:begin)(.+)(?:# riaps:{py_marker}:end)"
            base_py_rules.append(new_rule)

        for component in self.model:
            self.py_rules = base_py_rules.copy()
            for port_type, port_params in component['ports'].items():
                for port_name in port_params.keys():
                    handlerregex = r"(?:# riaps:keep_{}:begin)(.+)(?:# riaps:keep_{}:end)".format(port_name.lower(), port_name.lower())
                    self.py_rules.append(handlerregex)

            old_path = os.path.join(os.path.dirname(__file__), f'{output_dir}_bak/{component["name"]}.py')
            new_path = os.path.join(os.path.dirname(__file__), f'{output_dir}/{component["name"]}.py')
            self.apply_py_rules(old_path, new_path)

    def apply_py_rules(self, orig_filepath, new_filepath):
        if not os.path.exists(orig_filepath) or not os.path.exists(new_filepath):
            return

        rules = self.py_rules
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