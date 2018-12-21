{% set regular_ports = ['clts', 'anss', 'inss', 'pubs', 'qrys', 'reps', 'reqs', 'srvs', 'subs'] %}
{% set handler_ports = ['clts', 'anss', 'qrys', 'reps', 'reqs', 'srvs', 'subs', 'tims'] %}
{% set sender_ports = ['clts', 'anss', 'pubs', 'qrys', 'reps', 'reqs', 'srvs'] %}
{% set recv_ports = ['clts', 'anss', 'qrys', 'reps', 'reqs', 'srvs', 'subs', 'tims'] %}

{% set timer_port    = 'tims' %}
{% set fn_names  = namespace()  %}
{% set fn_params = namespace()  %}

{% macro portdefine(ports) -%}
{% for key, value in ports.items() %}
{% if value %}
{% if key in regular_ports %}
{% set port_type = key|upper|truncate(3, True, '', 0) %}
constexpr auto PORT_{{port_type}}_{{ value|first|upper }} = "{{value|first}}";
{% elif key == timer_port %}
constexpr auto PORT_TIMER_{{ value|first|upper }} = "{{value|first}}";
{% endif %}
{% endif %}
{% endfor %}
{%- endmacro %}

{% macro ontimers(ports) -%}
{% for key, value in ports['tims'].items() %}
{% if value %}
{% set fn_names.key = ['On', key|capitalize]|join %}
{% set fn_params.key = 'riaps::ports::PortBase* port' %}
virtual void {{fn_names.key}}({{fn_params.key}})=0;
{% endif %}
{% endfor %}
{%- endmacro %}

{% macro onportmessage(ports) -%}
{% for port_type_key, value in ports.items() %}
{% if value %}
{% if port_type_key in regular_ports %}
{% for port_key, port_params in value.items() %}
virtual void On{{port_key|capitalize}}(messages::{{port_params.type}}::Reader& message,
                                       riaps::ports::PortBase* port)=0;
{% endfor %}
{% endif %}
{% endif %}
{% endfor %}
{%- endmacro %}


