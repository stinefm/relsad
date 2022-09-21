===================
Reliability indices
===================

To evaluate the reliability of a power system reliability, proper indices can be used as a measure for the reliability assessment. The three basic reliability parameters as derived in :cite:`Billinton:1992`, are the fault frequency or average failure rate of the system. :math:`\lambda_{s}`, the annual average outage time in the system, :math:`U_{s}`, and the average outage time, :math:`r_{s}`. 
In a radially operated distribution system, these reliability parameters can be derived as 

.. math::
    :label: eq:failure_rate

    \lambda_{s} = \sum_{\forall i} \lambda_{i}

.. math::
    :label: eq:annual_outage_time

    U_{s} = \sum_{\forall i} \lambda_{i}r_{i}

.. math::
    :label: eq:outage_time

    r_{s} = \frac{U_{s}}{\lambda_{s}} = \frac{\sum_{\forall i} \lambda_{i}r_{i} }{\sum_{\forall i} \lambda_{i}}

where :math:`\lambda_{i}` is the average failure rate of component *i* and :math:`r_{i}` is the average outage time of component *i*. 

These reliability parameters do not tell anything about the electrical consequence for the system or the consequence experienced by the customers in the system. There exist different reliability indices used for measuring and quantifying the reliability in the distribution system. They are divided into customer-oriented indices and load- and production-oriented indices. 

.. Since relsad includes implementation of electrical vehicles (EVs), indices related to impacts on the EVs are included in relsad CITE ny artikkel.
.....................................
Load- and generation-oriented indices
.....................................


Load- and generation-oriented indices aim to give the electrical consequence of a failure in the system. In RELSAD, two indices in this category are considered.



1. Energy Not Supplied 


.. math::
    :label: eq:ENS

    \text{ENS}_{s} = \sum U_{i}P_{i}

ENS gives the energy not supplied for the power system which measures how much power is not being able to be served. 
                


2. Cost of Energy Not Supplied 

.. math::
    :label: eq:CENS

    \text{CENS}_{s} = \sum \text{ENS}_{i}c_{i}

CENS gives the cost of interruption in the system. :math:`c_{i}` is the specific interruption cost for the different customer categories at load point *i*. 
                

.....................................
Customer-oriented indices
.....................................

Customer-oriented indices aim to give the reliability of the distribution system by the frequency and duration of interruptions experienced by the customers. In RELSAD, three different customer-oriented indices are considered. 

1. System Average Interruption Frequency Index

.. math::
    :label: eq:SAIFI

    \text{SAIFI} = \frac{\sum_{\forall i} \lambda_{i}N_{i}}{\sum N_{i}}
                 

where :math:`N_{i}` is the total number of customers served and :math:`\sum_{\forall i} \lambda_{i}N_{i}` is the total number of customer interruptions. SAIFI measures the frequency of interruptions the customers in the system expect to experience. 

2. System Average Interruption Duration Index

.. math::
    :label: eq:SAIDI

    \text{SAIDI} = \frac{\sum_{\forall i} U_{i}N_{i}}{\sum N_{i}}

where :math:`\sum_{\forall i} U_{i}N_{i}` is the total number of customer interruption durations. SAIDI measures the expected duration of interruptions a customer is expected to experience in the system. 


3. Customer Average Interruption Duration Index

.. math::
    :label: eq:CAIDI

    \text{CAIDI} = \frac{\sum_{\forall i} U_{i}N_{i}}{\sum_{\forall i} \lambda_i N_{i}} = \frac{\text{SAIDI}}{\text{SAIFI}}

CAIDI is the ratio between SAIDI and SAIFI and measures the average duration each given customer in the system is expected to experience.