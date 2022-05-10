.. _load_and_production_generation:

=====================================
Load and production generation
=====================================

There exsist multiple methods to generate and collect load and genereation data. Here, some examples for generating load profiles and generation data from wind and solar power are illustrated. 


.....................................
Load profile generator
.....................................

The load profiles used in the examples presented in RELSAD are generated based on specifications from *FASIT Kravspesifikasjon* (requirements specification) :cite:`FASIT`. The load profiles are given for different load customer categories, time of day, low and high load, and if it is a weekday or weekend. The dataset used in the profiles can be seen in :download:`this file <../../../examples/data/load_profiles_fasit.csv>`.

The load profiles are calculated as

.. math::
    :label: eq:loadprofile

    P_{load} = A_{i, t}T+B_{i,t}

here, :math:`A_{i,t}` is the A parameter from the dataset for load category *i* at time *t*, :math:`T` is the temperature in degrees, and :math:`B_{i,t}` is the B parameter from the dataset for load category *i* at time *t*. 

The temperatures are collected from weather data at Rygge in Norway and can be seen :download:`this file <../../../examples/data/weather_data_rygge.csv>`. 

The dataset has an hourly resolution. 

.....................................
Wind power generator
.....................................

Wind power data can be generated from the power curve of a specific wind turbine. Figure LEGG INN FIGUR, illustrates a typical idealized power curve for a wind turbine. From the cut-in wind speed :math:`V_{C}` until the rated wind speed :math:`V_{R}`, the delivered power will increase for increased wind speed. After :math:`V_{R}`, the wind turbine is not able to give more power for increased wind speed due to generator limitations. When the wind speed reaches the cut-out wind speed :math:`V_{F}`, the wind is too strong for the wind turbine and the rotor shaft is locked so that no power can be produced. The power curve differs for different types of wind turbines. 

From the power curve, the produced power can be calculated with the use of wind speed data. For a given wind speed :math:`v_{i}`, the output power :math:`P_{i}` can be estimated based on interpolation for wind speeds between :math:`V_{C}` and :math:`V_{R}` for the analyzed wind turbine. Legg inn figur, see figure

.. math::
    :label: eq:windpower

    P_{i} = P_{i-1} + (P_{i+1} - P_{i-1})\frac{(v_{i}-v_{i-1})}{(v_{i+1}-v_{i-1})} 

where :math:`P_{i-1}` is the rated power of the wind turbine for wind speed :math:`v_{i-1}` and :math:`P_{i+1}` is the rated power of the wind turbine for wind speed :math:`v_{i+1}`. The wind speed :math:`v_{i-1}` is the closest lower wind speed with data from :math:`v_{i}` while :math:`v_{i+1}` is the closest higher wind speed with data from :math:`v_{i}`. 

The wind speed :math:`v_{i}` at the height of the wind turbine can be calculated by using wind speed data from a weather station that measures wind speed at a given height


.. math::
    :label: eq:windvelocity

    v_{i} = v_{0}(\frac{H}{H_{0}})^{\alpha}

where :math:`v_{0}` is the wind speed from the weather station at height :math:`H_{0}`, :math:`H` is the height of the wind turbine, and :math:`\alpha` is the friction coefficient of the terrain where the wind turbine is placed. 


.....................................
Solar power generator
.....................................

Solar power data can be generated based on the fill factor power model :cite:`jones2002modelling`. The fill factor approach uses the relationship between the irradiance and the cell temperature with the open circuit voltage, :math:`V_{oc}`, and short circuit current, :math:`I_{sc}`, to calculate the maximum power output of a solar module. 
The maximum power output of a solar module is 

.. math::
    :label: eq:PoutPV

    P_{out} = FF \cdot I_{sc} \cdot \frac{E}{E_{0}} \cdot V_{oc} \cdot \frac{ln(K \cdot E)}{ln(K \cdot E_{0})} \cdot \frac{T_{0}}{T_{cell}}

where :math:`E` is the irradiance at the moment, :math:`E_{0}` is the standard irradiance (1000 :math:`W/m^{2}` ), and :math:`T_{0}` is the reference temperature or standard module temperature (298 K).

The fill factor, :math:`FF`, is  

.. math::
    :label: eq:fillfactor

    \text{FF} = \frac{P_{mpp}}{(V_{oc}I_{sc})}

where the maximum power output :math:`P_{mpp}` can be calculated as   

.. math::
    :label: eq:maxpowerpoint

    P_{mpp} = V_{mpp}I_{mpp}

here, :math:`V_{mpp}` and :math:`I_{mpp}` is the maximum power point votlage and current, respectively.

The cell temperature of a solar module is calculated as 

.. math::
    :label: eq:Tcell

    T_{cell} = T+(\frac{\text{NOCT}-20}{800})S

where :math:`T` is the air temperature, :math:`NOCT` is the nominal operating cell temperature in degrees, and :math:`S` is the solar insolation in :math:`W/m^{2}`. 

In the end, :math:`K` represent a constant term 


.. math::
    :label: eq:Kconstantterm

    K = \frac{I_{sc}}{E_{0}I_{0}}

where :math:`I_{0}` is the saturated current for the diode. 

The AC output power from a PV array with an inverter efficiency :math:`\eta_{inv}`, can be calculated as

.. math::
    :label: eq:Kconstantterm

    P_{out, AC} = P_{out}N_{m}\eta_{inv}

where :math:`N_{m}` is the number of modules in the array. 