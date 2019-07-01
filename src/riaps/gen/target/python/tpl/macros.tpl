{% set handler_ports = ['clts', 'anss', 'qrys', 'reps', 'reqs', 'srvs', 'subs', 'tims', 'inss'] %}
{% set sender_ports = ['clts', 'anss', 'pubs', 'qrys', 'reps', 'reqs', 'srvs'] %}

{% macro args(component) -%}
{% for key in component.formals %}
, {{key.name -}}
{% endfor %}
{%- endmacro %}