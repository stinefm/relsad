.. _usage:

=====
Usage
=====

This document introduces basic usage of `relsad`.

.....................................
Traditional power system
.....................................

First, the creation of a small example network in `relsad` is presented. The network consists of 6 buses and 6 lines, where one of the lines is a backup line.


""""""""""""""""""""""""
Imports
""""""""""""""""""""""""

To create a power system the necessary imports need to be added. 

For importing components from relsad::

    from relsad.network.components import (
        Bus,
        Line,
        Disconnector,
        CircuitBreaker,
        ManualMainController,
    )


For importing systems and networks from relsad:: 

    from relsad.network.systems import (
        PowerSystem,
        Transmission,
        Distribution,
    )

To run time dependent simulations, the time utilities of `relsad` must be imported::

    from relsad.Time import (
        Time, 
        TimeUnit,
    )

Adding statistical distribution for, for example, outage time of components, is done by using the statistical distribution utilities of `relsad`, which needs to be imported::

    from relsad.StatDist import (
        StatDist,
        StatDistType,
        NormalParameters,
        CustomDiscreteParameters,
    )

The statistical distribution utilities of `relsad` enables a variety of custom distributions, including normal and uniform distributions.

""""""""""""""""""""""""
Initialize power system
""""""""""""""""""""""""

For systems without ICT, a manual main controller is added with a name and a desired sectional time::

    C1 = ManualMainController(name="C1", sectioning_time=Time(0))

Then the power system is created::

    ps = PowerSystem(controller=C1)


""""""""""""""""""""""""
Add components
""""""""""""""""""""""""
After this, the components are of the system is created

Creating buses::

    # Failure rate and outage time of the transformer on the bus are not necessary to add, this can be added on each bus. Their default values are 0 and Time(0) respectively.

    B1 = Bus(
        name="B1", 
        n_customers=0, 
        coordinate=[0, 0],
    )
    B2 = Bus(
        name="B2", 
        n_customers=1, 
        coordinate=[1, 0],
    )

    B3 = Bus(
        name="B3", 
        n_customers=1, 
        coordinate=[2, 1],
    )

    B4 = Bus(
        name="B4", 
        n_customers=1, 
        coordinate=[2, 0],
    )
    
    B5 = Bus(
        name="B5", 
        n_customers=1, 
        coordinate=[3, 0],
    )
    
    B6 = Bus(
        name="B6", 
        n_customers=1, 
        coordinate=[3, 1],
    ) 

Creating lines:: 

    # Failure rate and outage time of the lines can be added to each line. The default value of the line failure rate is 0, while the default outage time is 0 (Uniform float distribution with max/min values of 0).

    # For adding statistical distributions, in this case a truncated normal distribution: 

    line_stat_dist = StatDist(
        stat_dist_type=StatDistType.TRUNCNORMAL,
        parameters=NormalParameters(
            loc=1.25,
            scale=1,
            min_val=0.5,
            max_val=2,
        ),
    )

    fail_rate_line = 0.07

    L1 = Line(
        name="L1",
        fbus=B1,
        tbus=B2,
        r=0.5, 
        x=0.5,
        fail_rate_density_per_year=fail_rate_line, 
        repair_time_dist=line_stat_dist,
    )
    L2 = Line(
        name="L2",
        fbus=B2,
        tbus=B3,
        r=0.5, 
        x=0.5,
        fail_rate_density_per_year=fail_rate_line, 
        repair_time_dist=line_stat_dist,
    )
    L3 = Line(
        name="L3",
        fbus=B3,
        tbus=B4,
        r=0.5, 
        x=0.5,
        fail_rate_density_per_year=fail_rate_line, 
        repair_time_dist=line_stat_dist,
    )
    L4 = Line(
        name="L4",
        fbus=B4,
        tbus=B5,
        r=0.5, 
        x=0.5,
        fail_rate_density_per_year=fail_rate_line, 
        repair_time_dist=line_stat_dist,
    )
    L5 = Line(
        name="L5",
        fbus=B3,
        tbus=B6,
        r=0.5, 
        x=0.5,
        fail_rate_density_per_year=fail_rate_line, 
        repair_time_dist=line_stat_dist,
    )

    # Backup line

    L6 = Line(
        name="L6",
        fbus=B4,
        tbus=B6,
        r=0.5, 
        x=0.5,
        is_backup=True,
        fail_rate_density_per_year=fail_rate_line, 
        repair_time_dist=line_stat_dist,
    )

    # Set L6 as a backup line

    L6.set_backup()

