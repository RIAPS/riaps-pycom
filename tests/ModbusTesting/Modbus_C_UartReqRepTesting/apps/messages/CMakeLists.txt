cmake_minimum_required(VERSION 3.0)
file(GLOB_RECURSE CAPNP_SRCS     RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} *.capnp)
SET(messagesrc "")
foreach(capnpfile ${CAPNP_SRCS})
  message (${capnpfile})
  LIST(APPEND messagesrc "${capnpfile}.c++" "${capnpfile}.h")
  add_custom_command(OUTPUT  "${capnpfile}.c++" "${capnpfile}.h" DEPENDS "${capnpfile}" WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"  COMMAND capnp compile -oc++ "${capnpfile}" --import-path="${CMAKE_CURRENT_SOURCE_DIR}")
endforeach(capnpfile)

add_custom_target(
    messages ALL
    DEPENDS ${messagesrc}
    )
