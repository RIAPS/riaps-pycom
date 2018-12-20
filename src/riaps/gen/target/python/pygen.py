import os
from multigen.jinja import JinjaTask, JinjaGenerator

class CompPyTask(JinjaTask):
    template_name = 'comp.py.tpl'

    def __init__(self, part):
        super(CompPyTask, self).__init__()
        self.part = part

    def filtered_elements(self, model):
        return model['py']

    def relative_path_for_element(self, element):
        return f'{element["name"]}.py'

class CompGenerator(JinjaGenerator):
    def __init__(self):
        self.use_capnp = True
        self.templates_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'tpl'
        )

        self.tasks = [
            CompPyTask('components'),
            CompPyTask('devices')
        ]

        super(CompGenerator, self).__init__()


    def create_environment(self, **kwargs):
        environment = super().create_environment(**kwargs)
        environment.trim_blocks = True
        environment.globals["use_capnp"] = self.use_capnp
        return environment