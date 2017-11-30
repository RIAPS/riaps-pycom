Welcome to the RIAPS Modbus Device Testings

This current testing applications are:
* ModbusUartReqRepTesting
    - Application makes a command request to the device application and 
      will block until a response is returned.
    - Application and Device Components are both Python code
    - Works for 40 ms update rates or greater using a 115.2 kbps UART setup (example shows 57.6 kbps)
    - UART Physical Device only
* ModbusUartPollTesting (in development)
    - This could be utilized for systems that are reading measurements for updates.
    - Application sets up a polling request for reading or writing to a specific register set 
      (input or holding registers).  Then the application starts and stops the polling action.  
      Other commands can be requested during the polling, but could impact the system timing 
      if not carefully considered.  The polled information is published back thru a message 
      to the application at the period setup by the application.
    - Application and Device Components are both Python code
    - UART Physical Device only
* Modbus_C_UartReqRepTesting (in development)
    - This is the same as ModbusUartReqRepTesting, except that the Device Component is written
      as C++ component
    - Speed increase of this method is currently TBD
    - UART Physical Device only
    
The C++ Component code is located in ModbusUartCDevice.

The Modbus slave device is tested on a DSP.  The code for this is located in DSP_Code.

