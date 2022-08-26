import numpy as np

from relsad.loadflow.ac import run_bfs_load_flow
from relsad.network.components import (
    Battery,
    Bus,
    CircuitBreaker,
    Disconnector,
    EVPark,
    Line,
    MainController,
    ManualMainController,
    Production,
)
from relsad.network.systems import (
    Distribution,
    Microgrid,
    PowerSystem,
    Transmission,
)
from relsad.Time import Time, TimeUnit
from relsad.utils import eq


def initialize_network(
    island_mode: bool = False,
    include_battery: bool = False,
    include_wind: bool = False,
    include_PV: bool = False,
    include_ev: bool = False,
    v2g_flag: bool = False,
):

    C1 = ManualMainController(name="C1", sectioning_time=Time(0))

    ps = PowerSystem(C1)

    B1 = Bus(name="B1", n_customers=0, coordinate=[0, 0])
    B2 = Bus(name="B2", n_customers=1, coordinate=[0, -1])
    B3 = Bus(name="B3", n_customers=1, coordinate=[0, -2])
    B4 = Bus(name="B4", n_customers=1, coordinate=[-1, -3])
    B5 = Bus(name="B5", n_customers=1, coordinate=[-1, -4])
    B6 = Bus(name="B6", n_customers=1, coordinate=[1, -3])

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

    CircuitBreaker("E1", L1)

    if include_battery:
        Battery(
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
        Production(name="wind", bus=B4)

    if include_PV:
        Production(name="PV", bus=B6)

    if include_ev:
        EVPark(name="EV1", bus=B2, num_ev_dist=1, v2g_flag=v2g_flag)
        EVPark(name="EV2", bus=B3, num_ev_dist=1, v2g_flag=v2g_flag)
        EVPark(name="EV3", bus=B4, num_ev_dist=1, v2g_flag=v2g_flag)
        EVPark(name="EV4", bus=B6, num_ev_dist=1, v2g_flag=v2g_flag)

    if island_mode:
        dn = Distribution(parent_network=ps, connected_line=None)
        dn.add_buses([B1, B2, B3, B4, B5, B6])
        dn.add_lines([L1, L2, L3, L4, L5])
    else:
        tn = Transmission(ps, trafo_bus=B1)
        dn = Distribution(parent_network=tn, connected_line=L1)
        dn.add_buses([B2, B3, B4, B5, B6])
        dn.add_lines([L2, L3, L4, L5])
    return ps


def test_load_flow_battery_charge():
    ps = initialize_network(
        include_battery=True,
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
        pload=0.02,
        qload=0,
    )
    B6.add_load(
        pload=0.05,
        qload=0,
    )

    battery = ps.get_comp("Bat1")
    dt = Time(1, TimeUnit.HOUR)
    fail_duration = Time(0)
    p, q = ps.get_system_load_balance()
    battery.update(
        p=p,
        q=q,
        fail_duration=fail_duration,
        dt=dt,
    )

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


def test_load_flow_battery_discharge():
    ps = initialize_network(
        island_mode=True,
        include_battery=True,
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

    battery = ps.get_comp("Bat1")
    dt = Time(1, TimeUnit.HOUR)
    fail_duration = Time(0)
    p, q = ps.get_system_load_balance()

    print(p, q)
    battery.update(
        p=p,
        q=q,
        fail_duration=fail_duration,
        dt=dt,
    )
    # Set slack bus
    B1.set_slack()

    run_bfs_load_flow(ps, maxit=5)

    print(B1.pload)
    print(B2.pload)
    print(B3.pload)
    print(B4.pload)
    print(B5.pload)
    print(B6.pload)

    print(B1.pprod)
    print(B2.pprod)
    print(B3.pprod)
    print(B4.pprod)
    print(B5.pprod)
    print(B6.pprod)

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
