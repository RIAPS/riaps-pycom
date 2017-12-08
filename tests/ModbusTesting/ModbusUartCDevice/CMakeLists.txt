cmake_minimum_required(VERSION 3.8)
project(modbusuartdevice)

option(arch "amd64/armhf" "amd64")
option(BUILD_TESTS  "Build tests" ON)
set(CMAKE_SYSTEM_NAME Linux)

set(riaps_prefix "/opt/riaps/" CACHE STRING "the riaps prefix")

#Set the platform
if (${arch} STREQUAL "armhf")
    set(TOOLCHAIN_PREFIX arm-linux-gnueabihf)
    set(CMAKE_C_COMPILER ${TOOLCHAIN_PREFIX}-gcc)
    set(CMAKE_CXX_COMPILER ${TOOLCHAIN_PREFIX}-g++)
    set(CMAKE_FIND_ROOT_PATH /usr/${TOOLCHAIN_PREFIX})
    set (CMAKE_CXX_FLAGS "-std=c++11 -g")
    set (CMAKE_C_FLAGS "-std=c99 -g")
else()
    set(CMAKE_C_COMPILER gcc-5)
    set(CMAKE_CXX_COMPILER g++-5)
    set(CMAKE_CXX_FLAGS "-std=c++11 -D_GLIBCXX_USE_CXX11_ABI=0")
    set (CMAKE_C_FLAGS "-std=c99")
endif()

set(CMAKE_INSTALL_PREFIX ${riaps_prefix}/${arch})

set(DEPENDENCIES ${riaps_prefix})
set (LIBALLPATH_INCLUDE ${DEPENDENCIES}/${arch}/include)
set (LIBALLPATH_LIB ${DEPENDENCIES}/${arch}/lib)
include_directories(${LIBALLPATH_INCLUDE})
link_directories(${LIBALLPATH_LIB})

include_directories(include)
include_directories(include/base)
include_directories(messages)

list(APPEND device_HEADERS
        include/base/ModbusUARTBase.h
        include/ModbusUART.h
        include/SerialModbusComm.h
        messages/modbusuart.capnp.h
        )

list(APPEND device_SOURCE
        src/base/ModbusUARTBase.cc
        src/ModbusUART.cc
        src/SerialModbusComm.cc
        messages/modbusuart.capnp.c++
        )

add_library(modbusuart SHARED
        ${device_HEADERS}
        ${device_SOURCE}
        )

target_link_libraries(modbusuart modbus riaps)

#set(pybind11_DIR /usr/local/include/pybind11)
#find_package(pybind11 REQUIRED)
#include_directories(/usr/include/python3.5m)
#set(PYBIND11_CPP_STANDARD -std=c++11)
#
#pybind11_add_module(riapsmodbusuartpy SHARED
#        ${device_HEADERS}
#        ${device_SOURCE}
#        )
#
#target_link_libraries(riapsmodbusuartpy PUBLIC pybind11::module
#                                      PRIVATE modbus
#                                      PRIVATE riaps)