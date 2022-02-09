This test is an example of how to use qry/ans ports to allow target messages to specific components without creating a unique message for each connection. 

The components in this example are "client" and "server" with the assumption that there are many clients, and the server needs to send targeted messages to them. 

This works by having the many clients send a qry message to the server. If the server records the identity of the client then by selecting a particular client identity before sending the message the sever can send the message directly to a specific client. This works because the qry/ans ports are asynchronous, and the server can send many ans messages in response to the initial qry message.  

The critical code fragment for this example is in `server.py` in the `on_ans_port` function.

```
self.peer_list[msg["name"]] = self.ans_port.identity
```

Whenever a message is received on an ans port the identity property is set. This is because qry/ans is based on Dealer/Router ZeroMQ socket types. From the 0MQ [documentation](https://zeromq.org/socket-api/): 

"The ROUTER socket type talks to a set of peers, using explicit addressing so that each outgoing message is sent to a specific peer connection. ROUTER works as an asynchronous replacement for REP, and is often used as the basis for servers that talk to DEALER clients.

When receiving messages a ROUTER socket will **prepend a message part containing the routing id of the originating peer to the message before passing it to the application**. Messages received are fair-queued from among all connected peers. When sending messages a ROUTER socket will remove the first part of the message and use it to determine the routing id of the peer the message shall be routed to. If the peer does not exist anymore, or has never existed, the message shall be silently discarded."

We record the routing id of the peer in a `peer_list` for later messaging. 

We set the peer in `server.py` in the `on_poller` function, and send the targeted message. 

```
self.ans_port.identity = self.peer_list[peer]
self.ans_port.send_pyobj(msg)
```
