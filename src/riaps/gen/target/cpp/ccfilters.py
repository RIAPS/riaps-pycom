import subprocess

def port_macro(value, port_type):
    if port_type == 'tims':
        return f"PORT_TIMER_{value.upper()}"
    return f"PORT_{port_type[:-1].upper()}_{value.upper()}"

def handler_name(value):
    return f"On{value.capitalize()}"

def sender_name(value):
    return f"Send{value.capitalize()}"

def generate_capnp_id(value):
    cmd = ['capnp', 'id']
    id = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
    return id.decode("utf-8").rstrip()

def recv_message_type(value, port_type):
    type_name = 'type'
    if port_type == 'tims':
        return ""
    elif port_type in ['clts', 'qrys', 'reqs']:
        type_name = 'rep_type'
    elif port_type in ['anss', 'reps', 'srvs']:
        type_name = 'req_type'
    return value[type_name]

def sender_message_type(value, port_type):
    type_name = 'type'
    if port_type == 'tims':
        return ""
    elif port_type in ['clts', 'qrys', 'reqs']:
        type_name = 'req_type'
    elif port_type in ['anss', 'reps', 'srvs']:
        type_name = 'rep_type'
    return value[type_name]

def recv_return_type(value, port_type):
    msg_type = recv_message_type(value, port_type)
    if msg_type == "":
        return ""
    return f"messages::{msg_type}::Reader"

def cpp_port_type(port_type):
    if port_type == 'tims':
        return 'PeriodicTimer'
    elif port_type in ['clts', 'reqs']:
        return 'RequestPort'
    elif port_type in ['reps', 'srvs']:
        return 'ResponsePort'
    elif port_type == 'pubs':
        return 'PublisherPort'
    elif port_type == 'subs':
        return 'SubscriberPort'
    elif port_type == 'anss':
        return 'AnswerPort'
    elif port_type == 'qrys':
        return 'QueryPort'
    else:
        return 'UnknownPort'