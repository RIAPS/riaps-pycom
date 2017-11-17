MM TODO:  Update this to match C library usage and install

# RIAPS Application Description
* ComputationalComponent.py - this is the application code that send and reads data as desired by the application needs 
* ModbusUartDevice.py - this is the device actor that utilizes the Modbus UART interface and uses the developed library for communications
  - RIAPS developed library:  serialModbusLib

# BBB Software Setup Requirements

```
    sudo pip3 install minimalmodbus (which installs pyserial)
```

   For InfluxDB: On BBB or VM (where logging is happening)
   
```
    $ curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -      
    $ source /etc/lsb-release     
    $ echo "deb https://repos.influxdata.com/${DISTRIB_ID,,} ${DISTRIB_CODENAME} stable" | sudo tee /etc/apt/sources.list.d/influxdb.list     
    $ sudo apt-get update -y && sudo apt-get install influxdb -y      
    $ sudo systemctl start influxdb
```

   On BBB, configure python library
  
```
    $ sudo pip3 install influxdb
```
    
# UART Configuration
* port = '/dev/ttyO2'
* baud rate = 57600
* 8 bit, parity = None, 1 stopbit   
* timeout = 3 seconds

# Modbus Configuration
* Slave Address:  10 or (0x0A)

* InputRegs (read only)
  - [0]=outputCurrent,
  - [1]=outputVolt,
  - [2]=voltPhase,
  - [3]=time

* For Inverter control:  HoldingRegs (read/write)
  - [0]=unused
  - [1]=startStopCmd
  - [2]=power

# HW notes setting up the UART on the BBB
* Tools used to test UART2:  
  - Terminal tool on the host
  - USB to 3.3 V TTL Cable (TTL-232R-3V3 by FTDI Chip) 
    - How to connect with BBB (P9 connector) 
      - White (RX) to BBB TX (pin 21), 
      - Green (TX) to BBB RX (pin 22), 
      - GND on BBB pins 1, 2, 45, 46
    - Cable information from https://www.adafruit.com/product/954?gclid=EAIaIQobChMIlIWZzJvX1QIVlyOBCh3obgJjEAQYASABEgImJfD_BwE
    
* To turn on the UART2, on the beaglebone, modify /boot/uEnv.txt by uncommenting the following line and adding BB-UART2 
(which points to an overlay in /lib/firmware)
```
	#Example v4.1.x
	#cape_disable=bone_capemgr.disable_partno=
	cape_enable=bone_capemgr.enable_partno=BB-UART2
```

* Reboot the beaglebone to see the UART2 enabled. UART2 device is setup as ttyO2 (where the fourth letter 
is the letter 'O', not zero) that references ttyS2 (a special character files)

* To verify that UART2 is enabled, do the following:
```
	$ cat $SLOTS
	 0: PF----  -1 
	 1: PF----  -1 
	 2: PF----  -1 
	 3: PF----  -1 
	 4: P-O-L-   0 Override Board Name,00A0,Override Manuf,BB-UART2
```
 
$ ls -l /dev/ttyO*
```
	lrwxrwxrwx 1 root root 5 Mar  6 22:54 /dev/ttyO0 -> ttyS0
	lrwxrwxrwx 1 root root 5 Mar  6 22:54 /dev/ttyO2 -> ttyS2
```

# Connecting the BBB to the DSP Modbus UART Connection
* DSP:  C2000(TM) Microcontrollers (TMS320F28377S) LaunchPad Development Kit (LAUNCHXL-F28377S)
* Can buy from Newark (http://www.newark.com/texas-instruments/launchxl-f28377s/dev-board-tms320f28377s-c2000/dp/49Y4795)
  - powered by USB connection
* Code Composer Studio (CCS) by TI used to download software provide by NCSU (source code in library)
* Use CCS to start DSP application
		
# BBB UART to DSP Modbus Connection
* BBB TX (P9, pin 21) --> DSP RX (J4, pin 37, SCITXDB, GPIO15)
* BBB RX (P9, pin 22) --> DSP TX (J4, pin 38, SCIRXDB, GPIO14)
      
# Tools used for debugging Modbus I/F  
* BBB is master, so to debug this interface a slave simulator was used: MODBUS RTU RS-232 PLC 
  - Simulator found at www.plcsimulator.org
* DSP is slave, so to debug this interface a master simulator was used: QModMaster 0.4.7
  - libmodbus 3.1.4 found at https://sourceforge.net/projects/qmodmaster
* Modbus Message Parser
  - http://modbus.rapidscada.net/

# Debugging hints
* If serial port is busy, make sure to stop the gpsd service using the following command
```
	$ sudo systemctl stop gpsd
```
      