Creating circuit breaker::

    E1 = CircuitBreaker(
        name="E1",
        line=L1,
        )

Creating disconnectors::
    
Disconnectors can be added to the lines in the system. A line can have zero, one or two disconnectors connected. In this example, e we add several disconnectors for each line. If a circuit breaker is placed on a line, can also have two disconnectors:: 

    DL1a = Disconnector(
        name="L1a", 
        line=L1, bus=B1,
        )
    DL1b = Disconnector(
        name="L1b",
        line=L1,
        bus=B2,
        )
    DL2a = Disconnector(
        name="L2a",
        line=L2,
        bus=B2,
        )
    DL2b = Disconnector(
        name="L2b",
        line=L2,
        bus=B3,
        )
    DL3a = Disconnector(
        name="L3a",
        line=L3,
        bus=B3,
        )
    DL3b = Disconnector(
        name="L3b",
        line=L3,
        bus=B4,
        )
    DL4a = Disconnector(
        name="L4a",
        line=L4,
        bus=B4,
        )
    DL4b = Disconnector(
        name="L4b",
        line=L4,
        bus=B5,
        )
    DL5a = Disconnector(
        name="L5a",
        line=L5,
        bus=B3,
        )
    DL5b = Disconnector(
        name="L5b",
        line=L5,
        bus=B6,
        )

    # For backup line
    DL6a = Disconnector(
        name="L6a",
        line=L6,
        bus=B4,
        )
    DL6b = Disconnector(
        name="L6b",
        line=L6,
        bus=B6,
        )

""""""""""""""""""""""""
Add networks
""""""""""""""""""""""""

After creating the components in the network, the components need to be added to their associated networks and the associated networks must be added to the power system. 
First, the bus connecting to the overlying network (often transmission network) is added. In this case the overlying network is a transmission network, which is created by::
    
    tn = Transmission(
        parent_network=ps,
        trafo_bus=B1,
        )

The distribution network contains the rest of the components, and links to the transmission network with line L1. This is done by the following code snippet:: 

    dn = Distribution(
        parent_network=tn,
        connected_line=L1,
        )
    dn.add_buses(
        [B2, B3, B4, B5, B6]
    )
    dn.add_lines(
        [L2, L3, L4, L5, L6]
    )


""""""""""""""""""""""""
Visualize topology
""""""""""""""""""""""""

To validate the network topology, it can be plotted in the following way::

    from relsad.visualization.plotting import plot_topology
    
    fig = plot_topology(
        buses=ps.buses,
        lines=ps.lines,
        bus_text=True,
        line_text=True,
    )

    fig.savefig(
        "test_network.png",
        dpi=600,
    )

The plot should look like this:

.. figure:: figures/CINELDI_testnetwork.png
   :height: 200
   :width: 400
   :alt: Test network.
   
   Test network 


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

    P1 = Production(
        name="P1",
        bus=B3,
        )

    # A battery:

    B1 = Battery(
        name="B1",
        bus=B6,
        )

.....................................
Network with electrical vehicles and vehicle-to-grid
.....................................

For including electrical vehicles (EVs) import::

    from relsad.network.components import EVPark

Creating an EV park::

    EVPark(
        name="EV1", 
        bus=B5, 
        num_ev=5,
        v2g_flag=True,
    )

Here, the number of EVs in the park and the possibilities of vehicle-to-grid can be decided. 


.....................................
Network with microgrid
.....................................

"""""""""""""""""""""""""
Grid connected microgrids
"""""""""""""""""""""""""

For evaluating a network with a microgrid, an additional network class needs to be imported::

    from relsad.network.systems import(
        Microgrid,
    )

