.. _bfs_theory:

======================
Backward-Forward sweep
======================

Forward-Backward sweep (FBS) is a load flow approach suitable for radial operated power systems. 
The benefit of using an FBS approach is that the load flow is calculated iteratively and do not need to go through the Jacobian matrix, as in the Newton-Rapshon method. 
In this way, convergence problems related to an ill conditioned matrix of weak networks can be avoided. :cite:`haque1996load`

In an FBS approach, the load flow is calculated by updating the power flow through a backward sweep before the buses voltage magnitude and angle are updated and calculated in the forward sweep. 

..............
Backward sweep
..............

In the backward sweep, the active and reactive power over the system lines is calculated. The active and reactive power over line *l* for iteration *k*, :math:`P_{l}` and :math:`Q_{l}` respectively, is calculated by adding the 
accumulated active and reactive load, :math:`P_{l}^{'}` and :math:`Q_{l}^{'}` respectively, at the downstream buses and the accumulated active and reactive power losses, :math:`P_{l}^{*}`  and :math:`Q_{l}^{*}` respectively, over the downstream
lines including the power loss over line *l* and the load at the current bus

.. math::
    :label: eq:PowerA

    P_{l} = P_{l}^{'} + P_{l}^{*}

.. math::
    :label: eq:PowerQ

    Q_{l} = Q_{l}^{'} + Q_{l}^{*}
    
where the accumulated active and reactive load at the buses are calculated

.. math::
    :label: eq:acc_P_load

    P_{l}^{'} = P_{i}^{load} + \sum_{d_{b}} P_{d_{b}}^{load}


.. math::
    :label: eq:acc_Q_load

    Q_{l}^{'} = Q_{i}^{load} + \sum_{d_{b}} Q_{d_{b}}^{load}


where :math:`P_{i}^{load}` is the active load at node *i* while :math:`Q_{i}^{load}` is the reactive load at node *i*. :math:`P_{d_{b}}^{load}` and :math:`Q_{d_{b}}^{load}` are the active and reactive loads at the downstream buses, respectively. 

The accumulated active and reactive power losses can be calculated as 

.. math::
    :label: eq:acc_P_loss

    P_{l}^{*} = P_{l}^{loss} + \sum_{d_{l}} P_{d_{l}}^{loss}


.. math::
    :label: eq:acc_Q_loss

    Q_{l}^{*} = Q_{l}^{loss} + \sum_{d_{l}} Q_{d_{l}}^{loss}

where :math:`P_{l}^{loss}` and :math:`Q_{l}^{loss}` are the active and reactive power loss over line *l*, respectively. Here, :math:`P_{d_{l}}^{loss}` :math:`Q_{d_{l}}^{loss}` are the active and reactive power loss of the downstream lines, respectively. 


Furthermore, the active and reactive power loss over a line can be calculated battery

.. math::
    :label: eq:P_loss

    P_{l}^{loss} = R_{l}*{loss} \frac{P_{l}^{'2} + Q_{l}^{'2}}{V_{j}^{2}} 

.. math::
    :label: eq:Q_loss

    Q_{l}^{loss} = X_{l}*{loss} \frac{P_{l}^{'2} + Q_{l}^{'2}}{V_{j}^{2}} 


Here, :math:`R_{l}` is the line resistance while :math:`X_{l}` is the line reactance. :math:`V_{j}` is the voltage at the ending bus. 


..............
Forward sweep
..............

After a backward sweep, the forward sweep is conducted. In the forward sweep, the buses voltage magnitude and angle are updated by utilizing the updated active and reactive power from the backward sweep.
Here, the voltage magnitude at bus *i* in relation to the voltage magnitude at bus *j* for iteration *k* can be calculated battery

.. math::
    :label: eq:vol_mag

    V_{i} = V_{j} - I_{l}(R_{l}+jX_{l}) = \sqrt{V_{j}^{2} - T_{1} - T_{2}}

where the :math:`T_{1}` and :math:`T_{2}` can be expressed as

.. math::
    :label: eq:T1
    T_{1} = 2(P_{l}R_{l} + Q_{l}X_{l}) 

.. math::
    :label: eq:T2
    T_{2} = \frac{(P_{l}^{2}+Q_{l}^{2})(R_{l}^{2}+X_{l}^{2})}{V_{j}^{2}}

The voltage angle can be expressed as 

.. math::
    :label: eq:T1
    \delta_{i} = \delta_{j} + \arctan{\frac{Im(V_{i})}{Re(V_{i})}}

where :math:`\delta_{j}` is the voltage angle at bus *j* and :math:`Im(V_{i})` and :math:`Re(V_{i})` are the imaginary part and the real part of :math:`V_{i}`, respectively.