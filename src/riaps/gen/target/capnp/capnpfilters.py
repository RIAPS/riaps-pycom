import subprocess

def generate_capnp_id(value):
    cmd = ['capnp', 'id']
    id = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
    return id.decode("utf-8").rstrip()