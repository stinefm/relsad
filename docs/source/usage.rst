=====
Usage
=====

To use relsad in a project::

    import relsad

.....................................
Traditional power system
.....................................


To create a power system the necessary imports need to be added. 

For importing components from relsad::

    from relsad.network.components import (
        Bus,
        Line,
        Disconnector,
        CircuitBreaker,
        ManualMainController,
    )


For importing networks from relsad:: 

    from relsad.network.systems import (
        PowerSystem,
        Transmission,
        Distribution,
    )

In order to evaluate time dependencies, time and time unit needs to be imported::

    from relsad.Time import (
        Time, 
        TimeUnit,
    )

For using statistical distribution for, for example, failure rate and outage time of components, this needs to be imported::

    from relsad.StatDist import (
        StatDist,
        StatDistType,
        NormalParameters,
        CustomDiscreteParameters,
    )

The user can also use average values and not statistical distributions. 

For initializing a network a function can be created:: 

    def initialize_network(
        fail_rate_trafo: float,
        fail_rate_line: float,
        outage_time_trafo: Time,
    ):

Here, the failure rate and outage time for the components can be added. 

Then the system is initialized
For systems without ICT, a manual main controller is added::

    C1 = ManualMainController(name"C1"m sectioning_time=Time(0))

Then the power system is created::

    ps = PowerSystem(C1)

After this, the components are the system is created

Creating buses::

    # Failure rate and outage time of the transformer on the bus are not necessary to add, this can be added on each bus. The default is set to 0? 

    B1 = Bus(
        name="B1", 
        n_customers=0, 
        coordinate=[0,0], 
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )
    B2 = Bus(
        name="B2", 
        n_customers=1, 
        coordinate=[0,-1],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
    )

    B3 = Bus(
        name="B3", 
        n_customers=1, 
        coordinate=[0,-2], 
        fail_rate_per_year=fail_rate_trafo, 
        outage_time=outage_time_trafo,
    )

    B4 = Bus(
        name="B4", 
        n_customers=1, 
        coordinate=[-1,-3], 
        fail_rate_per_year=fail_rate_trafo, 
        outage_time=outage_time_trafo,
    )
    
    B5 = Bus(
        name="B5", 
        n_customers=1, 
        coordinate=[-1,-4], 
        fail_rate_per_year=fail_rate_trafo, 
        outage_time=outage_time_trafo,
    )
    
    B6 = Bus(
        name="B6", 
        n_customers=1, 
        coordinate=[1,-3], 
        fail_rate_per_year=fail_rate_trafo, 
        outage_time=outage_time_trafo,
    ) 

Creating lines:: 

    # Failure rate and outage time of the lines can be added to each line. The default is set to 0? 
    # For adding statistical distributions: 

    line_stat_dist = StatDist(
        stat_dist_type=StatDistType.TRUNCNORMAL,
        parameters=NormalParameters(
            loc=1.25,
            scale=1,
            min_val=0.5,
            max_val=2,
        ),
        draw_flag=True,
        get_flag=False,
    )

    L1 = Line(
        name="L1",
        fbus=B1,
        tbus=B2,
        r=0.5, 
        x=0.5,
        faile_rate_density_per_year=faile_rate_line, 
        outage_time_dist=line_stat_dist,
    )
    L2 = Line(
        name="L2",
        fbus=B2,
        tbus=B3,
        r=0.5, 
        x=0.5,
        faile_rate_density_per_year=faile_rate_line, 
        outage_time_dist=line_stat_dist,
    )
    L3 = Line(
        name="L3",
        fbus=B3,
        tbus=B4,
        r=0.5, 
        x=0.5,
        faile_rate_density_per_year=faile_rate_line, 
        outage_time_dist=line_stat_dist,
    )
    L4 = Line(
        name="L4",
        fbus=B4,
        tbus=B5,
        r=0.5, 
        x=0.5,
        faile_rate_density_per_year=faile_rate_line, 
        outage_time_dist=line_stat_dist,
    )
    L5 = Line(
        name="L5",
        fbus=B3,
        tbus=B6,
        r=0.5, 
        x=0.5,
        faile_rate_density_per_year=faile_rate_line, 
        outage_time_dist=line_stat_dist,
    )

    # Backup line

    L6 = Line(
        name="L6",
        fbus=B4,
        tbus=B6,
        r=0.5, 
        x=0.5,
        is_backup=True,
        faile_rate_density_per_year=faile_rate_line, 
        outage_time_dist=line_stat_dist,
    )

    L6.set_backup()

Creating circuit breaker::

    E1 = CircuitBreaker(name="E1", line=L1)

