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
    capacity = 100

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
        capacity=capacity,
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
        capacity=capacity,
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
        capacity=capacity,
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
        capacity=capacity,
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
        capacity=capacity,
    )

    CircuitBreaker("E1", L1)

    tn = Transmission(ps, trafo_bus=B1)
    dn = Distribution(parent_network=tn, connected_line=L1)
    dn.add_buses([B2, B3, B4, B5, B6])
    dn.add_lines([L2, L3, L4, L5])
    return ps


def test_run_increment():
    pass


def test_run_sequence():
    pass


def test_run_iteration():
    pass


def test_run_monte_carlo():
    pass
