//
// Created by Mary on 11/20/17.
//

#include <unistd.h>
#include <capnp/serialize.h>
#include <capnp/message.h>
#include "serialModbusLib/serialModbusComm.h"
#include "ModbusUartCReqRepDevice.h"


namespace RIAPSModbusCReqRepUART {
    namespace components {
// MM TODO:  adjust from python input to C++ - how to pass variables?
        comp_modbusUartCReqRepDevice::comp_modbusUartCReqRepDevice(_component_conf &config, riaps::Actor &actor, slaveaddress=0,port="UART2",baudrate=19200,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE) : comp_modbusUartCReqRepDeviceBase(config, actor) {            
            cpid = getpid();  

            debugMode = false;
            SetDebugLevel(_logger, spdlog::level::level_enum::debug);  // MM TODO:  for running, set to err
            
            holding_regs = (uint16_t *) malloc(nb_holdingRegs * sizeof(uint16_t));
            memset(holding_regs, 0, nb_holdingRegs * sizeof(uint16_t));
            input_regs = (uint16_t *) malloc(nb_inputRegs * sizeof(uint16_t));
            memset(input_regs, 0, nb_inputRegs * sizeof(uint16_t));
            coil_bits = (uint8_t *) malloc(nb_coilBits * sizeof(uint8_t));
            memset(coil_bits, 0, nb_coilBits * sizeof(uint8_t));

            auto iport = GetConfig().component_parameters.GetParam("port");
            if (iport!= nullptr){
                switch(iport->GetValueAsString()) {
                    case 'UART1':
                        portConfig.portname = '/dev/ttyO1';
                        break;
                    case 'UART2':
                        portConfig.portname = '/dev/ttyO2';
                        break;
                    case 'UART3':
                        portConfig.portname = '/dev/ttyO3';
                        break;
                    case 'UART4':
                        portConfig.portname = '/dev/ttyO4';
                        break;
                    case 'UART5':
                        portConfig.portname = '/dev/ttyO5';
                        break;
                    default:
                        _logger->error("{}: Invalid UART argument (port={}), use port = UART1..5", cpid, iport->GetValueAsString());
                }
            }

            auto ibaudrate = GetConfig().component_parameters.GetParam("baudrate");
            if (iport!= nullptr){

            }
            portConfig.baudrate = baudrate;
            portConfig.bytesize = bytesize;
            portConfig.parity = parity;
            portConfig.stopbits = stopbits;
           
            portSlaveAddress = slaveaddress;
            portSerialMode = MODBUS_RTU_RS232;  // MM TODO:  will this be found in .h paths?

            _logger->debug("Modbus settings {} @{}:{} {}{}{} [{}]", portSlaveAddress,portConfig.portname,portConfig.baudrate,portConfig.bytesize,portConfig.parity,portConfig.stopbits,cpid);
        }

        void comp_modbusUartCReqRepDevice::OnClock(riaps::ports::PortBase *port) {
            int64_t time = zclock_mono();
            //std::cout << "ModbusUartCReqRepDevice::OnClock(): " << time << std::endl;

            
            if (!isModbusReady()) {
            // Start Modbus
                ctx = startRTUModbus(portConfig,portSlaveAddress,portSerialMode);
            }

            if (debugMode){
                // MM TODO:  here is the Python Code to adjust to C++
                t1 = time.perf_counter()
                self.logger.debug("on_clock()[%s]: Modbus ready at %f, time to start Modbus is %f ms",str(self.pid),t1,(t1-t0)*1000)
            }

            // MM TODO:  here is the Python Code to adjust to C++
            if(ctx!=NULL){
               self.clock.halt();
            }            
        }

        void comp_modbusUartCReqRepDevice::OnModbusReqPort(const messages::ModbusCommand::Reader &message,
                                    riaps::ports::PortBase *port) {
            //PrintMessageOnPort(port);

            //std::cout << "Sensor::OnRequest(): " << message.getMsg().cStr() <<std::endl;

            // MM TODO:  here is the Python Code to adjust to C++
            '''Request Received'''
            commandRequest = self.modbusRepPort.recv_pyobj()

            if debugMode:
                self.modbusReqRxTime = time.perf_counter()
                #self.logger.debug("on_modbusRepPort()[%s]: Request=%s Received at %f",str(self.pid),commandRequest,self.modbusReqRxTime)

            self.unpackCommand(message)
            responseValue = -1  # invalid response
            if self.modbusReady == True:
                responseValue = self.sendModbusCommand()

                '''if debugMode:
                t1 = time.perf_counter()
                self.logger.debug("on_modbusRepPort()[%s]: Send Modbus response=%s back to requester at %f",str(self.pid),responseValue,t1)'''

            '''Send Results'''
            self.modbusRepPort.send_pyobj(responseValue)

            // MM TODO:  example of how to send a message out
            capnp::MallocMessageBuilder messageBuilder;
            messages::ModbusResponse::Builder msgModbusResponse = messageBuilder.initRoot<messages::ModbusResponse>();
            msgModbusResponse.setMsg("sensor_rep");

            if (!SendRequest(messageBuilder, msgModbusResponse)){
                // Couldn't send the response
            }
        }

        comp_modbusUartCReqRepDevice::~comp_modbusUartCReqRepDevice() {
            if (isModbusReady()){
                closeModbus(ctx);
            }
        }
     
