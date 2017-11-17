/*
 * Created on Nov 16, 2017
 *
 * @author: Mary Metelko
 *
 * This is a pybind wrapper around the libmodbus library - https://github.com/stephane/libmodbus.
 * Both RTU and TCP are available from libmodbus, but only RTU is implemented with this interface
 * at this time since HW tools available at the moment are serial I/F only.  This could easily be
 * expanded in the future to include TCP interface.
 *
 * MM TODO:  1) Definitely consider adding byte and response timeout setup in the future
 *           2) Add TCP capability later
 *           3) Error recovery available - reconnect and a sleep/flush sequence options
 *           4) Untested functions:  readInputBits, readCoilBits, writeCoilBit, writeCoilBits
 *
 *
 */


#include <iostream>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include "serialModbusComm.h"


bool portOpen = false;


/* Start RTU Modbus
 * Returns a pointer to a modbus_t structure if successful. Otherwise it shall return NULL.
 *   where, baudrate: 9600, 19200, 57600, 115200, etc
 *          Parity: 'N', 'O', 'E'
 *          Slave Address is a decimal value
 *          Serial Mode is either RS232 (0) or RS485 (1) -  RS232 mode is default
 */
modbus_t * startRTUModbus(struct serial_port_config portConfig, int slaveAddress, int serialMode)
{
    modbus_t *ctx;


    ctx = modbus_new_rtu(portConfig.portname.c_str(),portConfig.baudrate,portConfig.parity,portConfig.bytesize,portConfig.stopbits);

    // Enable debugging of libmodbus
    modbus_set_debug(ctx, true);

    modbus_set_slave(ctx, slaveAddress);

    if (serialMode == MODBUS_RTU_RS485) {
        if (modbus_rtu_set_serial_mode(ctx,serialMode) == -1) {
            fprintf(stderr, "Invalid Serial Mode: %s.  SerialMode=%d\n",modbus_strerror(errno),serialMode);
            modbus_free(ctx);
            return NULL;
        } else {
            std::cout<<"Modbus serial mode set to RS485"<<std::endl;
        }
    }

    if (modbus_connect(ctx) == -1) {
        fprintf(stderr, "Connection failed: %s\n",
                modbus_strerror(errno));
        modbus_free(ctx);
        return NULL;
    } else {
        portOpen = true;
        std::cout<<"SerialModbusComm - Modbus port open. Port="<<portConfig.portname<<","<<portConfig.baudrate<<","<<portConfig.bytesize<<","<<portConfig.parity<<","<<portConfig.stopbits<<std::endl;
    }

    return ctx;
}


/* Close Modbus */
void closeModbus(modbus_t *ctx){
    modbus_close(ctx);
    modbus_free(ctx);
    portOpen = false;
}


/* Is Modbus Ready?
 * User should make sure modbus is open before reading or writing bits or registers.
 */
bool isModbusReady(void){
    return portOpen;
}

/*  Read Coil Bit Status (Modbus Function Code = 0x01)
 *
 *  Reads the status of the 'nb' bits (coils) to the address 'addr' of the remote device. The result of reading
 *  is stored in 'dest' array as unsigned bytes (8 bits) set to TRUE or FALSE.

 *  User must take care to allocate enough memory to store the results in 'dest' (at least nb * sizeof(uint8_t)).
 *
 *  Returns the number of bits read if successful. Otherwise it shall return -1.
 */
int readCoilBits(modbus_t *ctx, int addr, int nb, uint8_t *dest){
    int bitsRead = 0;

    bitsRead = modbus_read_bits(ctx,addr,nb,dest);
    if (bitsRead == -1) {
        fprintf(stderr, "Failed to read coil bits: %s.  Address=%d,#Bits=%d\n",
                modbus_strerror(errno),addr,nb);
    }

    return bitsRead;
}


/*  Read Input Bits or Status (Modbus Function Code = 0x02)
 *
 *  Reads the content of the 'nb' input bits to the address 'addr' of the remote device. The result of reading
 *  is stored in 'dest' array as unsigned bytes (8 bits) set to TRUE or FALSE.
 *
 *  User must take care to allocate enough memory to store the results in 'dest' (at least nb * sizeof(uint8_t)).
 *
 *  Returns the number of bits read if successful. Otherwise it shall return -1.
 */
int readInputBits(modbus_t *ctx, int addr, int nb, uint8_t *dest){
    int bitsRead = 0;

    bitsRead = modbus_read_input_bits(ctx,addr,nb,dest);
    if (bitsRead == -1) {
        fprintf(stderr, "Failed to read input bits: %s.  Address=%d,#Bits=%d\n",
                modbus_strerror(errno),addr,nb);
    }

    return bitsRead;
}


/*  Read Holding Registers (Modbus Function Code = 0x03)
 *
 *  Reads the content of the 'nb' holding registers to the address 'addr' of the remote device.
 *  The result of reading is stored in 'dest' array as word values (16 bits).

 *  User must take care to allocate enough memory to store the results in 'dest' (at least nb * sizeof(uint16_t)).
 *
 *  Returns the number of holding registers read if successful. Otherwise it shall return -1.
 */
