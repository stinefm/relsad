======================
Switches
======================

There are three type of switches that are implemented in RELSAD. Here, some information about the switches is provided.

................
Circuit breaker
................

A circuit breaker is an electrical safety switch that is used to disconnect parts of the system to protect equipment from damage and prevent risks in relation to overcurrent or short circuits. The circuit breaker will automatically react when an unwanted event happens in the system to disconnect the system. The breaker can be reset when the unwanted event is cleared. 

In RELSAD, when a failure occurs, the closest circuit breaker to the failure will react and disconnect the system until the failure is isolated. The time it takes from the occurrence of a failure until the failure is isolated, and the circuit breaker is reset, is called *sectioning time* and can be set by the user. 

..............
Disconnector
..............

A disconnector is a switch that is used to disconnect sections of the system and breaks the circuit. They can either be manually or automatically operated. The placement of the disconnectors decides the division of sections of a system. In a radially operating system, all load points downstream of a disconnector will be isolated when the disconnector is opened. 

In RELSAD, the disconnectors can be placed on any line segment in the system, and the system sections are allocated based on the placement of the disconnectors. These are used to disconnect and connect line segments and isolate downstream failures in the system. 


..................
Intelligent switch
..................

In RELSAD, intelligent switches are implemented to make the system more automated. The intelligent switch objects can be placed on disconnectors in the system and by that be used to automatically control the disconnectors. An intelligent switch can receive commands about the switch position from a controller and automatically open/close the switch.h. 