=====================================
Load and production generation
=====================================

.....................................
Load profile generator
.....................................

The load profiles used in relsad is generated based on specifications from *FASIT Kravspesifikasjon* (requirements specification) CITE. The load profiles are given for different load customer categories, time of day, low and high load, and if it is a weekday or weekend. The dataset used in the profile can be seen in HENVISE TIL DATA... 

The load profiles are calculated as

.. math::
    :label: eq:loadprofile

    P_{load} = A_{i, t}T+B_{i,t}

here, :math:`A_{i,t}` is the A parameter from the dataset for load category *i* at time *t*, :math:`T` is the temperature in degrees, and :math:`B_{i,t}` is the B parameter from the dataset for load category *i* at time *t*. 

The temperatures are collected from weather data at Rygge in Norway and can be seen HENVIS TIL RYGGE DATA. 

The dataset has an hourly resolution. 

.....................................
Wind power generator
.....................................

Wind power can be generated 


.. math::
    :label: eq:windpower

    v_{wind} = v_{0}(\frac{H}{H_{0}})^{\alpha}

.. math::
    :label: eq:windvelocity

    v_{wind} = v_{0}(\frac{H}{H_{0}})^{\alpha}


.....................................
Solar power generator
.....................................
