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

from relsad.simulation.system_config import (
    find_sub_systems,
    update_backup_lines_between_sub_systems,
    set_slack,
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

    r = 0.5
    x = 0.5

    L1 = Line(
        name="L1",
        fbus=B1,
        tbus=B2,
        r=r,
        x=x,
    )
    L2 = Line(
        name="L2",
        fbus=B2,
        tbus=B3,
        r=r, 
        x=x, 
    )
    L3 = Line(
        name="L3",
        fbus=B3,
        tbus=B4,
        r=r, 
        x=x,
    )
    L4 = Line(
        name="L4",
        fbus=B4,
        tbus=B5,
        r=r, 
        x=x,
    )
    L5 = Line(
        name="L5",
        fbus=B3,
        tbus=B6,
        r=r, 
        x=x,
    )
    L6 = Line(
        name="L6",
        fbus=B4,
        tbus=B6,
        r=r, 
        x=x,
    )
    D1 = Disconnector("D1", line=L6, bus=B4)

    L6.set_backup()

    E1 = CircuitBreaker("E1", L1)

    tn = Transmission(ps, trafo_bus=B1)
    dn = Distribution(parent_network=tn, connected_line=L1)
    dn.add_buses(
        [B2, B3, B4, B5, B6]
    )
    dn.add_lines(
        [L2, L3, L4, L5, L6]
    )
    return ps


def test_find_sub_systems():
    ps = initialize_network()

    curr_time = Time(0)

    find_sub_systems(ps, curr_time)

    assert len(ps.sub_systems) == 1
    assert ps.get_comp("L1") in ps.sub_systems[0].lines
    assert ps.get_comp("L2") in ps.sub_systems[0].lines
    assert ps.get_comp("L3") in ps.sub_systems[0].lines
    assert ps.get_comp("L4") in ps.sub_systems[0].lines
    assert ps.get_comp("L5") in ps.sub_systems[0].lines
    assert ps.get_comp("L6") not in ps.sub_systems[0].lines
    assert ps.get_comp("B1") in ps.sub_systems[0].buses
    assert ps.get_comp("B2") in ps.sub_systems[0].buses
    assert ps.get_comp("B3") in ps.sub_systems[0].buses
    assert ps.get_comp("B4") in ps.sub_systems[0].buses
    assert ps.get_comp("B5") in ps.sub_systems[0].buses
    assert ps.get_comp("B6") in ps.sub_systems[0].buses

def test_find_sub_systems_fail():
    ps = initialize_network()

    curr_time = Time(0)

    ps.get_comp("L3").disconnect()

    find_sub_systems(ps, curr_time)

    assert len(ps.sub_systems) == 1
    assert ps.get_comp("L1") in ps.sub_systems[0].lines
    assert ps.get_comp("L2") in ps.sub_systems[0].lines
    assert ps.get_comp("L3") not in ps.sub_systems[0].lines
    assert ps.get_comp("L4") in ps.sub_systems[0].lines
    assert ps.get_comp("L5") in ps.sub_systems[0].lines
    assert ps.get_comp("L6") in ps.sub_systems[0].lines
    assert ps.get_comp("B1") in ps.sub_systems[0].buses
    assert ps.get_comp("B2") in ps.sub_systems[0].buses
    assert ps.get_comp("B3") in ps.sub_systems[0].buses
    assert ps.get_comp("B4") in ps.sub_systems[0].buses
    assert ps.get_comp("B5") in ps.sub_systems[0].buses
    assert ps.get_comp("B6") in ps.sub_systems[0].buses

def test_set_slack():
    ps = initialize_network()

