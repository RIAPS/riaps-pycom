{% extends "comp.common.tpl" %}

{% block includes %}
#include <{{classname}}.h>
// riaps:keep_header:begin

// riaps:keep_header:end
{% endblock includes %}

{% block component %}

        // riaps:keep_construct:begin
        {{classname}}::{{classname}}(const py::object*  parent_actor     ,
                      const py::dict     actor_spec       ,
                      const py::dict     type_spec        ,
                      const std::string& name             ,
                      const std::string& type_name        ,
                      const py::dict     args             ,
                      const std::string& application_name ,
                      const std::string& actor_name       ,
                      const py::list     groups)
            : {{baseclassname}}(parent_actor, actor_spec, type_spec, name, type_name, args, application_name, actor_name, groups) {

        }
        // riaps:keep_construct:end

{% for port_type, value in element.ports.items() %}
{% if value %}
{% if port_type in macros.handler_ports %}
{% for port_name, port_params in value.items() %}
        void {{classname}}::{{ port_name|handlername }}() {
            // riaps:keep_{{port_name|handlername|lower}}:begin
{% if port_type == 'tims' %}
            auto msg = Recv{{port_name|capitalize}}();
{% else %}
            auto [msg, err] = Recv{{port_name|capitalize}}();
{% endif %}
            // riaps:keep_{{port_name|handlername|lower}}:end
        }

{% endfor %}
{% endif %}
{% endif %}
{% endfor %}
        // riaps:keep_impl:begin

        // riaps:keep_impl:end

        // riaps:keep_destruct:begin
        {{classname}}::~{{classname}}() {

        }
        // riaps:keep_destruct:end

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
                    const std::string &actor_name,
                    const py::list     groups) {
    auto ptr = new {{classname_full}}(parent_actor, actor_spec, type_spec, name, type_name, args,
                                                                     application_name,
                                                                     actor_name, groups);
    return std::move(std::unique_ptr<{{classname_full}}>(ptr));
}

PYBIND11_MODULE(lib{{classname|lower}}, m) {
    py::class_<{{classname_full}}> testClass(m, "{{classname}}");
    testClass.def(py::init<const py::object*, const py::dict, const py::dict, const std::string&, const std::string&, const py::dict, const std::string&, const std::string&, const py::list>());

    testClass.def("setup"                 , &{{classname_full}}::Setup);
    testClass.def("activate"              , &{{classname_full}}::Activate);
    testClass.def("terminate"             , &{{classname_full}}::Terminate);
    testClass.def("handlePortUpdate"      , &{{classname_full}}::HandlePortUpdate);
    testClass.def("handleCPULimit"        , &{{classname_full}}::HandleCPULimit);
    testClass.def("handleMemLimit"        , &{{classname_full}}::HandleMemLimit);
    testClass.def("handleSpcLimit"        , &{{classname_full}}::HandleSpcLimit);
    testClass.def("handleNetLimit"        , &{{classname_full}}::HandleNetLimit);
    testClass.def("handleNICStateChange"  , &{{classname_full}}::HandleNICStateChange);
    testClass.def("handlePeerStateChange" , &{{classname_full}}::HandlePeerStateChange);
    testClass.def("handleReinstate"       , &{{classname_full}}::HandleReinstate);
    testClass.def("handleActivate"        , &{{classname_full}}::HandleActivate);

    m.def("create_component_py", &create_component_py, "Instantiates the component from python configuration");
}
{% endblock pybind %}
