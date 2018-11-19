{% extends "comp.common.tpl" %}

{% block macros %}
#ifndef {{element.name|upper}}BASE_H
#define {{element.name|upper}}BASE_H
{% endblock macros %}

{% block includes %}
#include <pybind11/stl.h>
#include <pybind11/pybind11.h>
#include <componentmodel/r_componentbase.h>
#include <messages/{{element.appname|lower}}.capnp.h>

namespace py = pybind11;
{% endblock includes %}

{% block portdefinitions %}
{{ macros.portdefine(element.ports) }}
{% endblock portdefinitions %}

{% block component %}
        class {{baseclassname}} : public riaps::ComponentBase {
        public:
            {{baseclassname}}(const py::object*  parent_actor     ,
                          const py::dict     actor_spec       ,
                          const py::dict     type_spec        ,
                          const std::string& name             ,
                          const std::string& type_name        ,
                          const py::dict     args             ,
                          const std::string& application_name ,
                          const std::string& actor_name       );

{% block onhandlers %} {% endblock %}

{% block recvfuncs %} {% endblock %}

{% block sendfuncs %} {% endblock %}

            virtual ~{{baseclassname}}() = default;
        protected:
            virtual void DispatchMessage(riaps::ports::PortBase* port) final;

            virtual void DispatchInsideMessage(zmsg_t* zmsg, riaps::ports::PortBase* port) final;
        };
{% endblock component %}

{% block endmacros %}
#endif // {{element.name|upper}}BASE_H
{% endblock endmacros %}