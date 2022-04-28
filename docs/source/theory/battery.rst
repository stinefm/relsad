======================
Battery behavior
======================


The State of Charge (SOC) of a battery indicates the level of charge of a battery relative to the battery capacity. 
The SOC of a battery can be calculated 


.. math::
    :label: eq:SOC

    \text{SOC} = \frac{E_{bat}}{E_{cap}}

where, :math:`\text{E}_{bat}` is the energy in the battery while :math:`\text{E}_{cap}` is the battery capacity. 

The energy in the battery is decided based on the amount of power charged or discharged to or from the battery

.. math::
    :label: eq:E_bat_charge

    \text{E}_{bat, charge} = E_{bat}+\eta_{charge} P_{charge}


.. math::
    :label: eq:E_bat_discharge

    \text{E}_{bat, discharge} = E_{bat}-\frac{P_{discharge}}{\eta_{discharge}} 

here, :math:`\eta_{charge}` and :math:`\eta_{discharge}` are the charging and discharging efficiency, respectively, and :math:`\text{P}_{charge}` and :math:`\text{P}_{discharge}` are the amount of power charged and discharged, respectively. 

