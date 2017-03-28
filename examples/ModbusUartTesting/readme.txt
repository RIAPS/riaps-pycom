
BBB Software Setup Requirements
--------------------------------
sudo pip3 install minimalmodbus (which installs pyserial)
sudo pip3 install influxdb  # for logging


UART Configuration
------------------
port = '/dev/ttyO2'
baud rate = 57600
8 bit, parity = None, 1 stopbit   
timeout = 3 seconds

Modbus Configuration
--------------------
Slave Address:  10 or (0x0A)

InputRegs (read only) = [0]=outputCurrent,[1]=outputVolt,[2]=voltPhase,[3]=time
For Inverter control:
HoldingRegs (read/write) = [0]=unused, [1]=startStopCmd, [2]=power
 

HW notes setting up the UART on the BBB
---------------------------------------
Tools used to test UART2:  
* Terminal tool on the host
* USB to 3.3 V TTL Cable (TTL-232R-3V3 by FTDI Chip) 
    - How to connect with BBB (P9 connector):  White (RX) to BBB TX (pin 21), Green (TX) to BBB RX (pin 22), GND on BBB pins 1, 2, 45, 46
    
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
    $ sudo usermod -a -G dialout riapsdev  (if running on the host VM)

To turn on the UART2, modify /boot/uEnv.txt by uncommenting the following line and adding BB-UART2 (which points to an overlay in /lib/firmware)
	#Example v4.1.x
	#cape_disable=bone_capemgr.disable_partno=
	cape_enable=bone_capemgr.enable_partno=BB-UART2
	
Reboot the beaglebone to see the UART2 enabled. UART2 device is setup as ttyO2 (where the fourth letter is the letter 'O', no zero) 
that references ttyS2 (a special character files)

To verify that UART2 is enabled, do the following:
$ cat $SLOTS
 0: PF----  -1 
 1: PF----  -1 
 2: PF----  -1 
 3: PF----  -1 
 4: P-O-L-   0 Override Board Name,00A0,Override Manuf,BB-UART2
 
$ ls -l /dev/ttyO*
lrwxrwxrwx 1 root root 5 Mar  6 22:54 /dev/ttyO0 -> ttyS0
lrwxrwxrwx 1 root root 5 Mar  6 22:54 /dev/ttyO2 -> ttyS2

Connecting the BBB to the DSP Modbus UART Connection
-----------------------------------------------------
DSP:  C2000(TM) Microcontrollers (TMS320F28377S) LaunchPad Development Kit (LAUNCHXL-F28377S)
		Can by from Newark (http://www.newark.com/texas-instruments/launchxl-f28377s/dev-board-tms320f28377s-c2000/dp/49Y4795)
		powered by USB connection
		Code Composer Studio (CCS) by TI used to download software provide by NCSU (source code in library)
		Use CCS to start DSP application
		
BBB UART to DSP Modbus Connection:
      BBB TX (P9, pin 21) --> DSP RX (J4, pin 37, SCITXDB, GPIO15)
      BBB RX (P9, pin 22) --> DSP TX (J4, pin 38, SCIRXDB, GPIO14)
      
Tools used for debugging Modbus I/F:  
	BBB is master, slave simulator used was MODBUS RTU RS-232 PLC - Simulator found at www.plcsimulator.org
	DSP is slave, master simulator used was QModMaster 0.4.7, libmodbus 3.1.4 found at https://sourceforge.net/projects/qmodmaster

Debugging hints:
----------------
If serial port is busy, make sure to stop the gpsd service using the following command:
	$ sudo systemctl stop gpsd
      