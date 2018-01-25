#include <TempMonitor.h>

namespace weathermonitor {
   namespace components {
      
      TempMonitor::TempMonitor(_component_conf &config, riaps::Actor &actor) :
      TempMonitorBase(config, actor) {
      }
      
      void TempMonitor::OnTempupdate(const TempDatatype::Reader &message,
      riaps::ports::PortBase *port)
      {
         std::cout << "TempMonitor::OnTempupdate(): " << std::endl;
      }
      
      void TempMonitor::OnGroupMessage(const riaps::groups::GroupId& groupId,
      capnp::FlatArrayMessageReader& capnpreader, riaps::ports::PortBase* port){
         
      }
      
      TempMonitor::~TempMonitor() {
         
      }
   }
}

riaps::ComponentBase *create_component(_component_conf &config, riaps::Actor &actor) {
   auto result = new weathermonitor::components::TempMonitor(config, actor);
   return result;
}

void destroy_component(riaps::ComponentBase *comp) {
   delete comp;
}
