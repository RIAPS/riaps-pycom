{{ ''|generateid }};

using Cxx = import "/capnp/c++.capnp";
$Cxx.namespace("{{element.name|lower}}::messages");

{% for message in element.messages %}
# <<riaps:keep_{{message.name|lower}}--
struct {{message.name}} {


}
# --riaps:keep_{{message.name|lower}}>>

{% endfor %}