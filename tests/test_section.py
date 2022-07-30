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


def initialize_network(
    include_ICT: bool = False,
    circuitbreaker_placement: str = "L1",
    disconnector_placement: str = "L1_B1",
):

    if include_ICT:
        C1 = MainController(name="C1")
    else:
        C1 = ManualMainController(name="C1", sectioning_time=Time(0))

    ps = PowerSystem(C1)

    B1 = Bus(name="B1", n_customers=0, coordinate=[0, 0])
    B2 = Bus(name="B2", n_customers=1, coordinate=[0, -1])
    B3 = Bus(name="B3", n_customers=1, coordinate=[0, -2])
    B4 = Bus(name="B4", n_customers=1, coordinate=[-1, -3])
    B5 = Bus(name="B5", n_customers=1, coordinate=[-1, -4])
    B6 = Bus(name="B6", n_customers=1, coordinate=[1, -3])

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

    if disconnector_placement == "L1_B1":
        D1 = Disconnector("D1", L1, B1)
    elif disconnector_placement == "L2_B2":
        D1 = Disconnector("D1", L2, B2)
    elif disconnector_placement == "L3_B3":
        D1 = Disconnector("D1", L3, B3)
    elif disconnector_placement == "L4_B4":
        D1 = Disconnector("D1", L4, B4)
    elif disconnector_placement == "L5_B3":
        D1 = Disconnector("D1", L5, B3)
    else:
        raise Exception("Invalid placement of disconnector")

    if include_ICT:
        IntelligentSwitch("ISW1", D1)

    if circuitbreaker_placement == "L1":
        connected_line = L1
    elif circuitbreaker_placement == "L2":
        connected_line = L2
    elif circuitbreaker_placement == "L3":
        connected_line = L3
    elif circuitbreaker_placement == "L4":
        connected_line = L4
    elif circuitbreaker_placement == "L5":
        connected_line = L5
    else:
        raise Exception("Invalid placement of circuitbreaker")

    CircuitBreaker("E1", connected_line)

    tn = Transmission(ps, trafo_bus=B1)
    dn = Distribution(parent_network=tn, connected_line=connected_line)
    dn.add_buses([B2, B3, B4, B5, B6])
    dn.add_lines(list(set([L1, L2, L3, L4, L5]) - set([connected_line])))
    return ps


def test_connect():
    ps = initialize_network(include_ICT=True)

    section = Section(
        parent_section=None,
        lines=ps.lines,
        switches=ps.disconnectors + ps.circuitbreakers,
    )

    ps.get_comp("ISW1").state = IntelligentSwitchState.OK

    dt = Time(1, TimeUnit.HOUR)

    section.connect(dt, ps.controller)

    assert ps.get_comp("L1").connected is True
    assert ps.get_comp("L2").connected is True
    assert ps.get_comp("L3").connected is True
    assert ps.get_comp("L4").connected is True
    assert ps.get_comp("L5").connected is True
    assert ps.get_comp("D1").is_open is False


def test_connect_manually():
    ps = initialize_network(include_ICT=False)

    section = Section(
        parent_section=None,
        lines=ps.lines,
        switches=ps.disconnectors + ps.circuitbreakers,
    )

    section.connect_manually()

    assert ps.get_comp("L1").connected is True
    assert ps.get_comp("L2").connected is True
    assert ps.get_comp("L3").connected is True
    assert ps.get_comp("L4").connected is True
    assert ps.get_comp("L5").connected is True
    assert ps.get_comp("D1").is_open is False


def test_disconnect():
    ps = initialize_network(include_ICT=False)

    section = Section(
        parent_section=None,
        lines=ps.lines,
        switches=ps.disconnectors + ps.circuitbreakers,
    )

    section.disconnect()

    assert ps.get_comp("L1").connected is False
    assert ps.get_comp("L2").connected is False
    assert ps.get_comp("L3").connected is False
    assert ps.get_comp("L4").connected is False
    assert ps.get_comp("L5").connected is False
    assert ps.get_comp("D1").is_open is True


def test_sectioning_cb_L1():
    ps = initialize_network(
        include_ICT=True,
        circuitbreaker_placement="L1",
    )

    ps.create_sections()

    dist_network = ps.child_network_list[1]

    assert ps.get_comp("L1") in dist_network.sections[0].lines
    assert ps.get_comp("L2") in dist_network.sections[0].lines
    assert ps.get_comp("L3") in dist_network.sections[0].lines
    assert ps.get_comp("L4") in dist_network.sections[0].lines
    assert ps.get_comp("L5") in dist_network.sections[0].lines


