import os
from multigen.jinja import JinjaTask, JinjaGenerator
from riaps.gen.target.capnp import capnpfilters

class CapnpTask(JinjaTask):
    template_name = 'capnp.tpl'

    def filtered_elements(self, model):
        model = {'capnp' : model}
        return model.values()

    def relative_path_for_element(self, element):
        output_file = os.path.join('./', f'{element["appname"].lower()}.capnp')
        return output_file

class CapnpGenerator(JinjaGenerator):
    templates_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'tpl'
    )

    tasks = [
        CapnpTask(),
    ]


    def create_environment(self, **kwargs):
        environment = super().create_environment(**kwargs)
        environment.trim_blocks = True
        environment.filters['generateid'] = capnpfilters.generate_capnp_id
        return environment