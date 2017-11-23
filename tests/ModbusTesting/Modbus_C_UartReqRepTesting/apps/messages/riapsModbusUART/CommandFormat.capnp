@0xa080f41ab7f77d1e;
using Cxx = import "/capnp/c++.capnp";
$Cxx.namespace("riapsModbusUART");

struct CommandFormat
{
    commandType @0: Int16;
    registerAddress @1: Int16;
    numberOfRegs @2: Int16;
    values @3: List(Int16);
    wreadRegAddress @4: Int16;
    wreadNumOfRegs @5: Int16;
}
