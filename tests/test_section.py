from relsad.network.components import (
    Bus,
    Line,
    Disconnector,
    CircuitBreaker,
    MainController,
    ManualMainController,
    IntelligentSwitch,
    IntelligentSwitchState,
)
from relsad.network.systems import (
    PowerSystem,
    Distribution,
    Transmission,
)
from relsad.network.containers import Section
from relsad.utils import eq
import numpy as np
from relsad.Time import (
    Time,
    TimeUnit,
)


def initialize_network(include_ICT: bool = False):

    if include_ICT:
        C1 = MainController(name="C1")
    else:
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

    D1 = Disconnector("D1", L1, B1)

    if include_ICT:
        ISW1 = IntelligentSwitch("ISW1", D1)

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

def test_connect():
    ps = initialize_network(include_ICT=True)

    section = Section(
    parent=ps,
    lines=ps.lines,
    disconnectors=ps.disconnectors,
    )

    ps.get_comp("ISW1").state = IntelligentSwitchState.OK

    dt = Time(1, TimeUnit.HOUR)

    section.connect(dt)

    assert ps.get_comp("L1").connected == True
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == True
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == True
    assert ps.get_comp("D1").is_open == False

def test_connect_manually():
    ps = initialize_network(include_ICT=False)

    section = Section(
    parent=ps,
    lines=ps.lines,
    disconnectors=ps.disconnectors,
    )

    section.connect_manually()

    assert ps.get_comp("L1").connected == True
    assert ps.get_comp("L2").connected == True
    assert ps.get_comp("L3").connected == True
    assert ps.get_comp("L4").connected == True
    assert ps.get_comp("L5").connected == True
    assert ps.get_comp("D1").is_open == False

def test_disconnect():
    ps = initialize_network(include_ICT=False)

    section = Section(
    parent=ps,
    lines=ps.lines,
    disconnectors=ps.disconnectors,
    )

    section.disconnect()

    assert ps.get_comp("L1").connected == False
    assert ps.get_comp("L2").connected == False
    assert ps.get_comp("L3").connected == False
    assert ps.get_comp("L4").connected == False
    assert ps.get_comp("L5").connected == False
    assert ps.get_comp("D1").is_open == True
