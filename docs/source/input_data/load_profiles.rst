.. _load_profiles:

........................
Load profile preparation
........................

The load profiles used in the examples presented in RELSAD are generated based on specifications from *FASIT Kravspesifikasjon* (requirements specification) :cite:`FASIT`. The load profiles are given for different load customer categories, time of day, low and high load, and if it is a weekday or weekend. The dataset used in the profiles can be seen in :download:`this file <../_static/load_profiles_fasit.csv>`.

The load profiles are calculated as

.. math::
    :label: eq:loadprofile

    P_{load} = A_{i, t}T+B_{i,t}

here, :math:`A_{i,t}` is the A parameter from the dataset for load category *i* at time *t*, :math:`T` is the temperature in degrees, and :math:`B_{i,t}` is the B parameter from the dataset for load category *i* at time *t*. 

The temperatures are collected from weather data at Rygge in Norway and can be seen :download:`this file <../../../examples/data/weather_data_rygge.csv>`. 

The dataset has an hourly resolution. 
