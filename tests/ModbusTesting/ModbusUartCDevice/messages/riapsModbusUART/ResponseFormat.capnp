@0xac3fa4cf20cb4a08;
using Cxx = import "/capnp/c++.capnp";
$Cxx.namespace("riapsModbusUART");

struct ResponseFormat
{
    commandType @0: Int16;
    registerAddress @1: Int16;
    numberOfRegs @2: Int16;
    values @3: List(Int16);
}
