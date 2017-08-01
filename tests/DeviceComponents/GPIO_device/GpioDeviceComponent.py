'''
Created on Apr 4, 2017

@author: Mary Metelko

Edited on Jul 27, 2017
@author: Tim Krentz
'''

'''
The GPIO device component utilizes Adafruit_BBIO for control of the GPIO pins
Need to install this on the BBBs
    $ sudo pip3 install Adafruit_BBIO
'''

from riaps.run.comp import Component
import logging
import os
import threading
import Adafruit_BBIO.GPIO as GPIO
#import pydevd
import zmq


class GpioDeviceThread(threading.Thread):
    def __init__(self, component, trigger):
        threading.Thread.__init__(self)
        self.terminated = threading.Event()
        self.terminated.clear()
        self.active = threading.Event()
        self.component = component
        self.trigger = trigger
        self.gpioAvailable = False
        self.pid = os.getpid()
        self.component.logger.info("GpioDeviceThread [%s]: init",self.pid)

        # Convert input configurations into enums that represent the requests
        if self.component.direction == 'IN':
            self.direction = GPIO.IN
        elif self.component.direction == 'OUT':
            self.direction = GPIO.OUT
        else:
            self.direction = GPIO.ALT0

        if self.component.pull_up_down == "PUD_UP":
            self.pull_up_down = GPIO.PUD_UP
        elif self.component.pull_up_down == "PUD_DOWN":
            self.pull_up_down = GPIO.PUD_DOWN
        else:
            self.pull_up_down = GPIO.PUD_OFF

        if self.component.trigger_edge == "RISING":
            self.trigger_edge = GPIO.RISING
        elif self.component.trigger_edge == "FALLING":
            self.trigger_edge = GPIO.FALLING
        else:
            self.trigger_edge = GPIO.BOTH

    def run(self):
        # Ask parent port to make a plug for this end
        self.plug = self.trigger.setupPlug(self)
        self.poller = zmq.Poller()
        self.poller.register(self.plug, zmq.POLLIN)
        if self.terminated.is_set(): return
        self.enableGpio()  # setup the requested GPIO

        while True:
            self.active.wait(None)
            if self.terminated.is_set():
                self.disableGpio()
                break
            if self.active.is_set():
                socks = dict(self.poller.poll())
                if self.plug in socks and socks[self.plug] == zmq.POLLIN:
                    message = self.plug.recv_pyobj()

                    if 'write' in message:
                        GPIO.output(self.component.bbb_pin_name, message[1])
                        self.component.logger.info("GpioDeviceThread - value written to GPIO %s: %s",
                                                    self.component.bbb_pin_name, str(message[1]))
                        self.plug.send_pyobj(message[1])

                    elif 'read' in message:
                        val = GPIO.input(self.component.bbb_pin_name)
                        self.component.logger.info("GpioDeviceThread - value read from GPIO %s: %s",
                                                    self.component.bbb_pin_name, val)
                        self.plug.send_pyobj(val)


    def isGpioAvailable(self):
        return self.gpioAvailable

    def enableGpio(self):
        self.component.logger.info("GpioDeviceThread setting up GPIO=%s: direction=%s resistor=%s trigger=%s ivalue=%d delay=%d [%d]",
                                    self.component.bbb_pin_name, self.component.direction, self.component.pull_up_down,
                                    self.component.trigger_edge, self.component.initial_value, self.component.setup_delay, self.pid)
        GPIO.setup(self.component.bbb_pin_name, self.direction, self.pull_up_down,
                    self.component.initial_value, self.component.setup_delay)
        self.gpioAvailable = True
        self.component.logger.info("GpioDeviceThread GPIO=%s setup and available for use", self.component.bbb_pin_name)

    def disableGpio(self):
        GPIO.cleanup(self.component.bbb_pin_name)
        self.gpioAvailable = False
        self.component.logger.info("GpioDeviceThread - disabled GPIO: %s",self.component.bbb_pin_name)

    def activate(self):
        self.active.set()

    def deactivate(self):
        self.active.clear()

    def terminate(self):
        self.terminated.set()

