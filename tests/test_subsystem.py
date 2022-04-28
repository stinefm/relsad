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
from relsad.simulation.system_config import find_sub_systems
import numpy as np
from relsad.Time import (
    Time,
    TimeUnit,
)


def initialize_network(
    island_mode: bool=False,
):

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

    D2 = Disconnector("D2", L2, B2)
    D3 = Disconnector("D3", L3, B3)

    E1 = CircuitBreaker("E1", L1)

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

def test_system_load_balance_active_load():
    ps = initialize_network(island_mode=True)
    B1 = ps.get_comp("B1")
    B2 = ps.get_comp("B2")
    B3 = ps.get_comp("B3")
    B4 = ps.get_comp("B4")
    B5 = ps.get_comp("B5")
    B6 = ps.get_comp("B6")
    
    B1.add_load_data(
        pload_data=np.array([0]),
        qload_data=np.array([0]),
    )
    B2.add_load_data(
        pload_data=np.array([0.05]),
        qload_data=np.array([0]),
    )
    B3.add_load_data(
        pload_data=np.array([0.04]),
        qload_data=np.array([0]),
    )
    B4.add_load_data(
        pload_data=np.array([0.03]),
        qload_data=np.array([0]),
    )
    B5.add_load_data(
        pload_data=np.array([0.02]),
        qload_data=np.array([0]),
    )
    B6.add_load_data(
        pload_data=np.array([0.05]),
        qload_data=np.array([0]),
    )

    curr_time = Time(0)
    ps.set_load_and_cost(inc_idx=0)
    find_sub_systems(ps, curr_time)

    sub_system = ps.sub_systems[0]

    system_load_balance_p, system_load_balance_q = sub_system.get_system_load_balance()

    assert eq(system_load_balance_p, 0.19, tol=1e-6)
    assert eq(system_load_balance_q, 0, tol=1e-6)

def test_system_load_balance_reactive_load():
    ps = initialize_network(island_mode=True)
    B1 = ps.get_comp("B1")
    B2 = ps.get_comp("B2")
    B3 = ps.get_comp("B3")
    B4 = ps.get_comp("B4")
    B5 = ps.get_comp("B5")
    B6 = ps.get_comp("B6")
    
    B1.add_load_data(
        pload_data=np.array([0]),
        qload_data=np.array([0]),
    )
    B2.add_load_data(
        pload_data=np.array([0.05]),
        qload_data=np.array([0.05]),
    )
    B3.add_load_data(
        pload_data=np.array([0.04]),
        qload_data=np.array([0.04]),
    )
    B4.add_load_data(
        pload_data=np.array([0.03]),
        qload_data=np.array([0.03]),
    )
    B5.add_load_data(
        pload_data=np.array([0.02]),
        qload_data=np.array([0.02]),
    )
    B6.add_load_data(
        pload_data=np.array([0.05]),
        qload_data=np.array([0.05]),
    )

    ps.set_load_and_cost(inc_idx=0)

    curr_time = Time(0)
    ps.set_load_and_cost(inc_idx=0)
    find_sub_systems(ps, curr_time)

    sub_system = ps.sub_systems[0]

    system_load_balance_p, system_load_balance_q = sub_system.get_system_load_balance()

    assert eq(system_load_balance_p, 0.19, tol=1e-6)
    assert eq(system_load_balance_q, 0.19, tol=1e-6)

def test_system_load_balance_active_power_high():
    ps = initialize_network(island_mode=True)
    B1 = ps.get_comp("B1")
    B2 = ps.get_comp("B2")
    B3 = ps.get_comp("B3")
    B4 = ps.get_comp("B4")
    B5 = ps.get_comp("B5")
    B6 = ps.get_comp("B6")
    
    B1.add_load_data(
        pload_data=np.array([0]),
        qload_data=np.array([0]),
    )
    B2.add_load_data(
        pload_data=np.array([-0.05]),
        qload_data=np.array([0.05]),
    )
    B3.add_load_data(
        pload_data=np.array([-0.04]),
        qload_data=np.array([0.04]),
    )
    B4.add_load_data(
        pload_data=np.array([0.03]),
        qload_data=np.array([0.03]),
    )
    B5.add_load_data(
        pload_data=np.array([-0.02]),
        qload_data=np.array([0.02]),
    )
    B6.add_load_data(
        pload_data=np.array([0.05]),
        qload_data=np.array([0.05]),
    )

    ps.set_load_and_cost(inc_idx=0)

    curr_time = Time(0)
    ps.set_load_and_cost(inc_idx=0)
    find_sub_systems(ps, curr_time)

    sub_system = ps.sub_systems[0]

    system_load_balance_p, system_load_balance_q = sub_system.get_system_load_balance()

    assert eq(system_load_balance_p, -0.03, tol=1e-6)
    assert eq(system_load_balance_q, 0.19, tol=1e-6)

