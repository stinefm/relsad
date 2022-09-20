.. _tutorial_traditional_power_system_sequential:

....................................
Traditional power system, Sequential
....................................

Here we present how to run a small sequential
simulation of the behavior of the network presented in the
:ref:`system setup <tutorial_traditional_power_system_setup>`
section to illustrate how `RELSAD` can be used.


.. include:: system.rst

"""""""""""""""""""""
Sequential simulation
"""""""""""""""""""""

To run a sequential simulation the user must specify:

* Simulation start time, `start_time`
* Simulation stop time, `stop_time`
* Time step, `time_step`
* Time unit presented in results, `time_unit`
* A callback function, `callback`
* Saving directory for results, `save_dir`
  

.. literalinclude:: ../../../../../relsad/examples/tutorial/sequential.py
   :language: python
   :lines: 6-37

Here we used the callback function to specify that line `L2` and
`L6` will fail at the start of the simulation, while line `L3` will fail
after two hours. The callback function enables easy customization
and implementation of scenarios of interest.

To run a deterministic sequential simulation the user must set
all failure rates to zero and all repair times to constant values.
Otherwise, the simulation will exhibit a stochastic behavior.

Here we plot `ENS` (Energy Not Supplied) for the power system:

.. literalinclude:: ../../../../../relsad/examples/tutorial/sequential.py
   :language: python
   :lines: 39-59
    
The plot should look like this:

.. figure:: ../../../_static/figures/tutorial/traditional_power_system/sequential/ENS.png
   :width: 800
   :alt: ENS.
   
   ENS
