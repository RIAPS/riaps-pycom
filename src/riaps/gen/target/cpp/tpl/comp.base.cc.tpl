{% extends "comp.base.skaleton.cc.tpl" -%}

{% block recvfuncs %}
{% for port_type, value in element.ports.items() %}
{% if value and  port_type in macros.recv_ports %}
{% for port_name, port_params in value.items() %}
{% if port_type == 'tims' %}
        string {{baseclassname}}::Recv{{port_name|capitalize}}() {
            auto port = GetPortAs<riaps::ports::{{port_type|cppporttype}}>({{port_name|portmacro(port_type)}});
            return port->Recv();
        }
{% else %}
        messages::{{port_params|recvmessagetype(port_type)}}::Reader {{baseclassname}}::Recv{{port_name|capitalize}}() {
            auto port = GetPortAs<riaps::ports::{{port_type|cppporttype}}>({{port_name|portmacro(port_type)}});
            auto reader = port->Recv();
            return reader->getRoot<messages::{{port_params|recvmessagetype(port_type)}}>();
        }

{% endif %}
{% endfor %}
{% endif %}
{% endfor %}
{% endblock %}

{% block sendfuncs %}
{% for port_type, value in element.ports.items() %}
{% if value and port_type in macros.sender_ports%}
{% for port_name, port_params in value.items() %}
        bool {{baseclassname}}::{{ port_name|sendername }}(MessageBuilder<messages::{{port_params|sendermessagetype(port_type)}}>& message) {
            return SendMessageOnPort(message.capnp_builder(), {{ port_name|portmacro(port_type) }});
        }

{% endfor %}
{% endif %}
{% endfor %}
{% endblock %}