int readHoldingRegs(modbus_t *ctx, int addr, int nb, uint16_t *dest){
    int regsRead = 0;

    regsRead = modbus_read_registers(ctx,addr,nb,dest);
    if (regsRead == -1) {
        fprintf(stderr, "Failed to read coil bits: %s.  Address=%d,#Reg=%d\n",
                modbus_strerror(errno), addr, nb);
    }

    return regsRead;
}


/*  Read Input Registers (Modbus Function Code = 0x04)
 *
 *  Reads the content of the 'nb' input registers to address 'addr' of the remote device.
 *  The result of the reading is stored in 'dest' array as word values (16 bits).

 *  User must take care to allocate enough memory to store the results in 'dest' (at least nb * sizeof(uint16_t)).
 *
 *  Returns the number of input registers read if successful. Otherwise it shall return -1.
 */
int readInputRegs(modbus_t *ctx, int addr, int nb, uint16_t *dest){
    int regsRead = 0;

    regsRead = modbus_read_input_registers(ctx,addr,nb,dest);
    if (regsRead == -1) {
        fprintf(stderr, "Failed to read coil bits: %s.  Address=%d,#Reg=%d\n",
                modbus_strerror(errno),addr,nb);
    }

    return regsRead;
}


/*  Write a single coil bit (Modbus Function Code = 0x05)
 *
 *  Writes the status of 'status' at the address 'addr' of the remote device.
 *  The value must be set to TRUE or FALSE.
 *
 *  Returns return 1 if successful. Otherwise it shall return -1.
 */
int writeCoilBit(modbus_t *ctx, int addr, int status){
    int bitWritten = 0;

    bitWritten = modbus_write_bit(ctx,addr,status);
    if (bitWritten == -1) {
        fprintf(stderr, "Failed to write coil bit: %s.  Address=%d,Status=%d\n",
                modbus_strerror(errno),addr,status);
    }

    return bitWritten;
}


/*  Write a single register (Modbus Function Code = 0x06)
 *
 *  Writes the value of 'value' holding registers at the address 'addr' of the remote device.
 *
 *  Returns return 1 if successful. Otherwise it shall return -1.
 */
int writeHoldingReg(modbus_t *ctx, int addr, int value){
    int valueWritten = 0;

    valueWritten = modbus_write_register(ctx,addr,value);
    if (valueWritten == -1) {
        fprintf(stderr, "Failed to write holding register: %s.  Address=%d,Value=%d\n",
                modbus_strerror(errno),addr,value);
    }

    return valueWritten;
}


/*  Write multiple coil bits (Modbus Function Code = 0x0F)
 *
 *  Writes the status of the 'nb' bits (coils) from 'src' at the address 'addr' of the remote device.
 *  The src array must contains bytes set to TRUE or FALSE.
 *
 *  Returns return return the number of written bits if successful. Otherwise it shall return -1.
 */
int writeCoilBits(modbus_t *ctx, int addr, int nb, const uint8_t *src){
    int bitsWritten = 0;

    bitsWritten = modbus_write_bits(ctx,addr,nb,src);
    if (bitsWritten == -1) {
        fprintf(stderr, "Failed to write coil bits: %s.  Address=%d,#Bits=%d\n",
                modbus_strerror(errno),addr,nb);
    }

    return bitsWritten;
}


/*  Write holding registers (Modbus Function Code = 0x10)
 *
 *  Writes the content of the 'nb' holding registers from the array 'src' at address 'addr' of the remote device.
 *
 *  Returns return the number of written registers if successful. Otherwise it shall return -1.
 */
int writeHoldingRegs(modbus_t *ctx, int addr, int nb, const uint16_t *src){
    int valuesWritten = 0;

    valuesWritten = modbus_write_registers(ctx,addr,nb,src);
    if (valuesWritten == -1) {
        fprintf(stderr, "Failed to write holding registers: %s.  Address=%d,#Regs=%d\n",
                modbus_strerror(errno),addr,nb);
    }

    return valuesWritten;
}


/*  Write and read many holding registers in a single transaction (Modbus Function Code = 0x17)
 *
 *  Writes the content of the 'write_nb' holding registers from the array 'src' to the address 'write_addr'
 *  of the remote device, then reads the content of the 'read_nb' holding registers to the address 'read_addr'
 *  of the remote device. The result of reading is stored in 'dest' array as word values (16 bits).
 *
 *  User must take care to allocate enough memory to store the results in 'dest' (at least nb * sizeof(uint16_t)).
 *
 *  Returns return the number of read registers if successful. Otherwise it shall return -1.
 */
int writeReadHoldingRegs(modbus_t *ctx, int write_addr, int write_nb, const uint16_t *src, int read_addr, int read_nb, uint16_t *dest){
    int regsRead = 0;

    regsRead = modbus_write_and_read_registers(ctx,write_addr,write_nb,src,read_addr,read_nb,dest);
    if (regsRead == -1) {
        fprintf(stderr, "Failed to write/read holding registers: %s.  WriteAddr=%d,#WriteRegs=%d,ReadAddr=%d,#ReadRegs=%d\n",
                modbus_strerror(errno),write_addr,write_nb,read_addr,read_nb);
    }

    return regsRead;
}

        
        
        