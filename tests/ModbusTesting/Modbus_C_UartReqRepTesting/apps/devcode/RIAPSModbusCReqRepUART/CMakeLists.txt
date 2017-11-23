#Initial Setup		
cmake_minimum_required(VERSION 3.0)
project (RIAPSModbusCReqRepUART)

set(CMAKE_SYSTEM_NAME Linux)
set (CMAKE_CXX_FLAGS "-std=c++11")
set (CMAKE_C_FLAGS "-std=c99")


set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/${ARCH}/bin)		
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/${ARCH}/bin)		
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY  ${CMAKE_CURRENT_SOURCE_DIR}/${ARCH}/bin)

#Library Dependencies
set(DEPENDENCIES ${RIAPS_PREFIX})
set (LIBALLPATH_INCLUDE ${DEPENDENCIES}/include)
set (LIBALLPATH_LIB ${DEPENDENCIES}/lib)
link_directories(${LIBALLPATH_LIB})


#include directories
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)

		

#capnproto files		
add_custom_command(OUTPUT  "${CMAKE_SOURCE_DIR}/messages/riapsModbusUART/LogData.capnp.c++"
                   DEPENDS "${CMAKE_SOURCE_DIR}/messages/riapsModbusUART/LogData.capnp" 
                   WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}/messages"  
                   COMMAND capnp compile -oc++ "${CMAKE_SOURCE_DIR}/messages/riapsModbusUART/LogData.capnp" --import-path="${CMAKE_SOURCE_DIR}/messages"
                   )
add_custom_command(OUTPUT  "${CMAKE_SOURCE_DIR}/messages/riapsModbusUART/ResponseFormat.capnp.c++"
                   DEPENDS "${CMAKE_SOURCE_DIR}/messages/riapsModbusUART/ResponseFormat.capnp" 
                   WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}/messages"  
                   COMMAND capnp compile -oc++ "${CMAKE_SOURCE_DIR}/messages/riapsModbusUART/ResponseFormat.capnp" --import-path="${CMAKE_SOURCE_DIR}/messages"
                   )
add_custom_command(OUTPUT  "${CMAKE_SOURCE_DIR}/messages/riapsModbusUART/CommandFormat.capnp.c++"
                   DEPENDS "${CMAKE_SOURCE_DIR}/messages/riapsModbusUART/CommandFormat.capnp" 
                   WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}/messages"  
                   COMMAND capnp compile -oc++ "${CMAKE_SOURCE_DIR}/messages/riapsModbusUART/CommandFormat.capnp" --import-path="${CMAKE_SOURCE_DIR}/messages"
                   )

#component libraries

# ComputationalComponent
add_library(computationalcomponent 
			SHARED src/ComputationalComponent.cc
			${CMAKE_SOURCE_DIR}/basecode/RIAPSModbusCReqRepUART/src/ComputationalComponentBase.cc
			${CMAKE_SOURCE_DIR}/messages/riapsModbusUART/LogData.capnp.c++
			${CMAKE_SOURCE_DIR}/messages/riapsModbusUART/ResponseFormat.capnp.c++
			${CMAKE_SOURCE_DIR}/messages/riapsModbusUART/CommandFormat.capnp.c++
			)
			
target_link_libraries(computationalcomponent czmq riaps dl capnp kj )

# Logger
add_library(logger 
			SHARED src/Logger.cc
			${CMAKE_SOURCE_DIR}/basecode/RIAPSModbusCReqRepUART/src/LoggerBase.cc
			${CMAKE_SOURCE_DIR}/messages/riapsModbusUART/LogData.capnp.c++
			)
			
target_link_libraries(logger czmq riaps dl capnp kj )
