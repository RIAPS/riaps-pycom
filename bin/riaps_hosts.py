# RIAPS hosts - list of RIAPS hosts on  configuration
# imported into the fab file
from fabric.api import *

env.hosts = [
            # Office 3 BBB cluster
            # 'bbb-6975.local', 'bbb-b863.local', 'bbb-4aba.local'
            # '192.168.0.101', '192.168.0.102', '192.168.0.103',
            # Home 4 BBB cluster  
            'bbb-78b2.local','bbb-4bbf.local','bbb-e8f2.local','bbb-9be2.local'
            ]
