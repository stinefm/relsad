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


def test_load_flow_normal_load():
    ps = initialize_network()

    B1 = ps.get_comp("B1")
    B2 = ps.get_comp("B2")
    B3 = ps.get_comp("B3")
    B4 = ps.get_comp("B4")
    B5 = ps.get_comp("B5")
    B6 = ps.get_comp("B6")

    L1 = ps.get_comp("L1")
    L2 = ps.get_comp("L2")
    L3 = ps.get_comp("L3")
    L4 = ps.get_comp("L4")
    L5 = ps.get_comp("L5")

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

    assert eq(L1.get_line_load()[0], 0.190063, tol=1e-6)
    assert eq(L2.get_line_load()[0], 0.140026, tol=1e-6)
    assert eq(L3.get_line_load()[0], 0.050003, tol=1e-6)
    assert eq(L4.get_line_load()[0], 0.020000, tol=1e-6)
    assert eq(L5.get_line_load()[0], 0.050003, tol=1e-6)

    assert eq(L1.ploss, 3.731819e-5, tol=1e-6)
    assert eq(L2.ploss, 2.026337e-5, tol=1e-6)
    assert eq(L3.ploss, 2.584717e-6, tol=1e-6)
    assert eq(L4.ploss, 4.135650e-7, tol=1e-6)
    assert eq(L5.ploss, 2.584675e-6, tol=1e-6)


def test_load_flow_high_load():
    ps = initialize_network()

    B1 = ps.get_comp("B1")
    B2 = ps.get_comp("B2")
    B3 = ps.get_comp("B3")
    B4 = ps.get_comp("B4")
    B5 = ps.get_comp("B5")
    B6 = ps.get_comp("B6")

    L1 = ps.get_comp("L1")
    L2 = ps.get_comp("L2")
    L3 = ps.get_comp("L3")
    L4 = ps.get_comp("L4")
    L5 = ps.get_comp("L5")

    B1.add_load(
        pload=0,
        qload=0,
    )
    B2.add_load(
        pload=19,
        qload=0,
    )
    B3.add_load(
        pload=19,
        qload=0,
    )
    B4.add_load(
        pload=19,
        qload=0,
    )
    B5.add_load(
        pload=19,
        qload=0,
    )
    B6.add_load(
        pload=20,
        qload=0,
    )

    run_bfs_load_flow(ps, maxit=45)

    assert eq(B1.vomag, 1, tol=1e-6)
    assert eq(B2.vomag, 0.807169, tol=1e-6)
    assert eq(B3.vomag, 0.653703, tol=1e-6)
    assert eq(B4.vomag, 0.577627, tol=1e-6)
    assert eq(B5.vomag, 0.540144, tol=1e-6)
    assert eq(B6.vomag, 0.619500, tol=1e-6)

    assert eq(np.degrees(B1.voang), 0.0, tol=1e-6)
    assert eq(np.degrees(B2.voang), -7.057533, tol=1e-6)
    assert eq(np.degrees(B3.voang), -15.728194, tol=1e-6)
    assert eq(np.degrees(B4.voang), -21.695640, tol=1e-6)
    assert eq(np.degrees(B5.voang), -25.302510, tol=1e-6)
    assert eq(np.degrees(B6.voang), -18.652644, tol=1e-6)

    assert eq(L1.get_line_load()[0], 144.290264, tol=1e-6)
    assert eq(L2.get_line_load()[0], 101.373291, tol=1e-6)
    assert eq(L3.get_line_load()[0], 44.060060, tol=1e-6)
    assert eq(L4.get_line_load()[0], 20.278240, tol=1e-6)
    assert eq(L5.get_line_load()[0], 21.076718, tol=1e-6)

    assert eq(L1.ploss, 23.916973, tol=1e-6)
    assert eq(L2.ploss, 17.236513, tol=1e-6)
    assert eq(L3.ploss, 4.781821, tol=1e-6)
    assert eq(L4.ploss, 1.278240, tol=1e-6)
    assert eq(L5.ploss, 1.076718, tol=1e-6)