Creating disconnectors:: 

    DL1a = Disconnector(name="L1a", line=L1, bus=B1, circuitbreaker=E1)
    DL1b = Disconnector(name="L1b", line=L1, bus=B2, circuitbreaker=E1)
    DL1c = Disconnector(name="L1c", line=L1, bus=B2)
    DL2a = Disconnector(name="L2a", line=L2, bus=B2)
    DL2b = Disconnector(name="L2b", line=L2, bus=B3)
    DL3a = Disconnector(name="L3a", line=L3, bus=B3)
    DL3b = Disconnector(name="L3b", line=L3, bus=B4)
    DL4a = Disconnector(name="L4a", line=L4, bus=B4)
    DL4b = Disconnector(name="L4b", line=L4, bus=B5)
    DL5a = Disconnector(name="L5a", line=L5, bus=B3)
    DL5b = Disconnector(name="L5b", line=L5, bus=B6)

    # For backup line
    DL6a = Disconnector(name="L6a", line=L6, bus=B4)
    DL6b = Disconnector(name="L6b", line=L6, bus=B6)

After creating the components in the network, the components need to be added to the associated network and the power system. 
First, the bus connecting to the overlying network (often transmission network) is added and a transmission network needs to be created::
    
    tn = Transmission(ps, trafo_bus=B1)

Then the rest of the components can be added to the distribution network by creating a distribution network before the function can return the power system:: 

    dn = Distribution(parent_network=tn, connected_line=L1)
    dn.add_buses(
        [B2, B3, B4, B5, B6]
    )
    dn.add_lines(
        [L2, L3, L4, L5, L6]
    )

    return ps


.....................................
Network with generation units
.....................................

In order to add generation units the components need to be imported::

    from relsad.network.components import (
        Production,
        Battery,
    )
    
    
Then the generation units need to be created::

    # A generation unit:

    P1 = Production(name="P1", bus=B3)

    # A battery:

    B1 = Battery(name="B1", bus=B6)

.....................................
Network with electrical vehicles and vehicle-to-grid
.....................................

For including electrical vehicles (EVs) import::

    from relsad.network.components import (
        EVPark,
    )

Creating EV parks::

    EVPark(
        name="EV1", 
        bus=B5, 
        num_ev=5,
        v2g_flag=True
    )

Here, the number of EVs in the park and the possibilities of vehicle-to-grid can be decided. 


.....................................
Network with microgrid
.....................................

^^^^^^^^^^^^^^^^^^^^^^^^^
Grid connected microgrids
^^^^^^^^^^^^^^^^^^^^^^^^^

For evaluating a network with a microgrid, an additional network class needs to be imported::

    from relsad.network.systems import(
        Microgrid,
    )

Furthermore, microgrid mode needs to be imported from the *MicrogridController* class::

    from relsad.network.components import(
        MicrogridMode, 
    )

This is in order for the simulation to understand which procedure the microgrid should follow. 

Then the components in the microgrid can be created::

    # Buses: 

    M1 = Bus(
        name="M1",
        n_customers=1,
        coordinate=[-1, -2],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
        )

    M2 = Bus(
        name="M2",
        n_customers=1,
        coordinate=[-2, -3],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
        )

    M3 = Bus(
        name="M3",
        n_customers=1,
        coordinate=[-1, -3],
        fail_rate_per_year=fail_rate_trafo,
        outage_time=outage_time_trafo,
        )

    # Lines: 

    ML1 = Line(
        name="ML1",
        fbus=M2,
        tbus=M1,
        r=0.5,
        x=0.5,
        fail_rate_density_per_year=fail_rate_line,
        outage_time_dist=line_stat_dist,
        )

    ML2 = Line(
        name="ML2",
        fbus=M1,
        tbus=M2,
        r=0.5,
        x=0.5,
        fail_rate_density_per_year=fail_rate_line,
        outage_time_dist=line_stat_dist,
        )

    ML3 = Line(
        name="ML3",
        fbus=M1,
        tbus=M3,
        r=0.5,
        x=0.5,
        fail_rate_density_per_year=fail_rate_line,
        outage_time_dist=line_stat_dist,
        )

    # Circuit breaker: 

    E2 = CircuitBreaker(name="E2", line=ML1)

    # Disconnectors: 

    DML1a = Disconnector(name="ML1a", line=ML1, bus=B2, E2)
    DML1b = Disconnector(name="ML1b", line=ML1, bus=M1, E2)
    DML1c = Disconnector(name="ML1c", line=ML1, bus=M1)
    DML2a = Disconnector(name="ML2a", line=ML2, bus=M1)
    DML2b = Disconnector(name="ML2b", line=ML2, bus=M2)
    DML3a = Disconnector(name="ML3a", line=ML3, bus=M1)
    DML4b = Disconnector(name="ML4b", line=ML3, bus=M3)

After the microgrid components are created, the microgrid can be created and the components can be added::

    m = Microgrid(dn, ML1, mode=microgrid_mode)
    m.add_buses([M1, M2, M3])
    m.add_lines([ML2, ML3])




^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Islanded networks (microgrids)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For evaluating islanded networks or microgrids, the network should be created without an overlying network connection::

    dn = Distribution(parent_network=ps, connected_line=None)
    dn.add_buses(
        [B1, B2, B3, B4, B5, B6]
    )
    dn.add_lines(
        [L1, L2, L3, L4, L5, L6]


.....................................
Network with ICT
.....................................


