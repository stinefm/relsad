=========================================================
Implementation of electric vehicles and vehicle to grid
=========================================================

An electric vehicle (EV) is modeled as a battery (see :ref:`battery_behavior`) with drawn SOC.
The functionality of the *EVPark* class is to aggregate the EVs at a bus into an EV park for each bus in the system. The amount of EVs on a bus can be specified by the user. 
An EV park is modeled to build up an aggregated battery solution with the available EVs specified on each bus in the system. The EV park contains information on the amount of EVs in the park and the SOC level on each EV. This information is used to make the EV park where the available power in the EV park is aggregated based on the EVs and the SOC level of the EVs in the park.

The user can specify if vehicle to grid should be activated or not for the EVs. If vehicle to grid is activated the EV park can charge and discharge the cars equal to a battery. If vehicle to grid is not activated, only charging the EVs in the EV park is possible. 