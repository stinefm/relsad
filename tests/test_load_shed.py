import numpy as np
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

from relsad.loadflow.ac import run_bfs_load_flow
from relsad.load.shedding import shed_loads
from relsad.utils import eq
from relsad.Time import (
    Time,
    TimeUnit,
)

def initialize_network(
    island_mode: bool=False,
    include_battery: bool=False,
    include_wind: bool=False, 
    include_PV: bool=False,
    include_ev: bool=False,
    v2g_flag: bool=False,
):

    C1 = ManualMainController(name="C1", sectioning_time=Time(0))

    ps = PowerSystem(C1)

    B1 = Bus(name="B1", n_customers=0, coordinate=[0,0])
    B2 = Bus(name="B2", n_customers=1, coordinate=[0,-1])
    B3 = Bus(name="B3", n_customers=1, coordinate=[0,-2])
    B4 = Bus(name="B4", n_customers=1, coordinate=[-1,-3])
    B5 = Bus(name="B5", n_customers=1, coordinate=[-1,-4])
    B6 = Bus(name="B6", n_customers=1, coordinate=[1,-3])

    length = 1
    r = 0.5
    x = 0.5
    rho = 1.72e-8
    s_ref = 1
    v_ref = 22.0

    area = length * rho * 1e3 / r

    L1 = Line(
        name="L1",
        fbus=B1,
        tbus=B2,
        r=r,
        x=x,
        rho=rho,
        area=area,
        s_ref=s_ref,
        v_ref=v_ref,
    )
    L2 = Line(
        name="L2",
        fbus=B2,
        tbus=B3,
        r=r, 
        x=x,
        rho=rho,
        area=area,
        s_ref=s_ref,
        v_ref=v_ref,
    )
    L3 = Line(
        name="L3",
        fbus=B3,
        tbus=B4,
        r=r, 
        x=x,
        rho=rho,
        area=area,
        s_ref=s_ref,
        v_ref=v_ref,
    )
    L4 = Line(
        name="L4",
        fbus=B4,
        tbus=B5,
        r=r, 
        x=x,
        rho=rho,
        area=area,
        s_ref=s_ref,
        v_ref=v_ref,
    )
    L5 = Line(
        name="L5",
        fbus=B3,
        tbus=B6,
        r=r, 
        x=x,
        rho=rho,
        area=area,
        s_ref=s_ref,
        v_ref=v_ref,
    )

    E1 = CircuitBreaker("E1", L1)

    if include_battery: 
        battery = Battery(
            name="Bat1",
            bus=B5,
            inj_p_max=0.05,
            inj_q_max=0.05,
            E_max=1,
            SOC_min=0.1,
            SOC_max=1,
            n_battery=0.95,
        )

    if include_wind: 
        wind = Production(name="wind", bus=B4)
    
    if include_PV:
        PV = Production(name="PV", bus=B6)
    
    if include_ev: 
        EV1 = EVPark(name="EV1", bus=B2, num_ev_dist=1, v2g_flag=v2g_flag)
        EV2 = EVPark(name="EV2", bus=B3, num_ev_dist=1, v2g_flag=v2g_flag)
        EV3 = EVPark(name="EV3", bus=B4, num_ev_dist=1, v2g_flag=v2g_flag)
        EV4 = EVPark(name="EV4", bus=B6, num_ev_dist=1, v2g_flag=v2g_flag)

    if island_mode:
        dn = Distribution(parent_network=ps, connected_line=None)
        dn.add_buses(
            [B1, B2, B3, B4, B5, B6]
        )
        dn.add_lines(
            [L1, L2, L3, L4, L5]
        )
    else:
        tn = Transmission(ps, trafo_bus=B1)
        dn = Distribution(parent_network=tn, connected_line=L1)
        dn.add_buses(
            [B2, B3, B4, B5, B6]
        )
        dn.add_lines(
            [L2, L3, L4, L5]
        )
    return ps


