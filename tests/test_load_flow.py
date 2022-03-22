
from relsad.network.components import (
    Bus,
    CircuitBreaker,
    Disconnector,
    Line,
    Battery,
    EVPark,
    Production,
    MainController,
    ManualMainController,
)

from relsad.network.systems import (
    Distribution,
    PowerSystem,
    Transmission,
    Microgrid,
)

def initialize_network(
    include_wind: bool=True, 
    include_PV: bool=True,
    include_ev: bool=True,
    v2g_flag: bool=True,
):

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


    C1 = ManualMainController(name="C1", section_time=Time(1, TimeUnit.HOUR))

    ps = PowerSystem(C1)

    fail_rate_trafo = 0.0  # fails per year
    fail_rate_line = 0.0  # fails per year
    outage_time_trafo = Time(8, TimeUnit.HOUR)

    B1 = Bus(name="B1", n_customers=0, coordinate=[0,0], fail_rate_per_year=fail_rate_trafo, outage_time=outage_time_trafo)
    B2 = Bus(name="B2", n_customers=1, coordinate=[0,-1], fail_rate_per_year=fail_rate_trafo,outage_time=outage_time_trafo)
    B3 = Bus(name="B3", n_customers=1, coordinate=[0,-2], fail_rate_per_year=fail_rate_trafo,outage_time=outage_time_trafo)
    B4 = Bus(name="B4", n_customers=1, coordinate=[-1,-3], fail_rate_per_year=fail_rate_trafo,outage_time=outage_time_trafo)
    B5 = Bus(name="B5", n_customers=1, coordinate=[-1,-4], fail_rate_per_year=fail_rate_trafo,outage_time=outage_time_trafo)
    B6 = Bus(name="B6", n_customers=1, coordinate=[1,-3], fail_rate_per_year=fail_rate_trafo,outage_time=outage_time_trafo)

    L1 = Line(name="L1", fbus=B1, tbus=B2, r=0.5, x=0.5, outage_time_dist=line_stat_dist, fail_rate_density_per_year=fail_rate_line)
    L2 = Line(name="L2", fbus=B2, tbus=B3, r=0.5, x=0.5, outage_time_dist=line_stat_dist, fail_rate_density_per_year=fail_rate_line)
    L3 = Line(name="L3", fbus=B3, tbus=B4, r=0.5, x=0.5, outage_time_dist=line_stat_dist, fail_rate_density_per_year=fail_rate_line)
    L4 = Line(name="L4", fbus=B4, tbus=B5, r=0.5, x=0.5, outage_time_dist=line_stat_dist, fail_rate_density_per_year=fail_rate_line)
    L5 = Line(name="L5", fbus=B3, tbus=B6, r=0.5, x=0.5, outage_time_dist=line_stat_dist, fail_rate_density_per_year=fail_rate_line)


    E1 = CircuitBreaker(name="E1", line=L1)

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

    if include_wind: 
        wind = Production(name="wind", bus=B4)
    
    if include_PV:
        PV = Production(name="PV", bus=B6)
    
    if include_ev: 
        EV1 = EVPark(name="EV1", bus=B2, num_ev_dist=1, v2g_flag=v2g_flag)
        EV2 = EVPark(name="EV2", bus=B3, num_ev_dist=1, v2g_flag=v2g_flag)
        EV3 = EVPark(name="EV3", bus=B4, num_ev_dist=1, v2g_flag=v2g_flag)
        EV4 = EVPark(name="EV4", bus=B6, num_ev_dist=1, v2g_flag=v2g_flag)

    tn = Transmission(ps, bus=B1)
    dn = Distribution(transmission_network=tn, connected_line=L1)
    dn.add_buses(
        [B1, B2, B3, B4, B5, B6]
    )
    dn.add_lines(
        [L1, L2, L3, L4, L5]
    )


def test_load_flow_passive():
    pass

def test_load_flow_battery_1():
    pass

def test_load_flow_battery_2():
    pass

def test_load_flow_wind_1():
    pass

def test_load_flow_wind_2():
    pass

def test_load_flow_PV_1():
    pass

def test_load_flow_PV_2():
    pass

def test_load_flow_V2g():
    pass

