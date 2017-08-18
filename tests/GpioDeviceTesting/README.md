# GPIO Device Component Testing

This test shows how to interface with the GPIO Device component from another RIAPS component (ToggleGpioComponent).  The component is able to read or write to GPIO pin that have been setup when configuring the GPIO Device component.

## Hardware Configuration

Test was done with an LED and resistor in series attached to P8_11 (connector_pin) on the BBB.  
The resistor side to ground and the LED in the pin location indicated.

## Software Configuration

### On Both VM and BBB

* Install GPIO Python Library

```
      $ sudo pip3 install Adafruit_BBIO
```
 
### On the BBB:

* For this to work, the user account must be in the 'gpio' group (which it is for the base BBB image)
    * Verify that ‘riaps’ user is in the ‘gpio’ group
    
    ```
      $ groups riaps
    ```

## Setting up an Application to Use GPIO Device Component

In the application model (.riaps file), create a GPIO device component with the configuration desired.  

```
      $ device GpioDeviceComponent(bbb_pin_name='P8_11', direction='OUT', pull_up_down='PUD_OFF', setup_delay=60) 
```

where,
- Pin name: connector and pin used on the BBB - P8_pin# or P9_pin# (***required input***)
- direction: pin direction - IN or OUT (***required input***)
- pull_up_down: BBB pin resistor configuration - ***PUD_OFF*** (***default***), PUD_UP or PUD_DOWN
- setup_delay: time in milliseconds to wait after exporting GPIO pin to give udev some time to set file permissions - ***default = 60 ms***, should not use over 1000 ms
  
To read a GPIO pin, the application publishes a ReadRequest message.  A timer (readValue) is used to call pollGpioValue.  The GPIO device component subscribes to the ReadRequest message and will publish the pin value as the DataValue message.  The application can subscribe (currentGpioValue) to the DataValue message to get the GPIO value that was read.

To write to a GPIO pin, the application publishes a WriteRequest message.  For pin toggling, a timer (toggle) is used to call writeGpioValue.
