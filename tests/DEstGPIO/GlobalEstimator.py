# GlobalEstimator.py
from riaps.run.comp import Component
import os
import logging
import time
# import Adafruit_BBIO.GPIO as GPIO

class GlobalEstimator(Component):
    def __init__(self):
        super(GlobalEstimator, self).__init__()
        self.pid = os.getpid()
        self.logger.info("(PID %s) - starting GlobalEstimator()" % str(self.pid))

#         ''' Enable GPIO '''
#         self.pinName = 'USR3'
#         self.initialValue = 0
#         self.setupDelay = 60
#         self.gpioOn = 1
#         self.gpioOff = 0
#         GPIO.setup(self.pinName,GPIO.OUT,GPIO.PUD_OFF,self.initialValue, self.setupDelay)

        self.availNumEst = 0
        self.runningSum = 0


    def on_estimate(self):
        msg = self.estimate.recv_pyobj()
        self.logger.info("PID (%s) - on_estimate():%s" % (str(self.pid), str(msg)))
        (estPid,sTime,sensorVal) = msg
        self.runningSum += sensorVal
        self.availNumEst += 1


    def on_wakeup(self):
        now = self.wakeup.recv_pyobj()
        #self.logger.info('PID(%s) - on_wakeup(): %s' % (str(self.pid),str(now)))

        ''' Average existing estimate '''
        if self.availNumEst != 0:
            averageEst = self.runningSum / self.availNumEst
            self.logger.info("global_est(value=%s)" % averageEst)

#             ''' Toggle GPIO '''
#             GPIO.output(self.pinName, self.gpioOn)
#             time.sleep(0.1)
#             GPIO.output(self.pinName, self.gpioOff)


    def __destroy__(self):
        self.logger.info("(PID %s) - stopping GlobalEstimator" % str(self.pid))
#         GPIO.cleanup(self.pinName)
