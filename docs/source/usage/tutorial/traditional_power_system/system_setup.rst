.. _tutorial_traditional_power_system_setup:

......................................
Traditional power system, system setup
......................................

Here we present the creation of a small example network in `RELSAD`.
The network consists of 6 buses and 6 lines,
where one of the lines is a backup line. We introduce simplified
loads.

"""""""
Imports
"""""""

To create a power system the necessary imports need to be added. 

We will make use of `os <https://docs.python.org/3/library/os.html>`_, 
`numpy <https://numpy.org/doc/stable/index.html>`_, 
`pandas <https://pandas.pydata.org/>`_ and 
`matplotlib <https://matplotlib.org/>`_ 
in this tutorial:

.. literalinclude:: ../../../../../relsad/examples/tutorial/system.py
   :language: python
   :lines: 13-16

For importing components from `RELSAD`:

.. literalinclude:: ../../../../../relsad/examples/tutorial/system_components.py
   :language: python
   :lines: 1-7

For importing systems and networks from `RELSAD`:

.. literalinclude:: ../../../../../relsad/examples/tutorial/system.py
   :language: python
   :lines: 3-7

To run time dependent simulations, the time utilities of `RELSAD`
must be imported:

.. literalinclude:: ../../../../../relsad/examples/tutorial/system_components.py
   :language: python
   :lines: 8-12

Adding statistical distribution for, for example, outage time of
components, is done by using the statistical distribution utilities
of `RELSAD`, which needs to be imported:

.. literalinclude:: ../../../../../relsad/examples/tutorial/system_components.py
   :language: python
   :lines: 13-17

The statistical distribution utilities of `RELSAD` enables a variety of custom distributions, including normal and uniform distributions.

To prioritize the bus loadings during outages, the user may define
cost functions that can be related to chosen buses. To use this feature,
the `CostFunction` class must be imported:

.. literalinclude:: ../../../../../relsad/examples/tutorial/system.py
   :language: python
   :lines: 9

To plot the network topology, we import the `plot_topology` function:

.. literalinclude:: ../../../../../relsad/examples/tutorial/system.py
   :language: python
   :lines: 11

The `Simulation` class must be imported to be able to run simulations:

.. literalinclude:: ../../../../../relsad/examples/tutorial/sequential.py
   :language: python
   :lines: 3


"""""""""""""""""
Create components
"""""""""""""""""

First, we create the components for our system.

Creating buses:

.. literalinclude:: ../../../../../relsad/examples/tutorial/system_components.py
   :language: python
   :lines: 20-57

Creating lines:

.. literalinclude:: ../../../../../relsad/examples/tutorial/system_components.py
   :language: python
   :lines: 59-138

Creating circuit breaker:

.. literalinclude:: ../../../../../relsad/examples/tutorial/system_components.py
   :language: python
   :lines: 140-143

Creating disconnectors::
    
Disconnectors can be added to the lines in the system.
A line can have zero, one or two disconnectors connected.
In this example, we add several disconnectors for each line.
If a circuit breaker is placed on a line, can also have two disconnectors:

.. literalinclude:: ../../../../../relsad/examples/tutorial/system_components.py
   :language: python
   :lines: 145-206

"""""""""""""""""""""""
Initialize power system
"""""""""""""""""""""""

For systems without ICT, a manual main controller is added with a name and a desired sectional time:

.. literalinclude:: ../../../../../relsad/examples/tutorial/system_components.py
   :language: python
   :lines: 208

Then the power system is created:

.. literalinclude:: ../../../../../relsad/examples/tutorial/system.py
   :language: python
   :lines: 37


"""""""""""""""
Create networks
"""""""""""""""

After creating the components in the network, the components need to
be added to their associated networks and the associated networks must
be added to the power system. 
First, the bus connecting to the overlying network
(often transmission network) is added.
In this case the overlying network is a transmission network,
which is created by:
    
.. literalinclude:: ../../../../../relsad/examples/tutorial/system.py
   :language: python
   :lines: 39-42

The distribution network contains the rest of the components,
and links to the transmission network with line L1.
This is done by the following code snippet: 

.. literalinclude:: ../../../../../relsad/examples/tutorial/system.py
   :language: python
   :lines: 44-49


""""""""""""""""""
Visualize topology
""""""""""""""""""

To validate the network topology, it can be plotted in the following way:

.. literalinclude:: ../../../../../relsad/examples/tutorial/system.py
   :language: python
   :lines: 51-61

The plot should look like this:

.. figure:: ../../../_static/figures/tutorial/traditional_power_system/CINELDI_testnetwork.png
   :width: 800
   :alt: Test network.
   
   Test network 


"""""""""""""""""""
Load and generation
"""""""""""""""""""

In :ref:`Load and generation preparation <load_and_generation_preparation>`,
examples of how to generate load and generation profiles are provided. 
The generated profiles can be used to set the load and generation
on the buses in the system. 
The load and generation profiles can then be added to the
buses in the system. 

For illustration purposes, we defines some constant loads in this tutorial:
    
.. literalinclude:: ../../../../../relsad/examples/tutorial/system.py
   :language: python
   :lines: 19

We refer to the example simulations for more realistic load handling.


In addition, a cost related to the load can be added to the bus.
For generating the specific interruption cost for a load category:

.. literalinclude:: ../../../../../relsad/examples/tutorial/system.py
   :language: python
   :lines: 21-24

Load and cost can be added to the buses:

.. literalinclude:: ../../../../../relsad/examples/tutorial/system.py
   :language: python
   :lines: 26-34
