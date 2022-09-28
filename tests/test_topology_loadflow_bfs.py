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
from relsad.topology.load_flow.bfs import is_cyclic
from relsad.Time import Time, TimeUnit


def initialize_network():

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

    L7 = Line(
        name="L7",
        fbus=B3,
        tbus=B5,
        r=r,
        x=x,
    )

    CircuitBreaker("E1", L1)

    tn = Transmission(ps, trafo_bus=B1)
    dn = Distribution(parent_network=tn, connected_line=L1)
    dn.add_buses([B2, B3, B4, B5, B6])
    dn.add_lines([L2, L3, L4, L5, L6, L7])
    return ps


def test_is_cyclic_1():
    ps = initialize_network()

    assert is_cyclic(ps) is True


def test_is_cyclic_2():
    ps = initialize_network()

    L6 = ps.get_comp("L6")

    L6.disconnect()

    assert is_cyclic(ps) is True 


def test_is_cyclic_3():
    ps = initialize_network()

    L6 = ps.get_comp("L6")
    L7 = ps.get_comp("L7")

    L6.disconnect()
    L7.disconnect()

    assert is_cyclic(ps) is False