def test_load_shed_isolated_hour():
    ps = initialize_network(
        island_mode=True,
    )

    B1 = ps.get_comp("B1")
    B2 = ps.get_comp("B2")
    B3 = ps.get_comp("B3")
    B4 = ps.get_comp("B4")
    B5 = ps.get_comp("B5")
    B6 = ps.get_comp("B6")

    B1.add_load(
        pload=0,
        qload=0,
    )
    B2.add_load(
        pload=0.05,
        qload=0,
    )
    B3.add_load(
        pload=0.04,
        qload=0,
    )
    B4.add_load(
        pload=0.03,
        qload=0,
    )
    B5.add_load(
        pload=0.07,
        qload=0,
    )
    B6.add_load(
        pload=0.05,
        qload=0,
    )
    B1.set_cost(1)
    B2.set_cost(1)
    B3.set_cost(1)
    B4.set_cost(1)
    B5.set_cost(1)
    B6.set_cost(1)

    B1.set_slack()

    run_bfs_load_flow(ps, maxit=5)

    assert eq(B1.vomag, 1, tol=1e-6)
    assert eq(B2.vomag, 0.999752, tol=1e-6)
    assert eq(B3.vomag, 0.999555, tol=1e-6)
    assert eq(B4.vomag, 0.999452, tol=1e-6)
    assert eq(B5.vomag, 0.999380, tol=1e-6)
    assert eq(B6.vomag, 0.999504, tol=1e-6)

    assert eq(np.degrees(B1.voang), 0.0, tol=1e-6)
    assert eq(np.degrees(B2.voang), -0.014209, tol=1e-6)
    assert eq(np.degrees(B3.voang), -0.025463, tol=1e-6)
    assert eq(np.degrees(B4.voang), -0.031388, tol=1e-6)
    assert eq(np.degrees(B5.voang), -0.035536, tol=1e-6)
    assert eq(np.degrees(B6.voang), -0.028425, tol=1e-6)

    shed_loads(
        power_system=ps,
        dt=Time(1, TimeUnit.HOUR),
        alpha=1e-7,
    )

    assert eq(B1.p_load_shed_stack, 0.0, tol=1e-6)
    assert eq(B1.q_load_shed_stack, 0.0, tol=1e-6)
    assert eq(B2.p_load_shed_stack, 0.05, tol=1e-6)
    assert eq(B2.q_load_shed_stack, 0.0, tol=1e-6)
    assert eq(B3.p_load_shed_stack, 0.04, tol=1e-6)
    assert eq(B3.q_load_shed_stack, 0.0, tol=1e-6)
    assert eq(B4.p_load_shed_stack, 0.03, tol=1e-6)
    assert eq(B4.q_load_shed_stack, 0.0, tol=1e-6)
    assert eq(B5.p_load_shed_stack, 0.07, tol=1e-6)
    assert eq(B5.q_load_shed_stack, 0.0, tol=1e-6)
    assert eq(B6.p_load_shed_stack, 0.05, tol=1e-6)
    assert eq(B6.q_load_shed_stack, 0.0, tol=1e-6)

def test_load_shed_isolated_half_hour():
    ps = initialize_network(
        island_mode=True,
    )

    B1 = ps.get_comp("B1")
    B2 = ps.get_comp("B2")
    B3 = ps.get_comp("B3")
    B4 = ps.get_comp("B4")
    B5 = ps.get_comp("B5")
    B6 = ps.get_comp("B6")

    B1.add_load(
        pload=0,
        qload=0,
    )
    B2.add_load(
        pload=0.05,
        qload=0,
    )
    B3.add_load(
        pload=0.04,
        qload=0,
    )
    B4.add_load(
        pload=0.03,
        qload=0,
    )
    B5.add_load(
        pload=0.07,
        qload=0,
    )
    B6.add_load(
        pload=0.05,
        qload=0,
    )
    
    B1.set_cost(1)
    B2.set_cost(1)
    B3.set_cost(1)
    B4.set_cost(1)
    B5.set_cost(1)
    B6.set_cost(1)

    B1.set_slack()

    run_bfs_load_flow(ps, maxit=5)

    assert eq(B1.vomag, 1, tol=1e-6)
    assert eq(B2.vomag, 0.999752, tol=1e-6)
    assert eq(B3.vomag, 0.999555, tol=1e-6)
    assert eq(B4.vomag, 0.999452, tol=1e-6)
    assert eq(B5.vomag, 0.999380, tol=1e-6)
    assert eq(B6.vomag, 0.999504, tol=1e-6)

    assert eq(np.degrees(B1.voang), 0.0, tol=1e-6)
    assert eq(np.degrees(B2.voang), -0.014209, tol=1e-6)
    assert eq(np.degrees(B3.voang), -0.025463, tol=1e-6)
    assert eq(np.degrees(B4.voang), -0.031388, tol=1e-6)
    assert eq(np.degrees(B5.voang), -0.035536, tol=1e-6)
    assert eq(np.degrees(B6.voang), -0.028425, tol=1e-6)

    shed_loads(
        power_system=ps,
        dt=Time(0.5, TimeUnit.HOUR),
        alpha=1e-7,
    )

    assert eq(B1.p_load_shed_stack, 0.0, tol=1e-6)
    assert eq(B1.q_load_shed_stack, 0.0, tol=1e-6)
    assert eq(B2.p_load_shed_stack, 0.025, tol=1e-6)
    assert eq(B2.q_load_shed_stack, 0.0, tol=1e-6)
    assert eq(B3.p_load_shed_stack, 0.02, tol=1e-6)
    assert eq(B3.q_load_shed_stack, 0.0, tol=1e-6)
    assert eq(B4.p_load_shed_stack, 0.015, tol=1e-6)
    assert eq(B4.q_load_shed_stack, 0.0, tol=1e-6)
    assert eq(B5.p_load_shed_stack, 0.035, tol=1e-6)
    assert eq(B5.q_load_shed_stack, 0.0, tol=1e-6)
    assert eq(B6.p_load_shed_stack, 0.025, tol=1e-6)
    assert eq(B6.q_load_shed_stack, 0.0, tol=1e-6)