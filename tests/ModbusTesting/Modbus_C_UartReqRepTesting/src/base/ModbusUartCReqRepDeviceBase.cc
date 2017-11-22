//
// Created by istvan on 3/10/17.
//

#include <base/SensorBase.h>

namespace distributedestimator {
    namespace components {

        comp_modbusUartCReqRepDeviceBase::comp_modbusUartCReqRepDeviceBase(_component_conf &config, riaps::Actor &actor) : ComponentBase(config,
                                                                                                       actor) {

        }

        void comp_modbusUartCReqRepDeviceBase::DispatchMessage(capnp::FlatArrayMessageReader* capnpreader,
                                              riaps::ports::PortBase *port) {
            auto portName = port->GetPortName();
            if (portName == PORT_TIMER_CLOCK) {
                OnClock(port);
            } else if (portName == PORT_REQ_MODBUSREQPORT) {
                auto ModbusCommand = capnpreader->getRoot<messages::ModbusCommand>();
                OnModbusReqPort(ModbusCommand, port);
            }

        }

        void comp_modbusUartCReqRepDeviceBase::DispatchInsideMessage(zmsg_t *zmsg, riaps::ports::PortBase *port) {

        }

        bool comp_modbusUartCReqRepDeviceBase::SendModbusReqPort(capnp::MallocMessageBuilder&    messageBuilder,
                                          messages::ModbusResponse::Builder& message) {
            return SendMessageOnPort(messageBuilder, PORT_REQ_MODBUSREQPORT);
        }

        comp_modbusUartCReqRepDeviceBase::~comp_modbusUartCReqRepDeviceBase() {

        }

    }
}