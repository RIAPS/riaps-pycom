//
// Created by Mary on 11/20/17.
//

#ifndef MODBUSUARTC_REQREP_DEVICE_H
#define MODBUSUARTC_REQREP_DEVICE_H

#include "base/ModbusUartCReqRepDeviceBase.h"

namespace RIAPSModbusCReqRepUART {
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
    
        class comp_modbusUartCReqRepDevice : public comp_modbusUartCReqRepDeviceBase {

        public:

            comp_modbusUartCReqRepDevice(_component_conf &config, riaps::Actor &actor);
            virtual ~comp_modbusUartCReqRepDevice();

        protected:

            virtual void OnClock(riaps::ports::PortBase *port);

            virtual void OnModbusReqPort(const messages::ModbusCommand::Reader &message,
                                   riaps::ports::PortBase *port);

        private:
            pid_t PID;
            bool debugMode;
            struct serial_port_config portConfig;
            int portSlaveAddress;
            int portSerialMode;
            modbus_t *ctx;
            int nb_holdingRegs = 3;
            int nb_inputRegs = 4;
            int nb_coilBits = 8;
            uint16_t *holding_regs;
            uint16_t *input_regs;
            uint8_t *coil_bits;
        
            int sendModbusCommand(const messages::ModbusCommand::Reader &message);

        };
    }
}

extern "C" riaps::ComponentBase* create_component(_component_conf&, riaps::Actor& actor);
extern "C" void destroy_component(riaps::ComponentBase*);


#endif //MODBUSUARTC_REQREP_DEVICE_H