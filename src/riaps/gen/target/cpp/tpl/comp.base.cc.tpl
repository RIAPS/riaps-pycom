{% extends "comp.base.skaleton.cc.tpl" %}

{% block recvfuncs %}
{% for port_type, value in element.ports.items() %}
{% if value and  port_type in macros.recv_ports %}
{% for port_name, port_params in value.items() %}
{% if port_type == 'tims' %}
        virtual string Recv{{port_name|capitalize}}() {
            auto port = GetPortAs<riaps::ports::{{port_type|cppporttype}}>({{port_name|portmacro(port_type)}});
            return port->Recv();
        }
{% else %}
        virtual messages::{{port_params|recvmessagetype(port_type)}}::Reader Recv{{port_name|capitalize}}() {
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
        bool {{baseclassname}}::{{ port_name|sendername }}(capnp::MallocMessageBuilder& messageBuilder, messages::{{port_params|sendermessagetype(port_type)}}::Builder& message) {
            return SendMessageOnPort(messageBuilder, {{ port_name|portmacro(port_type) }});
        }

{% endfor %}
{% endif %}
{% endfor %}
{% endblock %}