def test_sectioning_cb_L2():
    ps = initialize_network(
        include_ICT=True,
        circuitbreaker_placement="L2",
    )

    ps.create_sections()

    dist_network = ps.child_network_list[1]

    assert ps.get_comp("L2") in dist_network.sections[0].lines
    assert ps.get_comp("L3") in dist_network.sections[0].lines
    assert ps.get_comp("L4") in dist_network.sections[0].lines
    assert ps.get_comp("L5") in dist_network.sections[0].lines


def test_sectioning_cb_L3():
    ps = initialize_network(
        include_ICT=True,
        circuitbreaker_placement="L3",
    )

    ps.create_sections()

    dist_network = ps.child_network_list[1]

    assert ps.get_comp("L3") in dist_network.sections[0].lines
    assert ps.get_comp("L4") in dist_network.sections[0].lines


def test_sectioning_cb_L4():
    ps = initialize_network(
        include_ICT=True,
        circuitbreaker_placement="L4",
    )

    ps.create_sections()

    dist_network = ps.child_network_list[1]

    assert ps.get_comp("L4") in dist_network.sections[0].lines


def test_sectioning_cb_L5():
    ps = initialize_network(
        include_ICT=True,
        circuitbreaker_placement="L5",
    )

    ps.create_sections()

    dist_network = ps.child_network_list[1]

    assert ps.get_comp("L5") in dist_network.sections[0].lines


def test_sectioning_discon_L1_B1():
    ps = initialize_network(
        include_ICT=True,
        disconnector_placement="L1_B1",
    )

    ps.create_sections()

    dist_network = ps.child_network_list[1]

    assert ps.get_comp("L1") in dist_network.sections[0].lines
    assert ps.get_comp("L2") in dist_network.sections[0].lines
    assert ps.get_comp("L3") in dist_network.sections[0].lines
    assert ps.get_comp("L4") in dist_network.sections[0].lines
    assert ps.get_comp("L5") in dist_network.sections[0].lines


def test_sectioning_discon_L2_B2():
    ps = initialize_network(
        include_ICT=True,
        disconnector_placement="L2_B2",
    )

    ps.create_sections()

    dist_network = ps.child_network_list[1]

    assert ps.get_comp("L1") in dist_network.sections[0].lines
    assert ps.get_comp("L2") in dist_network.sections[1].lines
    assert ps.get_comp("L3") in dist_network.sections[1].lines
    assert ps.get_comp("L4") in dist_network.sections[1].lines
    assert ps.get_comp("L5") in dist_network.sections[1].lines


def test_sectioning_discon_L3_B3():
    ps = initialize_network(
        include_ICT=True,
        disconnector_placement="L3_B3",
    )

    ps.create_sections()

    dist_network = ps.child_network_list[1]

    assert ps.get_comp("L1") in dist_network.sections[0].lines
    assert ps.get_comp("L2") in dist_network.sections[0].lines
    assert ps.get_comp("L3") in dist_network.sections[1].lines
    assert ps.get_comp("L4") in dist_network.sections[1].lines
    assert ps.get_comp("L5") in dist_network.sections[0].lines


def test_sectioning_discon_L4_B4():
    ps = initialize_network(
        include_ICT=True,
        disconnector_placement="L4_B4",
    )

    ps.create_sections()

    dist_network = ps.child_network_list[1]

    assert ps.get_comp("L1") in dist_network.sections[0].lines
    assert ps.get_comp("L2") in dist_network.sections[0].lines
    assert ps.get_comp("L3") in dist_network.sections[0].lines
    assert ps.get_comp("L4") in dist_network.sections[1].lines
    assert ps.get_comp("L5") in dist_network.sections[0].lines


def test_sectioning_discon_L5_B3():
    ps = initialize_network(
        include_ICT=True,
        disconnector_placement="L5_B3",
    )

    ps.create_sections()

    dist_network = ps.child_network_list[1]

    assert ps.get_comp("L1") in dist_network.sections[0].lines
    assert ps.get_comp("L2") in dist_network.sections[0].lines
    assert ps.get_comp("L3") in dist_network.sections[0].lines
    assert ps.get_comp("L4") in dist_network.sections[0].lines
    assert ps.get_comp("L5") in dist_network.sections[1].lines
