#ifndef SERIALMODBUSCOMM_H
#define SERIALMODBUSCOMM_H

#include <modbus/modbus.h>
#include <modbus/modbus-rtu.h>
#include <tuple>


typedef struct serial_port_config {
    std::string portname; 
    int baudrate; 
    int bytesize; 
    char parity; 
    int stopbits;
}serial_port_config_t;


modbus_t * startRTUModbus(struct serial_port_config portConfig, int slaveAddress, int serialMode);
void closeModbus(modbus_t *ctx);
bool isModbusReady(void);
int readCoilBits(modbus_t *ctx, int addr, int nb, uint8_t *dest);
int readInputBits(modbus_t *ctx, int addr, int nb, uint8_t *dest);
int readHoldingRegs(modbus_t *ctx, int addr, int nb, uint16_t *dest);
int readInputRegs(modbus_t *ctx, int addr, int nb, uint16_t *dest);
int writeCoilBit(modbus_t *ctx, int addr, int status);
int writeHoldingReg(modbus_t *ctx, int addr, int value);
int writeCoilBits(modbus_t *ctx, int addr, int nb, const uint8_t *src);
int writeHoldingRegs(modbus_t *ctx, int addr, int nb, const uint16_t *src);
int writeReadHoldingRegs(modbus_t *ctx, int write_addr, int write_nb, const uint16_t *src, int read_addr, int read_nb, uint16_t *dest);

#endif /* SERIALMODBUSCOMM_H */