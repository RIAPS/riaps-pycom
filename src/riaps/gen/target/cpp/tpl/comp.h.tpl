{% extends "comp.common.tpl" -%}

{% block macros -%}
#ifndef {{element.name|upper}}_H
#define {{element.name|upper}}_H
{%- endblock macros %}

{% block includes %}
#include <base/{{baseclassname}}.h>
// <<riaps:keep_header--

// --riaps:keep_header>>
{% endblock includes %}

{% block component %}
        class {{classname}} : public {{baseclassname}} {
        public:
            {{classname}}(const py::object*  parent_actor     ,
                          const py::dict     actor_spec       ,
                          const py::dict     type_spec        ,
                          const std::string& name             ,
                          const std::string& type_name        ,
                          const py::dict     args             ,
                          const std::string& application_name ,
                          const std::string& actor_name       );


{% for port_type, value in element.ports.items() %}
{% if value %}
{% if port_type in macros.handler_ports %}
{% for port_name, port_params in value.items() %}
            virtual void {{ port_name|handlername }}() override;
{% endfor %}
{% endif %}
{% endif %}
{% endfor %}

            virtual ~{{classname}}();

            // <<riaps:keep_decl--

            // --riaps:keep_decl>>
        };
{% endblock component %}

{% block pybind %}
std::unique_ptr<{{classname_full}}>
create_component_py(const py::object *parent_actor,
                    const py::dict actor_spec,
                    const py::dict type_spec,
                    const std::string &name,
                    const std::string &type_name,
                    const py::dict args,
                    const std::string &application_name,
const std::string &actor_name);
{% endblock pybind %}

{% block endmacros %}
#endif // {{element.name|upper}}_H
{% endblock endmacros %}
