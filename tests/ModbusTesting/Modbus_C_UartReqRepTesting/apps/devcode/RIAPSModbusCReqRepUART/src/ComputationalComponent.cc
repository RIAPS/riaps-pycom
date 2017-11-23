#include <ComputationalComponent.h>

namespace riapsmodbuscreqrepuart {
   namespace components {
      
      ComputationalComponent::ComputationalComponent(_component_conf_j &config, riaps::Actor &actor) :
      ComputationalComponentBase(config, actor) {
      }
      
      void ComputationalComponent::OnClock(riaps::ports::PortBase *port) {
         std::cout << "ComputationalComponent::OnClock(): " << port->GetPortName() << std::endl;
      }
      
      
      
      void ComputationalComponent::OnOneShotTimer(const std::string& timerid){
         
      }
      
      ComputationalComponent::~ComputationalComponent() {
         
      }
   }
}

riaps::ComponentBase *create_component(_component_conf_j &config, riaps::Actor &actor) {
   auto result = new riapsmodbuscreqrepuart::components::ComputationalComponent(config, actor);
   return result;
}

void destroy_component(riaps::ComponentBase *comp) {
   delete comp;
}
