{% extends "comp.base.skaleton.h.tpl" %}
{% import 'macros.tpl' as macros %}

{% block onhandlers %}
{% for port_type, value in element.ports.items() %}
{% if value and  port_type in macros.handler_ports %}
{% for port_name, port_params in value.items() %}
            virtual void {{ port_name|handlername }}()=0;
{% endfor %}
{% endif %}
{% endfor %}
{% endblock %}

{% block recvfuncs %}
{% for port_type, value in element.ports.items() %}
{% if value and  port_type in macros.recv_ports %}
{% for port_name, port_params in value.items() %}
{% if port_type == 'tims' %}
            virtual timespec Recv{{port_name|capitalize}}() final;
{% else %}

            virtual std::tuple<MessageReader<messages::{{port_params|recvmessagetype(port_type)}}>, riaps::ports::PortError> Recv{{port_name|capitalize}}() final;
{% endif %}
{% endfor %}
{% endif %}
{% endfor %}
{% endblock %}

{% block sendfuncs %}
{% for port_type, value in element.ports.items() %}
{% if value and  port_type in macros.sender_ports %}
{% for port_name, port_params in value.items() %}
            virtual riaps::ports::PortError Send{{port_name|capitalize}}(MessageBuilder<messages::{{port_params|sendermessagetype(port_type)}}>& message) final;
{% endfor %}
{% endif %}
{% endfor %}
{%endblock %}
