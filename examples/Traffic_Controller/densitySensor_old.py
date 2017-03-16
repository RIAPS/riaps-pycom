#
from riaps.run.comp import Component
import logging

import socket
import json
import pprint

class densitySensor(Component):
    def __init__(self, parent):
        super(densitySensor, self).__init__(parent)
        self.gameSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.gameServerIP = "192.168.0.104"
        self.IC = self.parent.parent.name[-1]
        
    def on_clock(self):
        msg = self.clock.recv_pyobj()
        #self.logger.info('on_clock():%s', msg)
        gameDensity = self.send2Game(self.getDensities(self.IC))
        self.densityPort.send_pyobj(gameDensity)

        #self.logger.info('on_clock gameDensity:\n%s', pprint.pformat(gameDensity))
        msg = "data_ready"
        
    
    def send2Game(self, msg):
        response = 0
        self.gameSock.settimeout(1)
        msg_string = json.dumps(msg)
        #print ("msg string: {}".format(type(msg_string)))
        #gameSock.sendto(data_string, ("localhost", 11000))
        self.gameSock.sendto(msg_string.encode(encoding='utf_8', errors='strict'), (self.gameServerIP, 11000))
        #self.logger.info("@SEND msg_str: %s", pprint.pformat(msg_string))
        try:
            response_str, srvr = self.gameSock.recvfrom(1024)
            #self.logger.info("@SEND response_str: %s", pprint.pformat(response_str))
            response = json.loads(response_str.decode())

        except socket.timeout:
            response = ""
            self.logger.warning('Request timed out')
        return response
    
    def getDensities(self, IC):
        msg = {
                'Method': 'GETDENSITIES',
                'Object':{
                            'Name': 'NodeId',
                            'Type': 'PARAMETER',
                            'Value': IC,  #// should be 0 - 3 (for the selected ids)
                            'ValueType': 'System.UInt32',
                            'Parameters':
                            [
                                {
                                'Name': 'SegmentId',
                                'Type': 'PARAMETER',
                                'Value': 0,
                                'ValueType': 'System.UInt32'
                                },
                                {
                                'Name': 'SegmentId',
                                'Type': 'PARAMETER',
                                'Value': 1,
                                'ValueType': 'System.UInt32'
                                },
                                {
                                'Name': 'SegmentId',
                                'Type': 'PARAMETER',
                                'Value': 2,
                                'ValueType': 'System.UInt32'
                                },
                                {
                                'Name': 'SegmentId',
                                'Type': 'PARAMETER',
                                'Value': 3,
                                'ValueType': 'System.UInt32'
                                },

                            ]
                         }
                }
        return msg;