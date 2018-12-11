import os
import re
from riaps.gen.target.cpp import ccfilters

class FileSync:

    def __init__(self, model):
        self.h_rules     = []
        self.cpp_rules   = []
        self.cmake_rules = []
        self.model     = model

    def sync_all(self, output_dir):
        self.sync_code(output_dir)
        self.sync_cmake(output_dir)

    def sync_cmake(self, output_dir):
        old_path = os.path.join(os.path.dirname(__file__), f'{output_dir}_bak/CMakeLists.txt')
        new_path = os.path.join(os.path.dirname(__file__), f'{output_dir}/CMakeLists.txt')
        cmake_markers = ['keep_cmake']

        base_cmake_rules = []
        for cmake_marker in cmake_markers:
            new_rule = rf"(?:# riaps:{cmake_marker}:begin)(.+)(?:# riaps:{cmake_marker}:end)"
            base_cmake_rules.append(new_rule)

        self.cmake_rules = base_cmake_rules.copy()
        for component in self.model:
            cmake_regex = r"(?:# riaps:keep_{}:begin)(.+)(?:# riaps:keep_{}:end)".format(component["name"].lower(), component["name"].lower())
            self.cmake_rules.append(cmake_regex)
        self.apply_cmake_rules(old_path, new_path)

    def sync_code(self, output_dir):
        h_markers     = ['keep_header', 'keep_decl']
        cpp_markers   = ['keep_header', 'keep_decl', 'keep_impl', 'keep_construct', 'keep_destruct']

        for h_marker in h_markers:
            new_rule = rf"(?:// riaps:{h_marker}:begin)(.+)(?:// riaps:{h_marker}:end)"
            self.h_rules.append(new_rule)

        base_cpp_rules = []
        for cpp_marker in cpp_markers:
            new_rule = rf"(?:// riaps:{cpp_marker}:begin)(.+)(?:// riaps:{cpp_marker}:end)"
            base_cpp_rules.append(new_rule)

        items = {}

        for component in self.model:
            self.cpp_rules = base_cpp_rules.copy()
            for port_type, port_params in component['ports'].items():
                for port_name in port_params.keys():
                    handlerregex = r"(?:// riaps:keep_{}:begin)(.+)(?:// riaps:keep_{}:end)".format(
                    ccfilters.handler_name(port_name).lower(), ccfilters.handler_name(port_name).lower())
                    self.cpp_rules.append(handlerregex)

            old_path = os.path.join(os.path.dirname(__file__), f'{output_dir}_bak/include/{component["name"]}.h')
            new_path = os.path.join(os.path.dirname(__file__), f'{output_dir}/include/{component["name"]}.h')
            self.apply_cpp_rules(old_path, new_path)

            old_path = os.path.join(os.path.dirname(__file__), f'{output_dir}_bak/src/{component["name"]}.cc')
            new_path = os.path.join(os.path.dirname(__file__), f'{output_dir}/src/{component["name"]}.cc')
            self.apply_cpp_rules(old_path, new_path)

    def apply_cmake_rules(self, orig_filepath, new_filepath):
        if not os.path.exists(orig_filepath) or not os.path.exists(new_filepath):
            return

        rules = self.cmake_rules

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


    def apply_cpp_rules(self, orig_filepath, new_filepath):
        if not os.path.exists(orig_filepath) or not os.path.exists(new_filepath):
            return

        rules = []
        _, file_extension = os.path.splitext(orig_filepath)
        if file_extension == '.cc':
            rules = self.cpp_rules
        elif file_extension == '.h':
            rules = self.h_rules
        else:
            raise FutureWarning

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


