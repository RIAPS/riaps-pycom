'''
Created on Oct 29, 2018

@author: riaps
'''

class Origin(object):
    '''
    RIAPS app origin - 'signature file
    url = URL of the repo (or local folder) the app is coming from
    host = host IP addares
    mac = MAC address of host
    sha = SHA of package
    home = local source folder (used in remote debugging)
    '''
    def __init__(self,url,host,mac,sha,home):
        self.url = url
        self.host = host
        self.mac = mac
        self.sha = sha
        self.home = home
    def __repr__(self):
        return "%s(url=%r, host=%r, mac=%r, sha=%r, home=%r)" % (
             self.__class__.__name__, self.url, self.host, self.mac, self.sha, self.home)
