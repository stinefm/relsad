.. _tutorial:

....................
Active power systems
....................

The traditional power system shown in the tutorials presenting 
:ref:`Monte Carlo <tutorial_traditional_power_system_monte_carlo>`
and
:ref:`sequential <tutorial_traditional_power_system_monte_carlo>`
simulations types can be expanded with active and smart components.

This page illustrates how these components and features are initialized
and where they must be included in the system definition.

"""""""""""""""""""""""
Active generation units
"""""""""""""""""""""""

Three types of active generations units can be added:

- Production units
- Batteries
- EV parks (Electric vehicle parks)

In order to add generation units the components need to be imported::

    from relsad.network.components import (
        Production,
        Battery,
        EVPark,
    )
    from relsad.Table import Table
    
The `Table` class must be used to define the amount
of EVs in the EV park as a function of time.
    
Then the active generation units need to be created::

    # A generation unit:

    P1 = Production(
        name="P1",
        bus=B3,
    )

    # A battery:

    Bat1 = Battery(
        name="B1",
        bus=B6,
    )

    # An EV park

    num_ev_table = Table(
        x=np.arange(0, 24),  # Hour of the day
        y=np.ones(24) * 10,  # Number of EVs
    )

    EVPark(
        name="EV1", 
        bus=B5, 
        num_ev_dist=num_ev_table,
        v2g_flag=True,
    )

NB! The active generation units must be initialized before
any network initializations.

The production unit is placed on bus `B3` and the battery is placed
on bus `B6`.

Here, the EV park is placed in bus `B5` and `num_ev_table` defines a
constant number of ten cars in the EV park throughout the day.
The possibilities of vehicle-to-grid can be decided
using the `v2g_flag`.

Generation can be added to a production unit on the bus::

    generation_profile = np.ones(365 * 24) * 0.02  # MW
    P1.add_prod_data(
        pprod_data=generation_profile,
    )

The generation profile is specified by the variable `generation_profile`.
Here it is defined to provide a constant production of 0.02 MW throughout
the year.
A way of creating generation profiles is shown in :ref:`Load and generation preparation <load_and_generation_preparation>`. 


"""""""""""""""""""""""""
Grid connected microgrids
"""""""""""""""""""""""""

For evaluating a network with a microgrid, an additional network class needs to be imported::

    from relsad.network.systems import Microgrid

Furthermore, microgrid mode enumeration class needs to be imported from the *MicrogridController* class::

    from relsad.network.components import MicrogridMode

The Microgrid mode is used to specify the produre
the microgrid should follow. 

Then the components in the microgrid can be created::

    # Buses:
    
    M1 = Bus(
        name="M1",
        n_customers=1,
        coordinate=[-1, -2],
    )
    
    M2 = Bus(
        name="M2",
        n_customers=1,
        coordinate=[-2, -3],
    )
    
    M3 = Bus(
        name="M3",
        n_customers=1,
        coordinate=[-1, -3],
    )
    
    # Lines:
    
    ML1 = Line(
        name="ML1",
        fbus=B2,
        tbus=M1,
        r=0.5,
        x=0.5,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_repair_time_dist,
    )
    
    ML2 = Line(
        name="ML2",
        fbus=M1,
        tbus=M2,
        r=0.5,
        x=0.5,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_repair_time_dist,
    )
    
    ML3 = Line(
        name="ML3",
        fbus=M1,
        tbus=M3,
        r=0.5,
        x=0.5,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_repair_time_dist,
    )
    
    # Circuit breaker:
    
    E2 = CircuitBreaker(name="E2", line=ML1)
    
    # Disconnectors:
    
    DML1a = Disconnector(
        name="ML1a",
        line=ML1,
        bus=B2,
    )
    DML1b = Disconnector(
        name="ML1b",
        line=ML1,
        bus=M1,
    )
    DML2a = Disconnector(
        name="ML2a",
        line=ML2,
        bus=M1,
    )
    DML2b = Disconnector(
        name="ML2b",
        line=ML2,
        bus=M2,
    )
    DML3a = Disconnector(
        name="ML3a",
        line=ML3,
        bus=M1,
    )
    DML4b = Disconnector(
        name="ML4b",
        line=ML3,
        bus=M3,
    )

