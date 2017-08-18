Hardware Configuration
----------------------
Test was done with an LED and resistor in series attached to P8_11 (connector_pin) on the BBB.  
The resistor side to ground and the LED in the pin location indicated.

Software Configuration
----------------------
This software setup will be done as part of the release in the future.  They are noted here to explain how this test was performed.

On VM: 
* Install GPIO Python Library
	- sudo pip3 install Adafruit_BBIO
 
On the BBB:
* Place the attached rules file in the /etc/udev/rules.d folder (requires sudo) 
* Create a new group named ‘gpio’
	- sudo groupadd gpio
* Add ‘riaps’ user to ‘gpio’ group
	- sudo usermod –a –G gpio riaps
* Verify that ‘riaps’ user is in the ‘gpio’ group
	- groups riaps
* Install GPIO Python Library
	- sudo pip3 install Adafruit_BBIO
* Reboot the BBB (to allow udev rule to take effect)