def test_load_flow_normal_production():
    ps = initialize_network()

    B1 = ps.get_comp("B1")
    B2 = ps.get_comp("B2")
    B3 = ps.get_comp("B3")
    B4 = ps.get_comp("B4")
    B5 = ps.get_comp("B5")
    B6 = ps.get_comp("B6")

    L1 = ps.get_comp("L1")
    L2 = ps.get_comp("L2")
    L3 = ps.get_comp("L3")
    L4 = ps.get_comp("L4")
    L5 = ps.get_comp("L5")

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
        pload=-0.07,
        qload=0,
    )
    B6.add_load(
        pload=0.05,
        qload=0,
    )

    run_bfs_load_flow(ps, maxit=5)

    assert eq(B1.vomag, 1, tol=1e-6)
    assert eq(B2.vomag, 0.999897, tol=1e-6)
    assert eq(B3.vomag, 0.999845, tol=1e-6)
    assert eq(B4.vomag, 0.999886, tol=1e-6)
    assert eq(B5.vomag, 0.999959, tol=1e-6)
    assert eq(B6.vomag, 0.999793, tol=1e-6)

    assert eq(np.degrees(B1.voang), 0.0, tol=1e-6)
    assert eq(np.degrees(B2.voang), -0.005920, tol=1e-6)
    assert eq(np.degrees(B3.voang), -0.008880, tol=1e-6)
    assert eq(np.degrees(B4.voang), -0.006512, tol=1e-6)
    assert eq(np.degrees(B5.voang), -0.002368, tol=1e-6)
    assert eq(np.degrees(B6.voang), -0.011840, tol=1e-6)

    assert eq(L1.get_line_load()[0], 0.100022, tol=1e-6)
    assert eq(L2.get_line_load()[0], 0.050012, tol=1e-6)
    assert eq(L3.get_line_load()[0], -0.039993, tol=1e-6)
    assert eq(L4.get_line_load()[0], -0.069995, tol=1e-6)
    assert eq(L5.get_line_load()[0], 0.050003, tol=1e-6)

    assert eq(L1.ploss, 0.000010, tol=1e-6)
    assert eq(L2.ploss, 0.000003, tol=1e-6)
    assert eq(L3.ploss, 0.000002, tol=1e-6)
    assert eq(L4.ploss, 0.000005, tol=1e-6)
    assert eq(L5.ploss, 0.000003, tol=1e-6)


def test_load_flow_high_production():
    ps = initialize_network()

    B1 = ps.get_comp("B1")
    B2 = ps.get_comp("B2")
    B3 = ps.get_comp("B3")
    B4 = ps.get_comp("B4")
    B5 = ps.get_comp("B5")
    B6 = ps.get_comp("B6")

    L1 = ps.get_comp("L1")
    L2 = ps.get_comp("L2")
    L3 = ps.get_comp("L3")
    L4 = ps.get_comp("L4")
    L5 = ps.get_comp("L5")

    B1.add_load(
        pload=0,
        qload=0,
    )
    B2.add_load(
        pload=-0.05,
        qload=0,
    )
    B3.add_load(
        pload=-0.04,
        qload=0,
    )
    B4.add_load(
        pload=0.03,
        qload=0,
    )
    B5.add_load(
        pload=-0.07,
        qload=0,
    )
    B6.add_load(
        pload=0.05,
        qload=0,
    )

    run_bfs_load_flow(ps, maxit=5)

    assert eq(B1.vomag, 1, tol=1e-6)
    assert eq(B2.vomag, 1.000083, tol=1e-6)
    assert eq(B3.vomag, 1.000114, tol=1e-6)
    assert eq(B4.vomag, 1.000155, tol=1e-6)
    assert eq(B5.vomag, 1.000227, tol=1e-6)
    assert eq(B6.vomag, 1.000062, tol=1e-6)

    assert eq(np.degrees(B1.voang), 0.0, tol=1e-6)
    assert eq(np.degrees(B2.voang), 0.004735, tol=1e-6)
    assert eq(np.degrees(B3.voang), 0.006510, tol=1e-6)
    assert eq(np.degrees(B4.voang), 0.008877, tol=1e-6)
    assert eq(np.degrees(B5.voang), 0.013019, tol=1e-6)
    assert eq(np.degrees(B6.voang), 0.003551, tol=1e-6)

    assert eq(L1.get_line_load()[0], -0.079983, tol=1e-6)
    assert eq(L2.get_line_load()[0], -0.029990, tol=1e-6)
    assert eq(L3.get_line_load()[0], -0.039993, tol=1e-6)
    assert eq(L4.get_line_load()[0], -0.069995, tol=1e-6)
    assert eq(L5.get_line_load()[0], 0.050003, tol=1e-6)

    assert eq(L1.ploss, 6.608788e-6, tol=1e-6)
    assert eq(L2.ploss, 9.289648e-7, tol=1e-6)
    assert eq(L3.ploss, 1.651962e-6, tol=1e-6)
    assert eq(L4.ploss, 5.059683e-6, tol=1e-6)
    assert eq(L5.ploss, 2.582324e-6, tol=1e-6)


