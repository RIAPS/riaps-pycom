cmake_minimum_required(VERSION 3.0)
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_CXX_FLAGS "-std=c++11")
set(CMAKE_C_FLAGS "-std=c99")
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/build/${ARCH}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY  ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})
#Library Dependencies
set(DEPENDENCIES ${RIAPS_PREFIX})
set (LIBALLPATH_INCLUDE ${DEPENDENCIES}/include)
set (LIBALLPATH_LIB ${DEPENDENCIES}/lib)
link_directories(${LIBALLPATH_LIB})
include_directories(${CMAKE_SOURCE_DIR}//messages-gen)
include_directories(${CMAKE_SOURCE_DIR}/cpp/include)

# Generating the headers and cpp for message edu.vanderbilt.riaps.app.impl.FStructTypeImpl@5a3f7ab (name: TempDatatype)
add_custom_command(OUTPUT  "${CMAKE_SOURCE_DIR}/messages-gen/TempDatatype.capnp.c++"
				   DEPENDS "${CMAKE_SOURCE_DIR}/messages-gen/TempDatatype.capnp" 
				   WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}//messages-gen"  
				   COMMAND ${CMAKE_COMMAND} -E env "PATH=/opt/riaps/amd64/bin" capnp compile -oc++ "${CMAKE_SOURCE_DIR}/messages-gen/TempDatatype.capnp" --import-path="${CMAKE_SOURCE_DIR}//messages-gen"
				   )

# Creating Libraries for Component edu.vanderbilt.riaps.app.impl.ComponentImpl@7e48abdf (name: TempMonitor) (language: python, realtime: false)
add_library(TempMonitor 
			SHARED ${CMAKE_CURRENT_SOURCE_DIR}/cpp/TempMonitor.cc
			${CMAKE_CURRENT_SOURCE_DIR}/cpp/TempMonitorBase.cc
			${CMAKE_SOURCE_DIR}/messages-gen/TempDatatype.capnp.c++
			)
			
target_link_libraries(TempMonitor czmq riaps dl capnp kj)
install(TARGETS TempMonitor DESTINATION lib)

# Creating Libraries for Component edu.vanderbilt.riaps.app.impl.ComponentImpl@450e9c6f (name: TempSensor) (language: python, realtime: false)
add_library(TempSensor 
			SHARED ${CMAKE_CURRENT_SOURCE_DIR}/cpp/TempSensor.cc
			${CMAKE_CURRENT_SOURCE_DIR}/cpp/TempSensorBase.cc
			${CMAKE_SOURCE_DIR}/messages-gen/TempDatatype.capnp.c++
			)
			
target_link_libraries(TempSensor czmq riaps dl capnp kj)
install(TARGETS TempSensor DESTINATION lib)

