{% import 'macros.tpl' as macros %}

{% set baseclassname = [element.name,'Base']|join %}
{% set classname = element.name %}
{% set classname_full = [element.appname|lower,'::components::',classname]|join %}

{% block macros %}{% endblock %}

{% block includes %}{% endblock %}
{% block portdefinitions %}{% endblock %}

namespace {{element.appname|lower}} {
    namespace components {
{% block component %} {% endblock %}
    }
}

{% block pybind %}{% endblock %}

{% block endmacros %}{% endblock %}