def test_load_flow_reactive_normal():
    ps = initialize_network()

    B1 = ps.get_comp("B1")
    B2 = ps.get_comp("B2")
    B3 = ps.get_comp("B3")
    B4 = ps.get_comp("B4")
    B5 = ps.get_comp("B5")
    B6 = ps.get_comp("B6")

    L1 = ps.get_comp("L1")
    L2 = ps.get_comp("L2")
    L3 = ps.get_comp("L3")
    L4 = ps.get_comp("L4")
    L5 = ps.get_comp("L5")

    B1.add_load(
        pload=0,
        qload=0,
    )
    B2.add_load(
        pload=0.05,
        qload=0.005,
    )
    B3.add_load(
        pload=0.04,
        qload=0.004,
    )
    B4.add_load(
        pload=0.03,
        qload=0.003,
    )
    B5.add_load(
        pload=0.02,
        qload=0.002,
    )
    B6.add_load(
        pload=0.05,
        qload=0.005,
    )

    run_bfs_load_flow(ps, maxit=60)

    print(B1.vomag)
    print(B2.vomag)
    print(B3.vomag)
    print(B4.vomag)
    print(B5.vomag)
    print(B6.vomag)

    assert eq(B1.vomag, 1, tol=1e-6)
    assert eq(B2.vomag, 0.999784, tol=1e-6)
    assert eq(B3.vomag, 0.999625, tol=1e-6)
    assert eq(B4.vomag, 0.999568, tol=1e-6)
    assert eq(B5.vomag, 0.999545, tol=1e-6)
    assert eq(B6.vomag, 0.999568, tol=1e-6)

    assert eq(np.degrees(B1.voang), 0.0, tol=1e-6)
    assert eq(np.degrees(B2.voang), -0.010124, tol=1e-6)
    assert eq(np.degrees(B3.voang), -0.017586, tol=1e-6)
    assert eq(np.degrees(B4.voang), -0.020252, tol=1e-6)
    assert eq(np.degrees(B5.voang), -0.021318, tol=1e-6)
    assert eq(np.degrees(B6.voang), -0.020252, tol=1e-6)

    assert eq(L1.get_line_load()[0], 0.190064, tol=1e-6)
    assert eq(L2.get_line_load()[0], 0.140026, tol=1e-6)
    assert eq(L3.get_line_load()[0], 0.050003, tol=1e-6)
    assert eq(L4.get_line_load()[0], 0.020000, tol=1e-6)
    assert eq(L5.get_line_load()[0], 0.050003, tol=1e-6)

    assert eq(L1.get_line_load()[1], 0.019064, tol=1e-6)
    assert eq(L2.get_line_load()[1], 0.014026, tol=1e-6)
    assert eq(L3.get_line_load()[1], 0.005003, tol=1e-6)
    assert eq(L4.get_line_load()[1], 0.002000, tol=1e-6)
    assert eq(L5.get_line_load()[1], 0.005003, tol=1e-6)

    assert eq(L1.ploss, 3.769388e-5, tol=1e-6)
    assert eq(L2.ploss, 2.046756e-5, tol=1e-6)
    assert eq(L3.ploss, 2.610774e-6, tol=1e-6)
    assert eq(L4.ploss, 4.177352e-7, tol=1e-6)
    assert eq(L5.ploss, 2.610726e-6, tol=1e-6)

    assert eq(L1.qloss, 3.769388e-5, tol=1e-6)
    assert eq(L2.qloss, 2.046756e-5, tol=1e-6)
    assert eq(L3.qloss, 2.610774e-6, tol=1e-6)
    assert eq(L4.qloss, 4.177352e-7, tol=1e-6)
    assert eq(L5.qloss, 2.61072e-6, tol=1e-6)


