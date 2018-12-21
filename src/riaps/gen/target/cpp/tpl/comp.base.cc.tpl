{% extends "comp.base.skaleton.cc.tpl" -%}

{% block recvfuncs %}
{% for port_type, value in element.ports.items() %}
{% if value and  port_type in macros.recv_ports %}
{% for port_name, port_params in value.items() %}
{% if port_type == 'tims' %}
        timespec {{baseclassname}}::Recv{{port_name|capitalize}}() {
            auto port = GetPortAs<riaps::ports::{{port_type|cppporttype}}>({{port_name|portmacro(port_type)}});
            return port->Recv();
        }
{% else %}
        tuple<MessageReader<messages::{{port_params|recvmessagetype(port_type)}}>, PortError> {{baseclassname}}::Recv{{port_name|capitalize}}() {
            auto port = GetPortAs<riaps::ports::{{port_type|cppporttype}}>({{port_name|portmacro(port_type)}});
            auto [msg_bytes, error] = port->Recv();
            MessageReader<messages::{{port_params|recvmessagetype(port_type)}}> reader(msg_bytes);
            return make_tuple(reader, error);
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
        riaps::ports::PortError {{baseclassname}}::{{ port_name|sendername }}(MessageBuilder<messages::{{port_params|sendermessagetype(port_type)}}>& message) {
            return SendMessageOnPort(message.capnp_builder(), {{ port_name|portmacro(port_type) }});
        }

{% endfor %}
{% endif %}
{% endfor %}
{% endblock %}


