# Distributed Estimator using GPIOs

Several RIAPS nodes (beaglebone black boards) gather local sensor data at different rates 
(0.5 Hz, 1 Hz and 2 Hz) and toggle one of the blue LEDs on the board when the estimate is 
published. A single RIAPS node subscribes to the estimates and provides a running average 
of the estimates. This node will print out the running average at a 4 Hz rate and toggle 
a blue LED on the board.

## Equipment Utilized
- 4 Beaglebone Black boards
	- 3 Local estimators
	- 1 Global aggregator
- Local router

## Dependencies

Utilized the Adafruit BBIO library to control the blue user controlled LEDs, which are 
just GPIOs

```
sudo pip3 install Adafruit_BBIO
```

## Developers
Gabor Karsai    Vanderbilt University
Mary Metelko    Vanderbilt University