def test_load_flow_reactive_high():
    ps = initialize_network()

    B1 = ps.get_comp("B1")
    B2 = ps.get_comp("B2")
    B3 = ps.get_comp("B3")
    B4 = ps.get_comp("B4")
    B5 = ps.get_comp("B5")
    B6 = ps.get_comp("B6")

    L1 = ps.get_comp("L1")
    L2 = ps.get_comp("L2")
    L3 = ps.get_comp("L3")
    L4 = ps.get_comp("L4")
    L5 = ps.get_comp("L5")

    B1.add_load(
        pload=0,
        qload=0,
    )
    B2.add_load(
        pload=0.05,
        qload=5,
    )
    B3.add_load(
        pload=0.04,
        qload=4,
    )
    B4.add_load(
        pload=0.03,
        qload=3,
    )
    B5.add_load(
        pload=0.02,
        qload=2,
    )
    B6.add_load(
        pload=0.05,
        qload=5,
    )

    run_bfs_load_flow(ps, maxit=60)

    assert eq(B1.vomag, 1, tol=1e-6)
    assert eq(B2.vomag, 0.978960, tol=1e-6)
    assert eq(B3.vomag, 0.963557, tol=1e-6)
    assert eq(B4.vomag, 0.958087, tol=1e-6)
    assert eq(B5.vomag, 0.955901, tol=1e-6)
    assert eq(B6.vomag, 0.958097, tol=1e-6)

    assert eq(np.degrees(B1.voang), 0.0, tol=1e-6)
    assert eq(np.degrees(B2.voang), 1.137365, tol=1e-6)
    assert eq(np.degrees(B3.voang), 2.007096, tol=1e-6)
    assert eq(np.degrees(B4.voang), 2.324471, tol=1e-6)
    assert eq(np.degrees(B5.voang), 2.452437, tol=1e-6)
    assert eq(np.degrees(B6.voang), 2.324468, tol=1e-6)

    assert eq(L1.get_line_load()[0], 0.871846, tol=1e-6)
    assert eq(L2.get_line_load()[0], 0.420880, tol=1e-6)
    assert eq(L3.get_line_load()[0], 0.082713, tol=1e-6)
    assert eq(L4.get_line_load()[0], 0.024523, tol=1e-6)
    assert eq(L5.get_line_load()[0], 0.078138, tol=1e-6)

    assert eq(L1.get_line_load()[1], 19.681846, tol=1e-6)
    assert eq(L2.get_line_load()[1], 14.280880, tol=1e-6)
    assert eq(L3.get_line_load()[1], 5.032713, tol=1e-6)
    assert eq(L4.get_line_load()[1], 2.004523, tol=1e-6)
    assert eq(L5.get_line_load()[1], 5.028138, tol=1e-6)

    assert eq(L1.ploss, 0.400966, tol=1e-6)
    assert eq(L2.ploss, 0.220030, tol=1e-6)
    assert eq(L3.ploss, 0.028190, tol=1e-6)
    assert eq(L4.ploss, 0.004523, tol=1e-6)
    assert eq(L5.ploss, 0.028138, tol=1e-6)

    assert eq(L1.qloss, 0.400966, tol=1e-6)
    assert eq(L2.qloss, 0.220030, tol=1e-6)
    assert eq(L3.qloss, 0.028190, tol=1e-6)
    assert eq(L4.qloss, 0.004523, tol=1e-6)
    assert eq(L5.qloss, 0.028138, tol=1e-6)


