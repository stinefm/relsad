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
from relsad.utils import eq
from relsad.Time import (
    Time,
    TimeUnit,
)

def initialize_network():

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

    tn = Transmission(ps, trafo_bus=B1)
    dn = Distribution(parent_network=tn, connected_line=L1)
    dn.add_buses(
        [B2, B3, B4, B5, B6]
    )
    dn.add_lines(
        [L2, L3, L4, L5]
    )
    return ps


def test_load_flow_normal_load():
    ps = initialize_network()

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

    run_bfs_load_flow(ps, maxit=5)

    assert eq(B1.vomag, 1, tol=1e-6)
    assert eq(B2.vomag, 0.999804, tol=1e-6)
    assert eq(B3.vomag, 0.999659, tol=1e-6)
    assert eq(B4.vomag, 0.999607, tol=1e-6)
    assert eq(B5.vomag, 0.999587, tol=1e-6)
    assert eq(B6.vomag, 0.999607, tol=1e-6)

    assert eq(np.degrees(B1.voang), 0.0, tol=1e-6)
    assert eq(np.degrees(B2.voang), -0.011248, tol=1e-6)
    assert eq(np.degrees(B3.voang), -0.019539, tol=1e-6)
    assert eq(np.degrees(B4.voang), -0.022501, tol=1e-6)
    assert eq(np.degrees(B5.voang), -0.023686, tol=1e-6)
    assert eq(np.degrees(B6.voang), -0.022501, tol=1e-6)


def test_load_flow_high_load():
    ps = initialize_network()

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

def test_load_flow_high_production():
    ps = initialize_network()

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

def test_load_flow_normal_production():
    ps = initialize_network()

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
