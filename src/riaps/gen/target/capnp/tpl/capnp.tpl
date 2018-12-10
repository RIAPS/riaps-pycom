{{ ''|generateid }};

using Cxx = import "/capnp/c++.capnp";
$Cxx.namespace("{{element.appname|lower}}::messages");

{% for message in element.messages %}
# riaps:keep_{{message|lower}}:begin
struct {{message}} {


}
# riaps:keep_{{message|lower}}:end

{% endfor %}