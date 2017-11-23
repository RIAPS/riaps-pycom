@0xc07dd021227dcb3c;
using Cxx = import "/capnp/c++.capnp";
$Cxx.namespace("riapsModbusUART");

struct LogData
{
    logMsg @0: Text;
}
