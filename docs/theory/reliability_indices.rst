===================
Reliability indices
===================

SAIFI

.. math::
    :label: eq:SAIFI

    \text{SAIFI} &= \frac{\text{Total number of customers interruptions}}{\text{Total number of customers served}} \notag\\
                 &= \frac{\sum \lambda_{i}N_{i}}{\sum N_{i}}

SAIDI

.. math::
    :label: eq:SAIDI

    \text{SAIDI} &= \frac{\text{Sum of all customer interruption durations}}{\text{Total number of customers served}} \notag \\
    &= \frac{\sum U_{i}N_{i}}{\sum N_{i}}

Where :math:`U_{i}` is the annual outage time for location :math:`i`. 

CAIFI

.. math::
    :label: eq:CAIFI

    \text{CAIFI} &= \frac{\text{Total number of customer interruptions}}{\text{Total number of customers affected}} \notag \\
    &= \frac{\sum U_{i}N_{i}}{\sum N_{i}}

CAIDI

.. math::
    :label: eq:CAIDI

    \text{CAIDI} &= \frac{\text{Sum of customer interruption durations}}{\text{Total number of customer interruptions}} \notag \\
    &= \frac{\sum U_{i}N_{i}}{\sum \lambda_i N_{i}}