After the microgrid components are created, the microgrid
network can be created and the components can be added::

    m = Microgrid(
        distribution_network=dn,
        connected_line=ML1,
        mode=MicrogridMode.FULL_SUPPORT,
    )
    m.add_buses([M1, M2, M3])
    m.add_lines([ML2, ML3])




""""""""""""""""""""""""""""""
Islanded networks (microgrids)
""""""""""""""""""""""""""""""

For evaluating islanded networks or microgrids, the distribution network
or microgrid network can be initiated without an overlying
transmission network. Below is an example of how this is done. Note that
the `connected_line` variable is set to `None` in this case::

    dn = Distribution(
        parent_network=ps,
        connected_line=None,
    )
    dn.add_buses(
        [B1, B2, B3, B4, B5, B6]
    )
    dn.add_lines(
        [L1, L2, L3, L4, L5, L6]
    )


"""""""""""""""""""""""""""""""""""
Power system with ideal ICT network
"""""""""""""""""""""""""""""""""""

This section illustrates basic usage of the ICT features implemented in `RELSAD`.
First, we illustrate how to include ICT components without an ICT network.
In this case, the communication between the ICT components is considered
to be ideal, without any probability of failing.


For including ICT components imported the following:: 

    from relsad.network.components import (
        MainController, 
        Sensor, 
        IntelligentSwitch,
    )

A smart controller is initiated as follows::

    C1 = MainController(name="C1")

In addition, different failure rates and repair times for the controller
can be specified. 

Intelligent switches are added to disconnectors as shown here::

    Isw1 = IntelligentSwitch(
        name="Isw1",
        disconnector=DL2a,
    )

A failure rate for the intelligent switch can also be specified.
There can only be one intelligent switch on each disconnector. 

A sensor can be added on a line::

    S1 = Sensor(
        name="S1",
        line=L2,
    )

Failure rates and repair time of the sensor can be specified.
There can only be on sensor on each line. 


""""""""""""""""""""""""""""""""""""""
Power system with failable ICT network
""""""""""""""""""""""""""""""""""""""

Second, inclusion of ICT components with an ICT network is shown. In this case,
the communication between the ICT components might fail leading to potential
downtime.

For including an ICT network, the following must be imported:: 

    from relsad.network.systems import ICTNetwork
    from relsad.network.components import (
        ICTNode, 
        ICTLine,
    )

To add the ICT network, ICT nodes and ICT lines must be defined and added to
a ICT network::

    # ICT nodes
    ICTNC1 = ICTNode(
        name="ICTNC1",
    )
    ICTNISW1 = ICTNode(
        name="ICTNISW1",
    )
    ICTNS1 = ICTNode(
        name="ICTNS1",
    )

    # ICT lines
    ICTL1 = ICTLine(
        name="ICTL1",
        fnode=ICTNC1,
        tnode=ICTNISW1,
    )
    ICTL2 = ICTLine(
        name="ICTL2",
        fnode=ICTNC1,
        tnode=ICTNS1,
    )
    ICTL3 = ICTLine(
        name="ICTL3",
        fnode=ICTNS1,
        tnode=ICTNISWS1,
    )

    # ICT network
    ict_network = ICTNetwork(ps)
    ict_network.add_nodes(
        [
            ICTNC1,
            ICTNISW1,
            ICTNS1,
        ]
    )
    ict_network.add_lines(
        [
            ICTL1,
            ICTL2,
            ICTL3,
        ]
    )


Here, we only initiate a "dummy-network" to illustrate a minimal example
of the ICT network definition. In a real simulation, the network is
much more comprehensive. We refer to the CINELDI example network for
a more comprehensive example.
