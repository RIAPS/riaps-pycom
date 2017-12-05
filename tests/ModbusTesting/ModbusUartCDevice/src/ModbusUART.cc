#include <unistd.h>
#include <string.h>
#include <iostream>
#include "ModbusUART.h"


namespace riapsmodbuscreqrepuart {
    namespace components {

        ModbusUART::ModbusUART(_component_conf &config, riaps::Actor &actor) :
                ModbusUARTBase(config, actor) {
            PID = getpid();

            debugMode = false;
            SetDebugLevel(_logger, spdlog::level::level_enum::debug);  // MM TODO:  for running, set to err

            holding_regs = (uint16_t *) malloc(nb_holdingRegs * sizeof(uint16_t));
            memset(holding_regs, 0, nb_holdingRegs * sizeof(uint16_t));
            input_regs = (uint16_t *) malloc(nb_inputRegs * sizeof(uint16_t));
            memset(input_regs, 0, nb_inputRegs * sizeof(uint16_t));
            coilinput_bits = (uint8_t *) malloc(nb_coilInputBits * sizeof(uint8_t));
            memset(coilinput_bits, 0, nb_coilInputBits * sizeof(uint8_t));

            auto iport = GetConfig().component_parameters.GetParam("port");
            if (iport != nullptr) {
                std::string iportStr = iport->GetValueAsString();
                if (iportStr == "UART1") {
                    portConfig.portname = "/dev/ttyO1";
                }
                else if (iportStr == "UART2") {
                    portConfig.portname = "/dev/ttyO2";
                }
                else if (iportStr == "UART3") {
                    portConfig.portname = "/dev/ttyO3";
                }
                else if (iportStr == "UART4") {
                    portConfig.portname = "/dev/ttyO4";
                }
                else if (iportStr == "UART5") {
                    portConfig.portname = "/dev/ttyO5";
                }
                else {
                    _logger->error("{}: Invalid UART argument (port={}), use port = UART1..5", PID,
                                       iport->GetValueAsString());
                }
            }

            auto ibaudrate = GetConfig().component_parameters.GetParam("baudrate");
            if (ibaudrate != nullptr) {
                // MM TODO:  GetValueAsInt is currently unavailable (riaps-core 0.6.1Test)
                // portConfig.baudrate = ibaudrate->GetValueAsInt();
                portConfig.baudrate = std::stoi(ibaudrate->GetValueAsString());
            }

            auto ibytesize = GetConfig().component_parameters.GetParam("bytesize");
            if (ibytesize != nullptr) {
                // MM TODO:  GetValueAsInt is currently unavailable (riaps-core 0.6.1Test)
                //portConfig.bytesize = ibytesize->GetValueAsInt();
                portConfig.bytesize = std::stoi(ibytesize->GetValueAsString());
            }

            auto iparity = GetConfig().component_parameters.GetParam("parity");
            if (iparity != nullptr) {
                portConfig.parity = iparity->GetValueAsString()[0];
            }

            auto istopbits = GetConfig().component_parameters.GetParam("stopbits");
            if (istopbits != nullptr) {
                // MM TODO:  GetValueAsInt is currently unavailable (riaps-core 0.6.1Test)
                //portConfig.stopbits = istopbits->GetValueAsInt();
                portConfig.stopbits = std::stoi(istopbits->GetValueAsString());
            }

            auto islaveaddress = GetConfig().component_parameters.GetParam("slaveaddress");
            if (islaveaddress != nullptr) {
                // MM TODO:  GetValueAsInt is currently unavailable (riaps-core 0.6.1Test)
                //portSlaveAddress = islaveaddress->GetValueAsInt();
                portSlaveAddress = std::stoi(islaveaddress->GetValueAsString());
            }

            portSerialMode = MODBUS_RTU_RS232;

            _logger->info("{}: Modbus settings {} @{}:{} {}{}{}", PID, portSlaveAddress, portConfig.portname,
                          portConfig.baudrate, portConfig.bytesize, portConfig.parity, portConfig.stopbits);
        }