'''
GPIO Device Options:
  Pin name: connector and pin used on the BBB - P8_pin# or P9_pin# (required input)
  direction: pin direction - IN or OUT (required input)
  pull_up_down: BBB pin resistor configuration - PUD_OFF (default), PUD_UP or PUD_DOWN
  trigger_edge: which edge to trigger on - RISING, FALLING, BOTH
  initial_value: if GPIO is OUT direction, then this initial value will be set - default = 0
  setup_delay: time in milliseconds to wait after exporting GPIO pin to give udev some time to set file permissions - default = 60 ms, should not use over 1000 ms

  Note:  edge triggering will not be implemented in the initial release of this device component (MM)
'''
class GpioDeviceComponent(Component):
    def __init__(self, bbb_pin_name='P8_11', direction='OUT', pull_up_down='PUD_OFF', trigger_edge='RISING',initial_value=0, setup_delay=60):
        super().__init__()
        self.logger.setLevel(logging.DEBUG)
        self.pid = os.getpid()
        self.bbb_pin_name = bbb_pin_name
        self.direction = direction
        self.pull_up_down = pull_up_down
        self.trigger_edge = trigger_edge
        self.initial_value = initial_value
        self.setup_delay = setup_delay
#        pydevd.settrace(host='192.168.1.102',port=5678)
        self.logger.info("GpioDeviceComponent @%s: %s %s %s ivalue=%d delay=%d [%d]", self.bbb_pin_name, self.direction, self.pull_up_down, self.trigger_edge, self.initial_value, self.setup_delay, self.pid)
        self.gpioDeviceThread = None                    # Cannot manipulate GPIOs in constructor or start threads


    def on_clock(self):
        now = self.clock.recv_pyobj()   # Receive time (as float)
        self.logger.info("on_clock()[%s]: %s",str(self.pid),now)

        if self.gpioDeviceThread == None:
            self.gpioDeviceThread = GpioDeviceThread(self,self.trigger)
            self.gpioDeviceThread.start()
            self.trigger.activate()

        self.clock.halt()

    def __destroy__(self):
        self.logger.info("__destroy__")
        if self.gpioDeviceThread != None:
            self.gpioDeviceThread.deactivate()
            self.gpioDeviceThread.terminate()

    def on_gpioRepPort(self):
        msg = self.gpioRepPort.recv_pyobj()
        self.logger.info("on_gpioRepPort")
        if self.gpioDeviceThread == None:
            self.logger.info("on_gpioRepPort()[%s]: gpioDeviceThread not available yet",str(self.pid))
            msg = ('ERROR',-1)
            self.gpioRepPort.send_pyobj(msg)
        else:
            if self.gpioDeviceThread.isGpioAvailable() == True:
                msgType, msgVal = msg
                if msgType == 'read':
                    self.trigger.send_pyobj('read')
                    response = self.trigger.recv_pyobj()
                    self.logger.info("on_gpioRepPort()[%s]: %s",str(self.pid),repr(msg))
                    self.gpioRepPort.send_pyobj(('read',response))
                    self.logger.info("on_gpioRepPort(): reading data from GPIO=%s", self.bbb_pin_name)

                elif msgType == 'write':
                    if msgVal == 1 or msgVal == 0:
                        self.trigger.send_pyobj((msgType,msgVal))
                        response = self.trigger.recv_pyobj()
                        self.logger.info("on_gpioRepPort()[%s]: %s",str(self.pid),repr(msg))
                        self.gpioRepPort.send_pyobj(('write',response))
                        self.logger.info("on_gpioRepPort(): sending data to GPIO=%s", self.bbb_pin_name)
                    else:
                        self.logger.info("on_gpioRepPort()[%s]: invalid write value",str(self.pid))
                        msg = ('ERROR',-1)
                        self.gpioRepPort.send_pyobj(msg)

                else:
                    self.logger.info("on_gpioRepPort()[%s]: unsupported request=%s",str(self.pid),repr(msg))
                    msg = ('ERROR',-1)
                    self.gpioRepPort.send_pyobj(msg)
            else:
                self.logger.info("on_gpioRepPort()[%s]: GPIO not available yet",str(self.pid))
                msg = ('ERROR',-1)
                self.gpioRepPort.send_pyobj(msg)
