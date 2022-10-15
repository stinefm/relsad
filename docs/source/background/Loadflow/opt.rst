==================================
Load shedding optimization problem
==================================

Since in most systems, there are lines and generation resources with
limited capacity, a simple energy shedding optimization problem
is implemented. The load shedding optimization problem aims to
minimize the total load shed in a power system based on the
price of shedding load for the system operator. 

The energy shedding optimization problem minimizes the total load
shed in the network based on *Cost of Energy not Supplied* (CENS)
for shedding that specific load type. This is subjected to load flow
balance and capacity limitations over the power lines and bus restriction
such as load and generation capacity at the bus. Here :math:`C_{n}`
represent the cost of shedding load at bus *n* while :math:`P_{n}^{s}`
is the amount of power shed at node *n*. :math:`P_{j}^{g}` is the
production from generator *j* where :math:`P_{k}^{d}` is the load
demand at bus *k*. :math:`P_{i}^{l}` is the power transferred over
line *i*. :math:`\gamma_{i}` = 1 if line *i* is the starting point,
-1 if line *i* is the ending point. :math:`\lambda_{j}` = 1 if there
is a production unit at node *j*, otherwise :math:`\lambda_{j}` is 0.
:math:`\mu_{k}` = 1 if there is a load at node *k*, otherwise
:math:`\mu_{k}` is 0. 

.. math::
   :nowrap:

    \begin{align}
        &\underset{P^{s}_{n}}{\text{minimize}}
        \quad \mathcal{P}_s = \sum_{n = 1}^{N_n}   C_{n}\cdot P^{s}_{n} \label{eq:min}\\
        &\text{subject to: } \nonumber \\
        &\begin{aligned}
            \sum_{i=1}^{N_l} \gamma_i \cdot P^{l}_{i} &= \sum_{j=1}^{N_g} \lambda_j \cdot P^{g}_{j} - \sum_{k = 1}^{N_n}& \mu_k& \cdot (P^{d}_{k} - P^{s}_{k})\\
            \min P_{j}^{g} &\leq P_{j}^{g} \leq \max P_{j}^{g} &\forall j&=1,\dots,N_{g}\\
            0 &\leq P_{k}^{s} \leq P_{k}^{d}  &\forall k&=1,\dots,N_{n}\\
            \left| P_{i}^{l} \right| &\leq \max P_{i}^{l}  &\forall i&=1,\dots,N_{l}\\
        \end{aligned} \nonumber
    \end{align}
