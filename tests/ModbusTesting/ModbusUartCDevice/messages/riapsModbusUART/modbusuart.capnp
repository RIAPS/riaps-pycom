@0x882e1c0f1af44d05;
using Cxx = import "/capnp/c++.capnp";
$Cxx.namespace("riapsModbusUART");

enum ModbusCommands {
    noCmd @0;
    readCoilBits @1;
    readInputBits @2;
    readInputRegs @3;
    readHoldingRegs @4;
    writeCoilBit @5;
    writeHoldingReg @6;
    writeCoilBits @7;
    writeMultiHoldingRegs @8;
    writeReadHoldingRegs @9;
}

struct CommandFormat
{
    commandType @0: ModbusCommands;
    registerAddress @1: Int16;
    numberOfRegs @2: Int16;
    values @3: List(Int16);
    wreadRegAddress @4: Int16;
    wreadNumOfRegs @5: Int16;
}

struct ResponseFormat
{
    commandType @0: ModbusCommands;
    registerAddress @1: Int16;
    numberOfRegs @2: Int16;
    values @3: List(Int16);
}