        void ModbusUART::OnModbusRepPort(const riapsModbusUART::CommandFormat::Reader &message,
                                         riaps::ports::PortBase *port) {
            _logger->info("ModbusUART::OnModbusRepPort()");

            int responseValue = -1;  // invalid response

            if (isModbusReady()) {
                responseValue = sendModbusCommand(message);

                capnp::MallocMessageBuilder messageRepBuilder;
                riapsModbusUART::ResponseFormat::Builder msgModbusResponse = messageRepBuilder.initRoot<riapsModbusUART::ResponseFormat>();
                msgModbusResponse.setCommandType(message.getCommandType());
                msgModbusResponse.setRegisterAddress(message.getRegisterAddress());
                msgModbusResponse.setNumberOfRegs(responseValue);  // for writes, this value is 1 if successful, -1 if failed

                if(responseValue > 0) {
                    auto values = msgModbusResponse.initValues(responseValue);

                    if ((message.getCommandType() == (int16_t) ModbusCommands::READ_COILBITS) ||
                        (message.getCommandType() == (int16_t) ModbusCommands::READ_INPUTBITS)) {
                        for (int i = 0; i <= responseValue; i++) {
                            values.set(i, (uint16_t) coilinput_bits[i]);
                        }

                    } else if (message.getCommandType() == (int16_t) ModbusCommands::READ_INPUTREGS) {
                        for (int i = 0; i <= responseValue; i++) {
                            values.set(i, input_regs[i]);
                        }
                    } else if ((message.getCommandType() == (int16_t) ModbusCommands::READ_HOLDINGREGS) ||
                               (message.getCommandType() == (int16_t) ModbusCommands::WRITEREAD_HOLDINGREGS)) {
                        for (int i = 0; i <= responseValue; i++) {
                            values.set(i, holding_regs[i]);
                        }
                    }
                }
                // Send response back to requester
                _logger->warn_if(!SendModbusRepPort(messageRepBuilder, msgModbusResponse),
                                 "{}: Couldn't send response message", PID);
            } else {
                _logger->warn("{}: Modbus is not ready for commands", PID);
            }
        }

        void ModbusUART::OnClock(riaps::ports::PortBase *port) {
            _logger->debug("{}: ModbusUART::OnClock(): port={}", PID, port->GetPortName());

            if (!isModbusReady()) {
                // Start Modbus
                ctx = startRTUModbus(portConfig, portSlaveAddress, portSerialMode);
                _logger->debug("{}: Started Modbus: port={}, slaveAddress={}", PID, portConfig.portname,
                               portSlaveAddress);
            }

            // Halt clock port
            auto timerPort = GetPortByName(PORT_TIMER_CLOCK);
            if (timerPort == nullptr) {
                auto t = timerPort->AsTimerPort();
                if (t != nullptr) t->stop();
            }
        }

