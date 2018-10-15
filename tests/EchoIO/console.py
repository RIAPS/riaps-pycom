#!/usr/bin/python3
# Console script 
# Connects to a server on port, reads from stdin, sends string EchoIO.IODevice, prints reply

import zmq
import sys

port = "9876"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

context = zmq.Context()
print ("Connecting to server...")
socket = context.socket(zmq.REQ)    # Must be REQ port (EchoIO.IODevice has the REP port)
socket.connect ("tcp://localhost:%s" % port)
    
while True:
    msg = input("> ")
    socket.send_pyobj(msg)
    rsp = socket.recv_pyobj()
    print("< %s" % rsp)
