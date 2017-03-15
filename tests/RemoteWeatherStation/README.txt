Remote Weather Station Test is a device interface test for the UART1 on the beaglebone.  

Components are 
* WeatherReporter - includes UART1 interface for reading and writing
* WeatherListener - listens for the reporter data read and acknowledges the existence

The WeatherReporter will open the UART1 port and read the input when data arrives. It then publishes the DataFrame. 
WeatherListener subscribes to the DataFrame message and when a new message is received, it will publish an acknowledgement (DataAck = "OKAY, got it!").
The WeatherReporter listens for the DataAck and writes that message out to the UART port.

UART Configuration
------------------
port = '/dev/ttyO1'
baud rate = 115200
8 bit, parity = None, 1 stopbit   
timeout = 0, so it does not block 

HW notes on testing this
------------------------
Tools used:  
* Terminal tool on the host
* USB to 3.3 V TTL Cable (TTL-232R-3V3 by FTDI Chip) 
    - How to connect with BBB (P9 connector):  White (RX) to BBB TX (pin 24), Green (TX) to BBB RX (pin 26), GND on BBB pins 1, 2, 45, 46

Library used:
* pySerial used for UART communication
    - sudo pip3 install pyserial
    
Configuration needed on the BBB image (to be updated in a future image)
* in .bashrc, add setup environment variables for these tools 
    $ export SLOTS=/sys/devices/platform/bone_capemgr/slots
    $ export PINS=/sys/kernel/debug/pinctrl/44e10800.pinmux/pins 
* Update visudo to retain the environment variables on a su call
    * After "Defaults  env_reset"
    * Add
        * Defaults    env_keep += "SLOTS"  
        * Defaults    env_keep += "PINS" 
* To deal with user permission on UART
    $ sudo usermod -a -G dialout riaps
    $ sudo usermod -a -G dialout riapsdev

To turn on the UART1, modify /boot/uEnv.txt by uncommenting the following line and adding BB-UART1 (which points to an overlay in /lib/firmware)
	#Example v4.1.x
	#cape_disable=bone_capemgr.disable_partno=
	cape_enable=bone_capemgr.enable_partno=BB-UART1
	
Reboot the beaglebone to see the UART1 enabled. UART1 device is setup as ttyO1 (where the fourth letter is the letter 'O', no zero) 
that references ttyS1 (a special character files)

To verify that UART1 is enabled, do the following:
$ cat $SLOTS
 0: PF----  -1 
 1: PF----  -1 
 2: PF----  -1 
 3: PF----  -1 
 4: P-O-L-   0 Override Board Name,00A0,Override Manuf,BB-UART1
 
$ ls -l /dev/ttyO*
lrwxrwxrwx 1 root root 5 Mar  6 22:54 /dev/ttyO0 -> ttyS0
lrwxrwxrwx 1 root root 5 Mar  6 22:54 /dev/ttyO1 -> ttyS1


