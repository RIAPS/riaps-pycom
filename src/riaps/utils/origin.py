'''
Created on Oct 29, 2018

@author: riaps
'''

class Origin(object):
    '''
    RIAPS app origin
    '''
    def __init__(self,url,host,mac,sha):
        self.url = url
        self.host = host
        self.mac = mac
        self.sha = sha
    def __repr__(self):
        return "%s(url=%r, host=%r, mac=%r, sha=%r)" % (
             self.__class__.__name__, self.url, self.host, self.mac, self.sha)
