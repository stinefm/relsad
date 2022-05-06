=======================================
Load and Generation unit implementation
=======================================

.....................................
Implementation of load
.....................................

In RELSAD, a load can be set on each bus. The load can either be set as a constant load or a time varied load. For time varied loads, the load can be allocated to the bus through an array containing the load for each time increment (see Referer til funksjon... :API:`/network/components/Bus`). The package allows user-defined time increments and the user can set a start and an end time. If the load array varies from the user-specified time increment, the load data will be interpolated to fit the wanted time increment. 

RELSAD supports the inclusion of multiple load types and the specific interruption cost related to the different customer categories. The specific inturrption cost can be added in order to calculate the Cost of Energy Not Supplied in the system (default value for the specific interruption cost is set to 1). 
In addition, multiple different load types can be added to a bus, making the bus able to have different customer categories connected. 

.. 
    the specific interruption cost for each customer category can be included for calculating the Cost of Energy Not Supplied in the system. 







.....................................
Implementation of generation units
.....................................


In RELSAD, the generation units are implemented generic, which means that the package does to consider which type of generation unit that is generating power, only the amount of generated power. 

Similar to the implementation of load, the amount of generation from a generation unit at a bus can either be constant or time varied. For time varied generation, the generation from a unit can be added through an array (see referer). Equal as for setting the load, the generation array can be interpolated to fit the wanted time increment if the generation array deviates. 