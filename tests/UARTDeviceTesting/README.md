# UART Device Component Testing

This test shows how to interface with the UART Device component from another RIAPS component (TestUartComponentA and TestUartComponentB).
In this test, the TestUartActorA (using TestUartComponentA) will write an incremental count to the UART port while TestUartActorB (using TestUartComponentB) reads the value from the UART port.  

## Hardware Configuration

### UART Configuration
* port = '/dev/ttyO2'
* baud rate = 57600
* 8 bit, parity = None, 1 stopbit   
* timeout = 3 seconds

### BBB1 UART to BBB2 UART Wiring Connections
* UART1 BBB TX (P9, pin 21) --> UART2 RX (P9, pin 22)
* UART1 BBB RX (P9, pin 22) --> UART2 TX (P9, pin 21)

### Tools used to test UART2 on a single BBB (for debugging, if needed)

  - Terminal tool on the host
  - USB to 3.3 V TTL Cable (TTL-232R-3V3 by FTDI Chip) 
  - How to connect with BBB (P9 connector) 
    - White (RX) to BBB TX (pin 21), 
    - Green (TX) to BBB RX (pin 22), 
    - GND on BBB pins 1, 2, 45, 46
    - Cable information from https://www.adafruit.com/product/954?gclid=EAIaIQobChMIlIWZzJvX1QIVlyOBCh3obgJjEAQYASABEgImJfD_BwE
 
 ### Setup UART2 on BBBs
 
* To turn on the UART2, on the beaglebone, modify /boot/uEnv.txt by uncommenting the following line and adding BB-UART2 
(which points to an overlay in /lib/firmware)

```
    Example v4.1.x
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
``` 
    $ ls -l /dev/ttyO*

    lrwxrwxrwx 1 root root 5 Mar  6 22:54 /dev/ttyO0 -> ttyS0
    lrwxrwxrwx 1 root root 5 Mar  6 22:54 /dev/ttyO2 -> ttyS2
```

## Software Configuration

### On Both VM and BBB

* Install GPIO Python Library

```
    $ sudo pip3 install Adafruit_BBIO
```
 
### On the BBB:

* For this to work, the user account must be in the 'dialout' group (which it is for the base BBB image)
    * Verify that ‘riaps’ user is in the ‘dialout’ group
    
```
    $ groups riaps
```

## Setting up an Application to Use UART Device Component

In the application model (.riaps file), create two UART device components with the configuration desired.  

```
    device UartDeviceComponent(uart_port_name = 'UART2', baud_rate = 9600); 
```

where,
- Port Name: BBB UART port (UART1, 2, 3, 4, or 5)
- Baud Rate: UART rate in bits/sec, usually specified by slave device

  ***Note:  UART1 port is reserved for the ChronoCape hardware and should not be use*** 
  
Requests can be made to the UartDeviceComponent to read from the UART or write to it.  The UartDeviceComponent will respond once the action is complete.  

To write to the UART, create a message to indicate that this is a write command and the 'information to write'.  This will be sent as a request (uartReqPort) to the UART device component - see example message below.  The response will indicate this was a 'write' command and how many bytes were written (int value).

```
    msg = ('write',str.encode(<information to write>))
```

To read from the UART, create a message to indicate that this is a read command and how many bytes to be read.  This will be sent as a request (uartReqPort) to the UART device component - see example message below.  An acknowledgement of the command's receipt will be provided in a response immediately (before the read happens).  The response will indicate this was a 'read' command and return a message value of 1.

```
    msg = ('read', numBytes)
```
        
If the UART port is not available, the response message will be the following

```
    msg = ('ERROR',-1)
```

Other UART commands possible are to open or close the UART port.  The initialization of the UART device component will automatically open the UART2 port.  It is also possible to monitor the UART activity for debugging reasons using get_in_waiting, get_out_waiting, send_break, get_break_condition, and set_break_condition.  This test does not utilize these messages.

## Debugging hints

* If serial port is busy, make sure to stop the gpsd service using the following command

```
    $ sudo systemctl stop gpsd
```

