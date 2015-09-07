'''
nodula -- Project Nodula model -- Data Model

This module describes the underlying data module of Nodula.

Nodula is implemented as a directed graph; this graph contains Pins, whose
relationships form the edges (namely, the subclasses Plug, an output Pin, and
Socket, an input Pin), as well as obviously-named Nodes. These Nodes represent
units of work or processing, taking in some values on its input Sockets and
producing some values on its output Plugs. To this end, the Node is "ticked"
with its .Tick() method.

Actually running and scheduling a graph of Nodes is done through the Simulator.
The Simulator (through its derivatives) makes all decisions regarding when to
schedule nodes (namely, .Tick() them) and when to advance data through the
connections of the Pins (see particularly Plug.Advance() and Plug.IsSet()).
These decisions are quite important; they impact how data flows through the
graph, what happens when it bottlenecks, and whether or not Nodes may see unset
(default) data. Refer to specific subclasses for details.  It also conveniently
acts as a place to store data which is global to a graph.
'''
