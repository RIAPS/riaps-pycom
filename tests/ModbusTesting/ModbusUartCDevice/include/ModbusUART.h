//
// Auto-generated by edu.vanderbilt.riaps.generator.ComponenetGenerator.xtend
//
#ifndef RIAPS_FW_MODBUSUART_H
#define RIAPS_FW_MODBUSUART_H

#include "base/ModbusUARTBase.h"
#include "SerialModbusComm.h"

namespace riapsmodbuscreqrepuart {
   namespace components {

       enum class ModbusCommands {
           READ_COILBITS = 1,
           READ_INPUTBITS = 2,
           READ_INPUTREGS = 3,
           READ_HOLDINGREGS = 4,
           WRITE_COILBIT = 5,
           WRITE_HOLDINGREG = 6,
           WRITE_COILBITS = 7,
           WRITEMULTI_HOLDINGREGS = 8,
           WRITEREAD_HOLDINGREGS = 9
       };

       class ModbusUART : public ModbusUARTBase {
         
         public:
         
           ModbusUART(_component_conf &config, riaps::Actor &actor);
         
           //virtual void OnModbusRepPort(const
          // messages::edu.vanderbilt.riaps.app.impl.FStructTypeImpl@3dbfaaf0 (name: CommandFormat)::Reader &message, riaps::ports::PortBase *port);

           virtual void OnModbusRepPort(const riapsModbusUART::CommandFormat::Reader &message, riaps::ports::PortBase *port);

           virtual void OnClock(riaps::ports::PortBase *port);
         
           virtual ~ModbusUART();

         private:
           pid_t PID;
           bool debugMode;
           struct serial_port_config portConfig;
           int portSlaveAddress;
           int portSerialMode;
           modbus_t *ctx;
           int nb_holdingRegs = 3;
           int nb_inputRegs = 4;
           int nb_coilInputBits = 8;
           uint16_t *holding_regs;
           uint16_t *input_regs;
           uint8_t *coilinput_bits;

           int sendModbusCommand(const riapsModbusUART::CommandFormat::Reader &message);

       };
   }
}

extern "C" riaps::ComponentBase* create_component(_component_conf&, riaps::Actor& actor);
extern "C" void destroy_component(riaps::ComponentBase*);


#endif //RIAPS_FW_MODBUSUART_H
