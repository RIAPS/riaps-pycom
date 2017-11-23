cmake_minimum_required(VERSION 3.0)
include_directories(${CMAKE_SOURCE_DIR}/messages/)
include_directories(${CMAKE_SOURCE_DIR}/basecode/RIAPSModbusCReqRepUART/include)		
add_subdirectory(devcode/RIAPSModbusCReqRepUART)
