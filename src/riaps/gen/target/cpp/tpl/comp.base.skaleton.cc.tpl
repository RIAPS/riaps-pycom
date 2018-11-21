
{% extends "comp.common.tpl" %}
{% block includes %}
#include <componentmodel/r_pyconfigconverter.h>
#include <base/{{baseclassname}}.h>


using namespace std;
{% endblock %}

{% block component %}
        {{baseclassname}}::{{baseclassname}}(const py::object*  parent_actor     ,
                          const py::dict     actor_spec       ,
                          const py::dict     type_spec        ,
                          const std::string& name             ,
                          const std::string& type_name        ,
                          const py::dict     args             ,
                          const std::string& application_name ,
                          const std::string& actor_name       ) : ComponentBase(application_name, actor_name){
            auto conf = PyConfigConverter::convert(type_spec, actor_spec);
            conf.component_name = name;
            conf.component_type = type_name;
            conf.is_device=false;
            set_config(conf);
        }

{% block recvfuncs %} {% endblock %}

{% block sendfuncs %} {% endblock %}

        void {{baseclassname}}::DispatchMessage(riaps::ports::PortBase* port) {
            auto port_name = port->port_name();
{% for port_type, value in element.ports.items() %}
{% if value %}
{% if port_type in macros.handler_ports %}
{% for port_name, port_params in value.items() %}
{% if port_type == 'tims' %}
            if (port_name == {{ port_name|portmacro(port_type) }}) {
                {{ port_name|handlername }}();
            }
{% else %}
            if (port_name == {{ port_name|portmacro(port_type) }}) {
                {{ port_name|handlername }}();
            }
{% endif %}
{% endfor %}
{% endif %}
{% endif %}
{% endfor %}
        }

        void {{baseclassname}}::DispatchInsideMessage(zmsg_t *zmsg, riaps::ports::PortBase *port) { }
{% endblock %}