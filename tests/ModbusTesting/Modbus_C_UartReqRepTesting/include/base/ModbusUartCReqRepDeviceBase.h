//
// Created by Mary on 11/20/17.
//

#ifndef MODBUSUARTC_REQREP_DEVICEBASE_H
#define MODBUSUARTC_REQREP_DEVICEBASE_H

#include "componentmodel/r_componentbase.h"
#include "messages/RIAPSModbusCReqRepUART.capnp.h"

// TODO: Use constexpr instead of #define
#define PORT_REQ_MODBUSREQPORT "modbusRepPort"
#define PORT_TIMER_CLOCK "clock"

namespace RIAPSModbusCReqRepUART{
    namespace components{
        class comp_modbusUartCReqRepDeviceBase : public riaps::ComponentBase {

        public:
            comp_modbusUartCReqRepDeviceBase(_component_conf& config, riaps::Actor& actor);            
            virtual ~comp_modbusUartCReqRepDeviceBase();

        protected:
            virtual void OnClock(riaps::ports::PortBase* port)=0;
            
            virtual void OnModbusReqPort(const messages::ModbusCommand::Reader &message,
                                   riaps::ports::PortBase *port)=0;
                                   
            bool SendModbusReqPort(capnp::MallocMessageBuilder&    messageBuilder,
                           messages::ModbusResponse::Builder& message);


        private:
            virtual void DispatchMessage(capnp::FlatArrayMessageReader* capnpreader,
                                         riaps::ports::PortBase*   port);

            virtual void DispatchInsideMessage(zmsg_t* zmsg,
                                               riaps::ports::PortBase* port);
        };
    }
}


#endif //MODBUSUARTC_REQREP_DEVICEBASE_H