Furthermore, microgrid mode enumeration class needs to be imported from the *MicrogridController* class::

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
        repair_time_dist=line_stat_dist,
    )

    ML2 = Line(
        name="ML2",
        fbus=M1,
        tbus=M2,
        r=0.5,
        x=0.5,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
    )

    ML3 = Line(
        name="ML3",
        fbus=M1,
        tbus=M3,
        r=0.5,
        x=0.5,
        fail_rate_density_per_year=fail_rate_line,
        repair_time_dist=line_stat_dist,
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

After the microgrid components are created, the microgrid can be created and the components can be added::

    m = Microgrid(
        distribution_network=dn,
        connected_line=ML1,
        mode=microgrid_mode,
    )
    m.add_buses([M1, M2, M3])
    m.add_lines([ML2, ML3])


""""""""""""""""""""""""""""""
Islanded networks (microgrids)
""""""""""""""""""""""""""""""

For evaluating islanded networks or microgrids, the network should be created without an overlying network connection::

    dn = Distribution(
        parent_network=ps,
        connected_line=None,
        )
    dn.add_buses(
        [B1, B2, B3, B4, B5, B6]
    )
    dn.add_lines(
        [L1, L2, L3, L4, L5, L6]


.....................................
Network with ICT
.....................................

"""""""""""""""""""
Without ICT network
"""""""""""""""""""

This section illustrated basic usage of the ICT features implemented in RELSAD.
First, inclusion of ICT components without an ICT network is shown. In this case,
the communication between the ICT components is considered to be ideal, without
any probability of failing.


For including ICT components, the ICT components need to be imported:: 

    from relsad.network.components import (
        MainController, 
        Sensor, 
        IntelligentSwitch,
    )

The ICT components can be created.
For controller::

    C1 = MainController(name="C1")

In addition, different failure rates and repair times for the controller can be added. 

The intelligent switch is added to disconnectors::

    Isw1 = IntelligentSwitch(
        name="Isw1",
        disconnector=DL2a,
        )

A failure rate for the intelligent switch can also be added to the component. There can only be one intelligent switch on each disconnector. 

A sensor can be added on a line::

    S1 = Sensor(
        name="S1",
        line=L2,
        )

Failure rates and repair time of the sensor can be added to the component. There can only be on sensor on each line. 


"""""""""""""""""""
With ICT network
"""""""""""""""""""

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



.....................................
Monte Carlo simulation
.....................................

In :ref:`load_and_production_generation`, examples of how to generate load and generation profiles are provided. 
The generated profiles can be used to set the load and generation on the buses in the system. 
The load and generation profiles can then be added to the buses in the system. 


In addition, a cost related to the load can be added to the bus. For generating the specific interruption for a load category:: 

    household = CostFunction(
        A = A,
        B = B,
    )

Load and cost can be added to the buses::

    B2.add_load_data(
        pload_data=load_household,
        cost_function=household,
    )

Here, a household type load is chosen. The household type load is based on the load profile shown in :ref:`load_and_production_generation`.

Generation can be added to a production unit on the bus::

    P1.add_prod_data(
        pprod_data=Prod_PV,
    )

Here, the generation profile represent production from solar power. This generation type is based on the generation profiles shown in :ref:`load_and_production_generation`. 

Finally, to run a simulation the user must specify:

* The number of iterations, `iterations`
* Simulation start time, `start_time`
* Simulation stop time, `stop_time`
* Time step, `time_step`
* Time unit presented in results, `time_unit`
* List of Monte Carlo iterations to save, `save_iterations`
* Saving directory for results, `save_dir`
* Number of processes, `n_procs`
  
::

    sim = Simulation(power_system=ps, random_seed=random_seed)
    sim.run_monte_carlo(
        iterations=iterations, 
        start_time=TimeStamp(
            year=start_year, 
            month=start_month,
            day=start_day,
            hour=start_hour, 
            minute=start_minute, 
            second=start_second,
        ),
        stop_time=TimeStamp(
            year=stop_year,
            month=stop_month, 
            day=stop_day,
            minute=stop_minute, 
            second=stop_second,
        ),
        time_step=Time(1, TimeUnit.Hour), 
        time_unit=TimeUnit.Hour,
        save_iterations=save_iterations, 
        save_dir=save_dir,
        n_procs=number_processes, 
    )