def test_load_flow_reactive_active_high():
    ps = initialize_network()

    B1 = ps.get_comp("B1")
    B2 = ps.get_comp("B2")
    B3 = ps.get_comp("B3")
    B4 = ps.get_comp("B4")
    B5 = ps.get_comp("B5")
    B6 = ps.get_comp("B6")

    L1 = ps.get_comp("L1")
    L2 = ps.get_comp("L2")
    L3 = ps.get_comp("L3")
    L4 = ps.get_comp("L4")
    L5 = ps.get_comp("L5")

    B1.add_load(
        pload=0,
        qload=0,
    )
    B2.add_load(
        pload=15,
        qload=5,
    )
    B3.add_load(
        pload=15,
        qload=4,
    )
    B4.add_load(
        pload=15,
        qload=3,
    )
    B5.add_load(
        pload=15,
        qload=2,
    )
    B6.add_load(
        pload=15,
        qload=5,
    )

    run_bfs_load_flow(ps, maxit=80)

    assert eq(B1.vomag, 1, tol=1e-6)
    assert eq(B2.vomag, 0.857667, tol=1e-6)
    assert eq(B3.vomag, 0.743768, tol=1e-6)
    assert eq(B4.vomag, 0.688702, tol=1e-6)
    assert eq(B5.vomag, 0.661869, tol=1e-6)
    assert eq(B6.vomag, 0.714720, tol=1e-6)

    assert eq(np.degrees(B1.voang), 0.0, tol=1e-6)
    assert eq(np.degrees(B2.voang), -3.867644, tol=1e-6)
    assert eq(np.degrees(B3.voang), -8.139842, tol=1e-6)
    assert eq(np.degrees(B4.voang), -11.029875, tol=1e-6)
    assert eq(np.degrees(B5.voang), -12.718178, tol=1e-6)
    assert eq(np.degrees(B6.voang), -9.253371, tol=1e-6)

    assert eq(L1.get_line_load()[0], 97.834579, tol=1e-6)
    assert eq(L2.get_line_load()[0], 71.138570, tol=1e-6)
    assert eq(L3.get_line_load()[0], 32.638302, tol=1e-6)
    assert eq(L4.get_line_load()[0], 15.540028, tol=1e-6)
    assert eq(L5.get_line_load()[0], 15.505584, tol=1e-6)

    assert eq(L1.get_line_load()[1], 41.834579, tol=1e-6)
    assert eq(L2.get_line_load()[1], 25.138570, tol=1e-6)
    assert eq(L3.get_line_load()[1], 7.638302, tol=1e-6)
    assert eq(L4.get_line_load()[1], 2.540028, tol=1e-6)
    assert eq(L5.get_line_load()[1], 5.505584, tol=1e-6)

    assert eq(L1.ploss, 11.696009, tol=1e-6)
    assert eq(L2.ploss, 7.994683, tol=1e-6)
    assert eq(L3.ploss, 2.098274, tol=1e-6)
    assert eq(L4.ploss, 0.540028, tol=1e-6)
    assert eq(L5.ploss, 0.505584, tol=1e-6)

    assert eq(L1.qloss, 11.696009, tol=1e-6)
    assert eq(L2.qloss, 7.994683, tol=1e-6)
    assert eq(L3.qloss, 2.098274, tol=1e-6)
    assert eq(L4.qloss, 0.540028, tol=1e-6)
    assert eq(L5.qloss, 0.505584, tol=1e-6)


