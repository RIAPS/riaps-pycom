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
                portConfig.baudrate = ibaudrate->GetValueAsInt();
            }

            auto ibytesize = GetConfig().component_parameters.GetParam("bytesize");
            if (ibytesize != nullptr) {
                portConfig.bytesize = ibytesize->GetValueAsInt();
            }

            auto iparity = GetConfig().component_parameters.GetParam("parity");
            if (iparity != nullptr) {
                portConfig.parity = iparity->GetValueAsString()[0];
            }

            auto istopbits = GetConfig().component_parameters.GetParam("stopbits");
            if (istopbits != nullptr) {
                portConfig.stopbits = istopbits->GetValueAsInt();
            }

            auto islaveaddress = GetConfig().component_parameters.GetParam("slaveaddress");
            if (islaveaddress != nullptr) {
                portSlaveAddress = islaveaddress->GetValueAsInt();
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

                capnp::MallocMessageBuilder messageBuilder;
                riapsModbusUART::ResponseFormat::Builder msgModbusResponse = messageBuilder.initRoot<riapsModbusUART::ResponseFormat>();
                msgModbusResponse.setCommandType(message.getCommandType());
                msgModbusResponse.setRegisterAddress(message.getRegisterAddress());
                msgModbusResponse.setNumberOfRegs(
                        responseValue);  // for writes, this value is 1 if successful, -1 if failed

                if ((message.getCommandType() == (int16_t) ModbusCommands::READ_COILBITS) ||
                    (message.getCommandType() == (int16_t) ModbusCommands::READ_INPUTREGS)) {
                    uint16_t *retValues;
                    retValues = (uint16_t *) malloc(nb_coilInputBits * sizeof(uint16_t));
                    memset(retValues, 0, nb_coilInputBits * sizeof(uint16_t));

                    for (int i = 0; i <= responseValue; i++) {
                        retValues[i] = (uint16_t)coilinput_bits[i];
                    }

                    msgModbusResponse.setValues(retValues);
                    free(retValues);
                } else if (message.getCommandType() == (int16_t) ModbusCommands::READ_INPUTREGS) {
                    msgModbusResponse.setValues(input_regs);
                } else if ((message.getCommandType() == (int16_t) ModbusCommands::READ_HOLDINGREGS) ||
                           (message.getCommandType() == (int16_t) ModbusCommands::WRITEREAD_HOLDINGREGS)) {
                    msgModbusResponse.setValues(holding_regs);
                }

                _logger->warn_if(!SendModbusRepPort(messageBuilder, msgModbusResponse),
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
                    writeValue = reinterpret_cast<int>(message.getValues()[0]);
                    value = writeCoilBit(ctx, regAddress, writeValue);
                    _logger->debug("{}: Sent command {}, register={}, value={}", PID, "WRITE_COILBIT", regAddress,
                                   writeValue);
                    break;
                case (int16_t) ModbusCommands::WRITE_HOLDINGREG:
                    writeValue = reinterpret_cast<int>(message.getValues()[0]);
                    value = writeHoldingReg(ctx, regAddress, writeValue);
                    _logger->debug("{}: Sent command {}, register={}, value={}", PID, "WRITE_HOLDINGREG", regAddress,
                                   writeValue);
                    break;
                case (int16_t) ModbusCommands::WRITE_COILBITS:
                    for (int i = 0; i <= numRegs; i++) {
                        coilinput_bits[i] = reinterpret_cast<uint8_t>(message.getValues()[i]);
                    }
                    value = writeCoilBits(ctx, regAddress, numRegs, coilinput_bits);
                    _logger->debug("{}: Sent command {}, register={}, numberOfDecimals={}", PID, "WRITE_COILBITS",
                                   regAddress, numRegs);
                    _logger->debug("{}: Values:{}", PID, coilinput_bits);
                    break;
                case (int16_t) ModbusCommands::WRITEMULTI_HOLDINGREGS:
                    for (int i = 0; i <= numRegs; i++) {
                        holding_regs[i] = reinterpret_cast<uint16_t>(message.getValues()[i]);
                    }
                    value = writeHoldingRegs(ctx, regAddress, numRegs, holding_regs);
                    _logger->debug("{}: Sent command {}, register={}, numOfRegs={}", PID, "WRITEMULTI_HOLDINGREGS",
                                   regAddress, numRegs);
                    _logger->debug("{}: Values:{}", PID, holding_regs);
                    break;
                case (int16_t) ModbusCommands::WRITEREAD_HOLDINGREGS:
                    for (int i = 0; i <= numRegs; i++) {
                        holding_regs[i] = reinterpret_cast<uint16_t>(message.getValues()[i]);
                    }
                    value = writeReadHoldingRegs(ctx, regAddress, numRegs, holding_regs, message.getWreadRegAddress(),
                                                 message.getWreadNumOfRegs(), holding_regs);
                    _logger->debug("{}: Sent command {}, writeReg={}, numOfRegsWrite={}, readReg={}, numOfRegsRead={}",
                                   PID, "WRITEREAD_HOLDINGREGS", regAddress, numRegs, message.getWreadRegAddress(),
                                   message.getWreadNumOfRegs());
                    _logger->debug("{}: Values:{}", PID, holding_regs);
                    break;
                default:
                    _logger->warn("{}: Invalid Command - {}", PID, message.getCommandType());
            }

            return value;
        }

        ModbusUART::~ModbusUART() {
            if (isModbusReady()) {
                closeModbus(ctx);
            }

            free(holding_regs);
            free(input_regs);
            free(coilinput_bits);
        }
    }
}

riaps::ComponentBase *create_component(_component_conf &config, riaps::Actor &actor) {
   auto result = new riapsmodbuscreqrepuart::components::ModbusUART(config, actor);
   return result;
}

void destroy_component(riaps::ComponentBase *comp) {
   delete comp;
}
