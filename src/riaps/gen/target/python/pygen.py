import os
from multigen.jinja import JinjaTask, JinjaGenerator

class CompPyTask(JinjaTask):
    template_name = 'comp.py.tpl'

    def __init__(self, part):
        super(CompPyTask, self).__init__()
        self.part = part

    def filtered_elements(self, model):
        components = model[self.part].values()
        for item in components:
            item.update({"appname": model['name']})
        return components

    def relative_path_for_element(self, element):
        return f'{element["name"]}.py'

class CapnpTask(JinjaTask):
    template_name = 'message.capnp.tpl'

    def filtered_elements(self, model):
        model = {'capnp' : model}
        return model.values()

    def relative_path_for_element(self, element):
        return f'{element["name"].lower()}.capnp'

class CompGenerator(JinjaGenerator):

    # Root path where Jinja templates are found.


    def __init__(self, use_capnp):
        self.use_capnp = use_capnp
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