def test_load_flow_active_reactive_production():
    ps = initialize_network()

    B1 = ps.get_comp("B1")
    B2 = ps.get_comp("B2")
    B3 = ps.get_comp("B3")
    B4 = ps.get_comp("B4")
    B5 = ps.get_comp("B5")
    B6 = ps.get_comp("B6")

    L1 = ps.get_comp("L1")
    L2 = ps.get_comp("L2")
    L3 = ps.get_comp("L3")
    L4 = ps.get_comp("L4")
    L5 = ps.get_comp("L5")

    B1.add_load(
        pload=0,
        qload=0,
    )
    B2.add_load(
        pload=-0.05,
        qload=0.005,
    )
    B3.add_load(
        pload=0.04,
        qload=-0.004,
    )
    B4.add_load(
        pload=-0.03,
        qload=0.003,
    )
    B5.add_load(
        pload=0.02,
        qload=-0.002,
    )
    B6.add_load(
        pload=-0.05,
        qload=-0.005,
    )

    run_bfs_load_flow(ps, maxit=60)

    print(B1.vomag)
    print(B2.vomag)
    print(B3.vomag)
    print(B4.vomag)
    print(B5.vomag)
    print(B6.vomag)

    assert eq(B1.vomag, 1, tol=1e-6)
    assert eq(B2.vomag, 1.000075, tol=1e-6)
    assert eq(B3.vomag, 1.000104, tol=1e-6)
    assert eq(B4.vomag, 1.000114, tol=1e-6)
    assert eq(B5.vomag, 1.000095, tol=1e-6)
    assert eq(B6.vomag, 1.000161, tol=1e-6)

    assert eq(np.degrees(B1.voang), 0.0, tol=1e-6)
    assert eq(np.degrees(B2.voang), 0.003965, tol=1e-6)
    assert eq(np.degrees(B3.voang), 0.004676, tol=1e-6)
    assert eq(np.degrees(B4.voang), 0.005327, tol=1e-6)
    assert eq(np.degrees(B5.voang), 0.004025, tol=1e-6)
    assert eq(np.degrees(B6.voang), 0.007338, tol=1e-6)

    assert eq(L1.get_line_load()[0], -0.069991, tol=1e-6)
    assert eq(L2.get_line_load()[0], -0.019996, tol=1e-6)
    assert eq(L3.get_line_load()[0], -0.009999, tol=1e-6)
    assert eq(L4.get_line_load()[0], 0.02000, tol=1e-6)
    assert eq(L5.get_line_load()[0], -0.049997, tol=1e-6)

    assert eq(L1.get_line_load()[1], -0.002991, tol=1e-6)
    assert eq(L2.get_line_load()[1], -0.007996, tol=1e-6)
    assert eq(L3.get_line_load()[1], 0.001001, tol=1e-6)
    assert eq(L4.get_line_load()[1], -0.002000, tol=1e-6)
    assert eq(L5.get_line_load()[1], -0.004997, tol=1e-6)

    assert eq(L1.ploss, 5.069972e-6, tol=1e-6)
    assert eq(L2.ploss, 4.790578e-7, tol=1e-6)
    assert eq(L3.ploss, 1.043074e-7, tol=1e-6)
    assert eq(L4.ploss, 4.172760e-7, tol=1e-6)
    assert eq(L5.ploss, 2.607630e-6, tol=1e-6)

    assert eq(L1.qloss, 5.069972e-6, tol=1e-6)
    assert eq(L2.qloss, 4.790578e-7, tol=1e-6)
    assert eq(L3.qloss, 1.043074e-7, tol=1e-6)
    assert eq(L4.qloss, 4.172760e-7, tol=1e-6)
    assert eq(L5.qloss, 2.607630e-6, tol=1e-6)