        int ModbusUART::sendModbusCommand(const riapsModbusUART::CommandFormat::Reader &message) {
            int value = 999;   // Return from the commands - read return number of items read, write provides success (1) / fail (0)
            int writeValue;

            int16_t regAddress = message.getRegisterAddress();
            int16_t numRegs = message.getNumberOfRegs();
            std::string valueLogMsg;


            switch (message.getCommandType()) {
                case (int16_t) ModbusCommands::READ_COILBITS:
                    value = readCoilBits(ctx, regAddress, numRegs, coilinput_bits);
                    _logger->debug("{}: Sent command {}, register={}, numOfDecimals={}", PID, "READ_COILBITS",
                                   regAddress, numRegs);
                    break;
                case (int16_t) ModbusCommands::READ_INPUTBITS:
                    value = readInputBits(ctx, regAddress, numRegs, coilinput_bits);
                    _logger->debug("{}: Sent command {}, register={}, numOfDecimals={}", PID, "READ_INPUTBITS",
                                   regAddress, numRegs);
                    break;
                case (int16_t) ModbusCommands::READ_INPUTREGS:
                    value = readInputRegs(ctx, regAddress, numRegs, input_regs);
                    _logger->debug("{}: Sent command {}, register={}, numOfRegs={}", PID, "READ_INPUTREGS", regAddress,
                                   numRegs);
                    break;
                case (int16_t) ModbusCommands::READ_HOLDINGREGS:
                    value = readHoldingRegs(ctx, regAddress, numRegs, holding_regs);
                    _logger->debug("{}: Sent command {}, register={}, numOfRegs={}", PID, "READ_HOLDINGREGS",
                                   regAddress, numRegs);
                    break;
                case (int16_t) ModbusCommands::WRITE_COILBIT:

                    writeValue = (int)message.getValues()[0];
                    value = writeCoilBit(ctx, regAddress, writeValue);
                    _logger->debug("{}: Sent command {}, register={}, value={}", PID, "WRITE_COILBIT", regAddress,
                                   writeValue);
                    break;
                case (int16_t) ModbusCommands::WRITE_HOLDINGREG:
                    writeValue = (int)message.getValues()[0];
                    value = writeHoldingReg(ctx, regAddress, writeValue);
                    _logger->debug("{}: Sent command {}, register={}, value={}", PID, "WRITE_HOLDINGREG", regAddress,
                                   writeValue);
                    break;
                case (int16_t) ModbusCommands::WRITE_COILBITS:
                    for (int i = 0; i <= numRegs; i++) {
                        coilinput_bits[i] = (uint8_t)message.getValues()[i];
                        valueLogMsg.append(std::to_string(coilinput_bits[i]) + " ");
                    }
                    value = writeCoilBits(ctx, regAddress, numRegs, coilinput_bits);
                    _logger->debug("{}: Sent command {}, register={}, numberOfDecimals={}", PID, "WRITE_COILBITS",
                                   regAddress, numRegs);
                    _logger->debug("{}: Values:{}", PID, valueLogMsg);
                    break;
                case (int16_t) ModbusCommands::WRITEMULTI_HOLDINGREGS:
                    for (int i = 0; i <= numRegs; i++) {
                        holding_regs[i] = (uint16_t)message.getValues()[i];
                        valueLogMsg.append(std::to_string(holding_regs[i]) + " ");
                    }
                    value = writeHoldingRegs(ctx, regAddress, numRegs, holding_regs);
                    _logger->debug("{}: Sent command {}, register={}, numOfRegs={}", PID, "WRITEMULTI_HOLDINGREGS",
                                   regAddress, numRegs);
                    _logger->debug("{}: Values:{}", PID, valueLogMsg);
                    break;
                case (int16_t) ModbusCommands::WRITEREAD_HOLDINGREGS:
                    for (int i = 0; i <= numRegs; i++) {
                        holding_regs[i] = (uint16_t)message.getValues()[i];
                        valueLogMsg.append(std::to_string(holding_regs[i]) + " ");
                    }
                    value = writeReadHoldingRegs(ctx, regAddress, numRegs, holding_regs, message.getWreadRegAddress(),
                                                 message.getWreadNumOfRegs(), holding_regs);
                    _logger->debug("{}: Sent command {}, writeReg={}, numOfRegsWrite={}, readReg={}, numOfRegsRead={}",
                                   PID, "WRITEREAD_HOLDINGREGS", regAddress, numRegs, message.getWreadRegAddress(),
                                   message.getWreadNumOfRegs());
                    _logger->debug("{}: Values:{}", PID, valueLogMsg);
                    break;
                default:
                    _logger->warn("{}: Invalid Command - {}", PID, message.getCommandType());
            }

            return value;
        }

        void ModbusUART::OnGroupMessage(const riaps::groups::GroupId &, capnp::FlatArrayMessageReader &,
                                        riaps::ports::PortBase *) {

        }

        ModbusUART::~ModbusUART() {
            if (isModbusReady()) {
                closeModbus(ctx);
            }

            free(holding_regs);
            free(holding_regs);
            free(input_regs);
            free(coilinput_bits);
        }
    }

    // Expose ModbusCommands to Python programs that need to interact with this device
//    PYBIND11_MODULE(riapsmodbusuartpy,m){
//        m.doc() = "pybind 11 RIAPS Modbus UART Interface Plugin";
//
//        py::enum_<ModbusCommands>(m, "ModbusCommands", py::arithmetic())
//                .value("READ_COILBITS", ModbusCommands::READ_COILBITS)
//                .value("READ_INPUTBITS", ModbusCommands::READ_INPUTBITS)
//                .value("READ_INPUTREGS", ModbusCommands::READ_INPUTREGS)
//                .value("READ_HOLDINGREGS", ModbusCommands::READ_HOLDINGREGS)
//                .value("WRITE_COILBIT", ModbusCommands::WRITE_COILBIT)
//                .value("WRITE_HOLDINGREG", ModbusCommands::WRITE_HOLDINGREG)
//                .value("WRITE_COILBITS", ModbusCommands::WRITE_COILBITS)
//                .value("WRITEMULTI_HOLDINGREGS", ModbusCommands::WRITEMULTI_HOLDINGREGS)
//                .value("WRITEREAD_HOLDINGREGS", ModbusCommands::WRITEREAD_HOLDINGREGS)
//                .export_values();
//        }

}

riaps::ComponentBase *create_component(_component_conf &config, riaps::Actor &actor) {
   auto result = new riapsmodbuscreqrepuart::components::ModbusUART(config, actor);
   return result;
}

void destroy_component(riaps::ComponentBase *comp) {
   delete comp;
}
