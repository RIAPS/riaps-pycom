/* 
 * Testing Routine for C wrapper around libmodbus library
 */

#include <iostream>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include "time_macros.h"  // MM TODO:  this is here for timing purposes only, remove when done
#include "serialModbusComm.h"
//#include <pybind11/pybind11.h>

//namespace py = pybind11;

/*
 * PYBIND11_MODULE(cpp_test, m) {
m.doc() = "cpp test module";
m.def("ztest", &ztest, "cpp thread w/ zmq test");
}
 */

// For testing
int main ()
{
    std::string portname;
    int baudrate = 115200;
    int bytesize = 8;
    char parity = 'N';
    int stopbits = 1;
    bool portOpen = false;
    int slaveAddress = 10;
    int serialMode = 0;    // for RS232
    modbus_t *ctx;
    int nb_holdingRegs = 3;
    int nb_inputRegs = 4;
    const int n_loop = 100;
    uint16_t *holding_regs;
    uint16_t *input_regs;
    std::string udevice ("/dev/ttyO2");
    struct serial_port_config testPortConfig={udevice,115200,8,'N',1};


    holding_regs = (uint16_t *) malloc(nb_holdingRegs * sizeof(uint16_t));
    memset(holding_regs, 0, nb_holdingRegs * sizeof(uint16_t));
    input_regs = (uint16_t *) malloc(nb_inputRegs * sizeof(uint16_t));
    memset(input_regs, 0, nb_inputRegs * sizeof(uint16_t));

    struct timespec resolution={0,0};
    int result= clock_getres(CLOCK_MONOTONIC, & resolution);
    if(result!=0)
    {
        std::cout<<"error occurred "<<strerror(errno)<<std::endl;
        exit(errno);
    }

    struct timespec preobservations[n_loop];
    struct timespec postobservations[n_loop];

    //0 it out. can do with memzero as well.
    for(int i=0;i<n_loop;i++)
    {
        preobservations[i].tv_nsec=0;
        preobservations[i].tv_sec=0;
        postobservations[i].tv_nsec=0;
        postobservations[i].tv_sec=0;
    }

    // Start Modbus
    ctx = startRTUModbus(testPortConfig,slaveAddress,serialMode);

    if(isModbusReady()){
        for(int i=0;i<n_loop;i++)
        {
            clock_gettime(CLOCK_MONOTONIC,&preobservations[i]);

            readHoldingRegs(ctx,0,nb_holdingRegs,holding_regs);

            clock_gettime(CLOCK_MONOTONIC,&postobservations[i]);
        }

        //calculate time error
        for(int i=0;i<n_loop;i++)
        {
            system_timespec result;
            system_time_sub(&postobservations[i],&preobservations[i],&result);
            std::cout<<"tv.sec="<<result.tv_sec<<" tv_nsec="<<((double)result.tv_nsec)/NSEC_PER_SEC<<std::endl;
        }
    }
}
