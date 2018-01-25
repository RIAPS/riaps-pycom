#include <TempSensor.h>

namespace weathermonitor {
   namespace components {
      
      TempSensor::TempSensor(_component_conf &config, riaps::Actor &actor) :
      TempSensorBase(config, actor) {
      }
      
      void TempSensor::OnClock(riaps::ports::PortBase *port) {
         std::cout << "TempSensor::OnClock(): " << port->GetPortName() << std::endl;
      }
      
      
      void TempSensor::OnGroupMessage(const riaps::groups::GroupId& groupId,
      capnp::FlatArrayMessageReader& capnpreader, riaps::ports::PortBase* port){
         
      }
      
      TempSensor::~TempSensor() {
         
      }
   }
}

riaps::ComponentBase *create_component(_component_conf &config, riaps::Actor &actor) {
   auto result = new weathermonitor::components::TempSensor(config, actor);
   return result;
}

void destroy_component(riaps::ComponentBase *comp) {
   delete comp;
}
