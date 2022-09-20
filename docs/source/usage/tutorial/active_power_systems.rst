.. _tutorial:

....................
Active power systems
....................

The traditional power system shown in the tutorials presenting 
:ref:`Monte Carlo <tutorial_traditional_power_system_monte_carlo>`
and
:ref:`sequential <tutorial_traditional_power_system_monte_carlo>`
simulations types can be expanded with active and smart components.

This page illustrates how these components and features are initialized
and specifies where they must be included in the system definition.

"""""""""""""""""""""""
Active generation units
"""""""""""""""""""""""

Three types of active generations units can be added:

- Production units
- Batteries
- EV parks (Electric vehicle parks)

The active generation units must be initialized before
any network initializations.

In order to add generation units the components need to be imported:

.. literalinclude:: ../../../../relsad/examples/tutorial/active_generation_units.py
   :language: python
   :lines: 3-8
    
The `Table` class must be used to define the amount
of EVs in the EV park as a function of time.
    
Then the active generation units need to be created:

.. literalinclude:: ../../../../relsad/examples/tutorial/active_generation_units.py
   :language: python
   :lines: 12-38


The production unit is placed on bus `B3` and the battery is placed
on bus `B6`.

Here, the EV park is placed in bus `B5` and `num_ev_table` defines a
constant number of ten cars in the EV park throughout the day.
The possibilities of vehicle-to-grid can be decided
using the `v2g_flag`.

Generation can be added to a production unit on the bus:

.. literalinclude:: ../../../../relsad/examples/tutorial/active_generation_units.py
   :language: python
   :lines: 40-43

The generation profile is specified by the variable `generation_profile`.
Here it is defined to provide a constant production of 0.02 MW throughout
the year.
A way of creating generation profiles is shown in :ref:`Load and generation preparation <load_and_generation_preparation>`. 


"""""""""""""""""""""""""
Grid connected microgrids
"""""""""""""""""""""""""

For evaluating a network with a microgrid, an additional network
class needs to be imported:

.. literalinclude:: ../../../../relsad/examples/tutorial/grid_connected_microgrids.py
   :language: python
   :lines: 9

Furthermore, microgrid mode enumeration class needs to be imported
from the *MicrogridController* class:

.. literalinclude:: ../../../../relsad/examples/tutorial/grid_connected_microgrids.py
   :language: python
   :lines: 11

The Microgrid mode is used to specify the produre
the microgrid should follow. 

Then the components in the microgrid can be created:

.. literalinclude:: ../../../../relsad/examples/tutorial/grid_connected_microgrids.py
   :language: python
   :lines: 27-114

After the microgrid components are created, the microgrid
network can be created and the components can be added:

.. literalinclude:: ../../../../relsad/examples/tutorial/grid_connected_microgrids.py
   :language: python
   :lines: 116-122

""""""""""""""""""""""""""""""
Islanded networks (microgrids)
""""""""""""""""""""""""""""""

For evaluating islanded networks or microgrids, the distribution network
or microgrid network can be initiated without an overlying
transmission network. Below is an example of how this is done. Note that
the `connected_line` variable is set to `None` in this case:

.. literalinclude:: ../../../../relsad/examples/tutorial/islanded_networks.py
   :language: python
   :lines: 7-12

"""""""""""""""""""""""""""""""""""
Power system with ideal ICT network
"""""""""""""""""""""""""""""""""""

This section illustrates basic usage of the ICT features implemented in `RELSAD`.
First, we illustrate how to include ICT components without an ICT network.
In this case, the communication between the ICT components is considered
to be ideal, without any probability of failing.

The ICT components must be initialized before
any network initializations.

For including ICT components imported the following:: 

    from relsad.network.components import (
        MainController, 
        Sensor, 
        IntelligentSwitch,
    )

A smart controller is initiated as follows:

.. literalinclude:: ../../../../relsad/examples/tutorial/power_system_with_ideal_ict.py
   :language: python
   :lines: 9

In addition, different failure rates and repair times for the controller
can be specified. 

Intelligent switches are added to disconnectors as shown here:

.. literalinclude:: ../../../../relsad/examples/tutorial/power_system_with_ideal_ict.py
   :language: python
   :lines: 11-14

A failure rate for the intelligent switch can also be specified.
There can only be one intelligent switch on each disconnector. 

A sensor can be added on a line:

.. literalinclude:: ../../../../relsad/examples/tutorial/power_system_with_ideal_ict.py
   :language: python
   :lines: 16-19

Failure rates and repair time of the sensor can be specified.
There can only be on sensor on each line. 


""""""""""""""""""""""""""""""""""""""
Power system with fallible ICT network
""""""""""""""""""""""""""""""""""""""

Second, inclusion of ICT components with an ICT network is shown. In this case,
the communication between the ICT components might fail leading to potential
downtime.

For including an ICT network, the following must be imported:

.. literalinclude:: ../../../../relsad/examples/tutorial/power_system_with_fallible_ict.py
   :language: python
   :lines: 3-7

To add the ICT network, ICT nodes and ICT lines must be defined and added to
a ICT network:

.. literalinclude:: ../../../../relsad/examples/tutorial/power_system_with_fallible_ict.py
   :language: python
   :lines: 13-56

Here, we only initiate a "dummy-network" to illustrate a minimal example
of the ICT network definition. In a real simulation, the network is
much more comprehensive. We refer to the CINELDI example network which is
located in the package source code for a more comprehensive example.
