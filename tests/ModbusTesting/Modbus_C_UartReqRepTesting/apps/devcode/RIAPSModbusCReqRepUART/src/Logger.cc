#include <Logger.h>

namespace riapsmodbuscreqrepuart {
   namespace components {
      
      Logger::Logger(_component_conf_j &config, riaps::Actor &actor) :
      LoggerBase(config, actor) {
      }
      
      void Logger::OnRx_modbusData(const riapsModbusUART::LogData::Reader &message,
      riaps::ports::PortBase *port)
      {
         std::cout << "Logger::OnRx_modbusData(): " << std::endl;
      }
      
      void Logger::OnOneShotTimer(const std::string& timerid){
         
      }
      
      Logger::~Logger() {
         
      }
   }
}

riaps::ComponentBase *create_component(_component_conf_j &config, riaps::Actor &actor) {
   auto result = new riapsmodbuscreqrepuart::components::Logger(config, actor);
   return result;
}

void destroy_component(riaps::ComponentBase *comp) {
   delete comp;
}
