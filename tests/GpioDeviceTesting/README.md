# GPIO Device Component Testing

## Hardware Configuration

Test was done with an LED and resistor in series attached to P8_11 (connector_pin) on the BBB.  
The resistor side to ground and the LED in the pin location indicated.

## Software Configuration

* Install GPIO Python Library on both VM and BBBs
	- sudo pip3 install Adafruit_BBIO
 
### On the BBB:

* For this to work, the user account must be in the 'gpio' group (which it is for the base BBB image)
    * Verify that ‘riaps’ user is in the ‘gpio’ group
	    - groups riaps