        // MM TODO:  here is the Python Code to adjust to C++    
        int comp_modbusUartCReqRepDevice::sendModbusCommand(const messages::ModbusCommand::Reader &message){
            int value = 999   // Return from the commands - read return number of items read, write provides success (1) / fail (0)

            if debugMode:
                t0 = time.perf_counter()
                // MM TODO: update - self.logger.debug("sendModbusCommand()[%s]: Sending command to Modbus library at %f",str(self.pid),t0)

            switch(message.commandType) {
                case ModbusCommands::READ_COILBITS:
                    value = readCoilBits(ctx, message.registerAddress, message.numberOfDecimals, coil_bits);
                    // MM TODO: update - self.logger.info("ModbusUartDevice: sent command %s, register=%d, numOfDecimals=%d, signed=%s", ModbusCommands.READ_INPUTREG.name,self.registerAddress,self.numberOfDecimals,str(self.signedValue))
                    break;
                case ModbusCommands::READ_INPUTBITS:
value = readInputBits(modbus_t *ctx, int addr, int nb, uint8_t *dest);
                    value = self.modbus.readHoldingRegValue(self.registerAddress, self.numberOfDecimals, self.signedValue)
                    // MM TODO: update - self.logger.info("ModbusUartDevice: sent command %s, register=%d, numOfDecimals=%d, signed=%s", ModbusCommands.READ_HOLDINGREG.name,self.registerAddress,self.numberOfDecimals,str(self.signedValue))
                    break;
                case ModbusCommands.READ_INPUTREGS:
value = readInputRegs(ctx,0,nb_inputRegs,input_regs);
                    value = self.modbus.readMultiInputRegValues(self.registerAddress, self.numberOfRegs)
                    // MM TODO: update - self.logger.info("ModbusUartDevice: sent command %s, register=%d, numOfRegs=%d", ModbusCommands.READMULTI_INPUTREGS.name,self.registerAddress,self.numberOfRegs)
                    break;
                case ModbusCommands.READ_HOLDINGREGS:
value = readHoldingRegs(ctx,1,nb_holdingRegs-1,holding_regs);
                    value = self.modbus.readMultiHoldingRegValues(self.registerAddress, self.numberOfRegs)
                    // MM TODO: update - self.logger.info("ModbusUartDevice: sent command %s, register=%d, numOfRegs=%d", ModbusCommands.READMULTI_HOLDINGREGS.name,self.registerAddress,self.numberOfRegs)
                    break;
                case ModbusCommands.WRITE_COILBIT:
value = writeCoilBit(modbus_t *ctx, int addr, int status);
                    self.modbus.writeHoldingRegister(self.registerAddress, self.values[0], self.numberOfDecimals, self.signedValue)
                    // MM TODO: update - self.logger.info("ModbusUartDevice: sent command %s, register=%d, value=%d, numberOfDecimals=%d, signed=%s",ModbusCommands.WRITE_HOLDINGREG.name,self.registerAddress,self.values[0],self.numberOfDecimals,str(self.signedValue))
                    break;
                case ModbusCommands.WRITE_HOLDINGREG:
value = writeHoldingReg(ctx,1,95+j++);
                    self.modbus.writeHoldingRegister(self.registerAddress, self.values[0], self.numberOfDecimals, self.signedValue)
                    // MM TODO: update - self.logger.info("ModbusUartDevice: sent command %s, register=%d, value=%d, numberOfDecimals=%d, signed=%s",ModbusCommands.WRITE_HOLDINGREG.name,self.registerAddress,self.values[0],self.numberOfDecimals,str(self.signedValue))
                    break;
                case ModbusCommands.WRITE_COILBITS:
value = writeCoilBits(modbus_t *ctx, int addr, int nb, const uint8_t *src);
                    self.modbus.writeHoldingRegister(self.registerAddress, self.values[0], self.numberOfDecimals, self.signedValue)
                    // MM TODO: update - self.logger.info("ModbusUartDevice: sent command %s, register=%d, value=%d, numberOfDecimals=%d, signed=%s",ModbusCommands.WRITE_HOLDINGREG.name,self.registerAddress,self.values[0],self.numberOfDecimals,str(self.signedValue))
                    break;
                case ModbusCommands.WRITEMULTI_HOLDINGREGS:
value = writeHoldingRegs(ctx,0,3,newholding_regs);
                    self.modbus.writeHoldingRegisters(self.registerAddress, self.values)
                    // MM TODO: update - self.logger.info("ModbusUartDevice: sent command %s, register=%d",ModbusCommands.WRITEMULTI_HOLDINGREGS.name,self.registerAddress)
                    // MM TODO: update - self.logger.info("ModbusUartDevice: Values - %s", str(self.values).strip('[]'))
                    break;
                case ModbusCommands.WRITEREAD_HOLDINGREGS:
value = writeReadHoldingRegs(ctx,0,nb_holdingRegs,newholding_regs,0,nb_holdingRegs,holding_regs);
                    self.modbus.writeHoldingRegisters(self.registerAddress, self.values)
                    // MM TODO: update - self.logger.info("ModbusUartDevice: sent command %s, register=%d",ModbusCommands.WRITEMULTI_HOLDINGREGS.name,self.registerAddress)
                    // MM TODO: update - self.logger.info("ModbusUartDevice: Values - %s", str(self.values).strip('[]'))
                    break;                    
                default:
            }

            if debugMode:
                t1 = time.perf_counter()
                self.logger.debug("sendModbusCommand()[%s]: Modbus library command complete at %f, time to interact with Modbus library is %f ms",str(self.pid),t1,(t1-t0)*1000)

            return value
        }

    }
}

riaps::ComponentBase* create_component(_component_conf& config, riaps::Actor& actor){
    auto result = new RIAPSModbusCReqRepUART::components::comp_modbusUartCReqRepDevice(config, actor);
    return result;
}

void destroy_component(riaps::ComponentBase* comp){
    delete comp;
}