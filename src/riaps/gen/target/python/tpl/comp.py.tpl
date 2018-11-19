{% import 'macros.tpl' as macros -%}

from riaps.run.comp import Component
import logging
{% if use_capnp %}
import capnp
import {{ element.appname|lower }}_capnp
{% endif %}
# <<riaps:keep_import--

# --riaps:keep_import>>


class {{element.name}}(Component):
    def __init__(self{{macros.args(element)}}):
        super({{element.name}}, self).__init__()

{% for port_type, value in element.ports.items() %}
{% if value and port_type in macros.handler_ports %}
{% for port_name, port_params in value.items() %}
# <<riaps:keep_{{port_name|lower}}--
    def on_{{port_name|lower}}(self):
{% if use_capnp and port_type !='tims' %}
        msg = self.{{port_name|lower}}.recv()
{% else %}
        msg = self.{{port_name|lower}}.recv_pyobj()
{% endif %}
# --riaps:keep_{{port_name|lower}}>>

{% endfor %}
{% endif %}
{% endfor %}

# <<riaps:keep_impl--

# --riaps:keep_impl>>
