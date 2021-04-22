'''
Application descriptor (used as a yaml object)

Created on Oct 29, 2018

@author: riaps
'''
import yaml


class AppDescriptor(yaml.YAMLObject):
    '''
    RIAPS app origin - 'signature file
    url = URL of the repo (or local folder) the app is coming from
    host = host IP addares
    mac = MAC address of host
    sha = SHA of package
    home = local source folder (used in remote debugging)
    hosts = hosts participating in the app
    network = network access control for nodes, (ip|'[]') => [] | [ ('dns' | ip) ]+  
    '''
    yaml_loader = yaml.SafeLoader

    def __init__(self, url, host, mac, sha, home, hosts, network):
        self.url = url
        self.host = host
        self.mac = mac
        self.sha = sha
        self.home = home
        self.hosts = hosts
        self.network = network
        
    def __repr__(self):
        return "%s(url=%r, host=%r, mac=%r, sha=%r, home=%r, hosts=%r, network=%r)" % (
             self.__class__.__name__, self.url, self.host, self.mac, self.sha, self.home,
             self.hosts, self.network)

