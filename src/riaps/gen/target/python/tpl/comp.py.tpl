{% import 'macros.tpl' as macros -%}

# riaps:keep_import:begin
from riaps.run.comp import Component
import logging
import spdlog
{% if use_capnp %}
import capnp
import {{ element.appname|lower }}_capnp
{% endif %}

# riaps:keep_import:end

class {{element.name}}(Component):

# riaps:keep_constr:begin
    def __init__(self{{macros.args(element)}}):
        super({{element.name}}, self).__init__()
# riaps:keep_constr:end

{% for port_type, value in element.ports.items() %}
{% if value and port_type in macros.handler_ports %}
{% for port_name, port_params in value.items() %}
# riaps:keep_{{port_name|lower}}:begin
    def on_{{port_name}}(self):
        pass
# riaps:keep_{{port_name|lower}}:end

{% endfor %}
{% endif %}
{% endfor -%}

# riaps:keep_impl:begin

# riaps:keep_impl:end