def test_system_load_balance_reactive_power_high():
    ps = initialize_network(island_mode=True)
    B1 = ps.get_comp("B1")
    B2 = ps.get_comp("B2")
    B3 = ps.get_comp("B3")
    B4 = ps.get_comp("B4")
    B5 = ps.get_comp("B5")
    B6 = ps.get_comp("B6")
    
    B1.add_load_data(
        pload_data=np.array([0]),
        qload_data=np.array([0]),
    )
    B2.add_load_data(
        pload_data=np.array([0.05]),
        qload_data=np.array([0.05]),
    )
    B3.add_load_data(
        pload_data=np.array([0.04]),
        qload_data=np.array([-0.04]),
    )
    B4.add_load_data(
        pload_data=np.array([0.03]),
        qload_data=np.array([-0.03]),
    )
    B5.add_load_data(
        pload_data=np.array([0.02]),
        qload_data=np.array([-0.02]),
    )
    B6.add_load_data(
        pload_data=np.array([0.05]),
        qload_data=np.array([-0.05]),
    )

    ps.set_load_and_cost(inc_idx=0)

    curr_time = Time(0)
    ps.set_load_and_cost(inc_idx=0)
    find_sub_systems(ps, curr_time)

    sub_system = ps.sub_systems[0]

    system_load_balance_p, system_load_balance_q = sub_system.get_system_load_balance()

    assert eq(system_load_balance_p, 0.19, tol=1e-6)
    assert eq(system_load_balance_q, -0.09, tol=1e-6)

def test_system_load_balance_active_reactive_power_high():
    ps = initialize_network(island_mode=True)
    B1 = ps.get_comp("B1")
    B2 = ps.get_comp("B2")
    B3 = ps.get_comp("B3")
    B4 = ps.get_comp("B4")
    B5 = ps.get_comp("B5")
    B6 = ps.get_comp("B6")
    
    B1.add_load_data(
        pload_data=np.array([0]),
        qload_data=np.array([0]),
    )
    B2.add_load_data(
        pload_data=np.array([-0.05]),
        qload_data=np.array([0.05]),
    )
    B3.add_load_data(
        pload_data=np.array([-0.04]),
        qload_data=np.array([-0.04]),
    )
    B4.add_load_data(
        pload_data=np.array([0.03]),
        qload_data=np.array([-0.03]),
    )
    B5.add_load_data(
        pload_data=np.array([-0.02]),
        qload_data=np.array([-0.02]),
    )
    B6.add_load_data(
        pload_data=np.array([0.05]),
        qload_data=np.array([-0.05]),
    )

    ps.set_load_and_cost(inc_idx=0)

    curr_time = Time(0)
    ps.set_load_and_cost(inc_idx=0)
    find_sub_systems(ps, curr_time)

    sub_system = ps.sub_systems[0]

    system_load_balance_p, system_load_balance_q = sub_system.get_system_load_balance()

    assert eq(system_load_balance_p, -0.03, tol=1e-6)
    assert eq(system_load_balance_q, -0.09, tol=1e-6)

def test_system_load_balance_active_reactive_power_low():
    ps = initialize_network(island_mode=True)
    B1 = ps.get_comp("B1")
    B2 = ps.get_comp("B2")
    B3 = ps.get_comp("B3")
    B4 = ps.get_comp("B4")
    B5 = ps.get_comp("B5")
    B6 = ps.get_comp("B6")
    
    B1.add_load_data(
        pload_data=np.array([0]),
        qload_data=np.array([0]),
    )
    B2.add_load_data(
        pload_data=np.array([-0.05]),
        qload_data=np.array([0.05]),
    )
    B3.add_load_data(
        pload_data=np.array([0.04]),
        qload_data=np.array([-0.04]),
    )
    B4.add_load_data(
        pload_data=np.array([0.03]),
        qload_data=np.array([0.03]),
    )
    B5.add_load_data(
        pload_data=np.array([0.02]),
        qload_data=np.array([0.02]),
    )
    B6.add_load_data(
        pload_data=np.array([0.05]),
        qload_data=np.array([0.05]),
    )

    ps.set_load_and_cost(inc_idx=0)

    curr_time = Time(0)
    ps.set_load_and_cost(inc_idx=0)
    find_sub_systems(ps, curr_time)

    sub_system = ps.sub_systems[0]

    system_load_balance_p, system_load_balance_q = sub_system.get_system_load_balance()

    assert eq(system_load_balance_p, 0.09, tol=1e-6)
    assert eq(system_load_balance_q, 0.11, tol=1e-6)