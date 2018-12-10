import os
from multigen.jinja import JinjaTask, JinjaGenerator
from riaps.gen.target.cpp import ccfilters



class CompHppBaseTask(JinjaTask):
    template_name = 'comp.base.h.tpl'

    def filtered_elements(self, model):
        return model['cpp']

    def relative_path_for_element(self, element):
        output_file = os.path.join("include/base/", f'{element["name"]}Base.h')
        return output_file

class CompCppBaseTask(JinjaTask):
    template_name = 'comp.base.cc.tpl'

    def filtered_elements(self, model):
        return model['cpp']

    def relative_path_for_element(self, element):
        output_file = os.path.join("src/base/", f'{element["name"]}Base.cc')
        return output_file

class CompHppTask(JinjaTask):
    template_name = 'comp.h.tpl'

    def filtered_elements(self, model):
        return model['cpp']

    def relative_path_for_element(self, element):
        output_file = os.path.join("include", f'{element["name"]}.h')
        return output_file

class CompCppTask(JinjaTask):
    template_name = 'comp.cc.tpl'

    def filtered_elements(self, model):
        return model['cpp']

    def relative_path_for_element(self, element):
        output_file = os.path.join("src", f'{element["name"]}.cc')
        return output_file

class CmakeTask(JinjaTask):
    template_name = 'cmake.tpl'

    def filtered_elements(self, model):
        model = {'cmake' : model['cpp']}
        return model.values()
        #return model['cpp'].values()

    def relative_path_for_element(self, element):
        output_file = os.path.join('CMakeLists.txt')
        return output_file

class CompGenerator(JinjaGenerator):
    templates_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'tpl'
    )

    tasks = [
        CompHppBaseTask(),
        CompCppBaseTask(),
        CompHppTask(),
        CompCppTask(),
        CmakeTask(),
    ]


    def create_environment(self, **kwargs):
        environment = super().create_environment(**kwargs)
        environment.trim_blocks = True
        environment.filters['handlername'       ] = ccfilters.handler_name
        environment.filters['sendername'        ] = ccfilters.sender_name
        environment.filters['recvreturntype'    ] = ccfilters.recv_return_type
        environment.filters['portmacro'         ] = ccfilters.port_macro
        environment.filters['recvmessagetype'   ] = ccfilters.recv_message_type
        environment.filters['sendermessagetype' ] = ccfilters.sender_message_type
        environment.filters['cppporttype'       ] = ccfilters.cpp_port_type
        return environment