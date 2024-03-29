from relsad.examples.CINELDI.network import initialize_network
from relsad.network.components import MicrogridMode
from relsad.simulation.system_config import find_sub_systems
from relsad.StatDist import StatDist, StatDistType, UniformParameters
from relsad.Time import Time, TimeUnit


class MyError(Exception):
    def __init__(self, m):
        self.m = m

    def __str__(self):
        return self.m


def test_B2_trafo_fail():
    ps = initialize_network(
        include_ICT=False,
        microgrid_mode=MicrogridMode.LIMITED_SUPPORT,
    )

    # Create sections
    ps.create_sections()

    # Simulate failure at time 0
    # Time = 0
    curr_time = Time(0)
    dt = Time(1, TimeUnit.HOUR)

    ps.get_comp("B2").trafo_fail(dt)

    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    # Time = 1
    curr_time = Time(1)
    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    assert ps.get_comp("L1").connected is True
    assert ps.get_comp("L2").connected is True
    assert ps.get_comp("L3").connected is True
    assert ps.get_comp("L4").connected is True
    assert ps.get_comp("L5").connected is True
    assert ps.get_comp("L6").connected is False
    assert ps.get_comp("L7").connected is True
    assert ps.get_comp("ML1").connected is True
    assert ps.get_comp("ML2").connected is True
    assert ps.get_comp("E1").is_open is False
    assert ps.get_comp("L1a").is_open is False
    assert ps.get_comp("L1b").is_open is False
    assert ps.get_comp("L2a").is_open is False
    assert ps.get_comp("L2b").is_open is False
    assert ps.get_comp("L3a").is_open is False
    assert ps.get_comp("L3b").is_open is False
    assert ps.get_comp("L4a").is_open is False
    assert ps.get_comp("L4b").is_open is False
    assert ps.get_comp("L5a").is_open is False
    assert ps.get_comp("L5b").is_open is False
    assert ps.get_comp("L6a").is_open is True
    assert ps.get_comp("L6b").is_open is True
    assert ps.get_comp("E2").is_open is False
    assert ps.get_comp("L7a").is_open is False
    assert ps.get_comp("L7b").is_open is False
    assert ps.get_comp("ML1a").is_open is False
    assert ps.get_comp("ML1b").is_open is False
    assert ps.get_comp("ML2a").is_open is False
    assert ps.get_comp("ML2b").is_open is False


def test_B3_trafo_fail():
    ps = initialize_network(
        include_ICT=False,
        microgrid_mode=MicrogridMode.LIMITED_SUPPORT,
    )

    # Create sections
    ps.create_sections()

    # Simulate failure at time 0
    # Time = 0
    curr_time = Time(0)
    dt = Time(1, TimeUnit.HOUR)

    ps.get_comp("B3").trafo_fail(dt)

    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    # Time = 1
    curr_time = Time(1)
    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    assert ps.get_comp("L1").connected is True
    assert ps.get_comp("L2").connected is True
    assert ps.get_comp("L3").connected is True
    assert ps.get_comp("L4").connected is True
    assert ps.get_comp("L5").connected is True
    assert ps.get_comp("L6").connected is False
    assert ps.get_comp("L7").connected is True
    assert ps.get_comp("ML1").connected is True
    assert ps.get_comp("ML2").connected is True
    assert ps.get_comp("E1").is_open is False
    assert ps.get_comp("L1a").is_open is False
    assert ps.get_comp("L1b").is_open is False
    assert ps.get_comp("L2a").is_open is False
    assert ps.get_comp("L2b").is_open is False
    assert ps.get_comp("L3a").is_open is False
    assert ps.get_comp("L3b").is_open is False
    assert ps.get_comp("L4a").is_open is False
    assert ps.get_comp("L4b").is_open is False
    assert ps.get_comp("L5a").is_open is False
    assert ps.get_comp("L5b").is_open is False
    assert ps.get_comp("L6a").is_open is True
    assert ps.get_comp("L6b").is_open is True
    assert ps.get_comp("E2").is_open is False
    assert ps.get_comp("L7a").is_open is False
    assert ps.get_comp("L7b").is_open is False
    assert ps.get_comp("ML1a").is_open is False
    assert ps.get_comp("ML1b").is_open is False
    assert ps.get_comp("ML2a").is_open is False
    assert ps.get_comp("ML2b").is_open is False


def test_B4_trafo_fail():
    ps = initialize_network(
        include_ICT=False,
        microgrid_mode=MicrogridMode.LIMITED_SUPPORT,
    )

    # Create sections
    ps.create_sections()

    # Simulate failure at time 0
    # Time = 0
    curr_time = Time(0)
    dt = Time(1, TimeUnit.HOUR)

    ps.get_comp("B4").trafo_fail(dt)

    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    # Time = 1
    curr_time = Time(1)
    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    assert ps.get_comp("L1").connected is True
    assert ps.get_comp("L2").connected is True
    assert ps.get_comp("L3").connected is True
    assert ps.get_comp("L4").connected is True
    assert ps.get_comp("L5").connected is True
    assert ps.get_comp("L6").connected is False
    assert ps.get_comp("L7").connected is True
    assert ps.get_comp("ML1").connected is True
    assert ps.get_comp("ML2").connected is True
    assert ps.get_comp("E1").is_open is False
    assert ps.get_comp("L1a").is_open is False
    assert ps.get_comp("L1b").is_open is False
    assert ps.get_comp("L2a").is_open is False
    assert ps.get_comp("L2b").is_open is False
    assert ps.get_comp("L3a").is_open is False
    assert ps.get_comp("L3b").is_open is False
    assert ps.get_comp("L4a").is_open is False
    assert ps.get_comp("L4b").is_open is False
    assert ps.get_comp("L5a").is_open is False
    assert ps.get_comp("L5b").is_open is False
    assert ps.get_comp("L6a").is_open is True
    assert ps.get_comp("L6b").is_open is True
    assert ps.get_comp("E2").is_open is False
    assert ps.get_comp("L7a").is_open is False
    assert ps.get_comp("L7b").is_open is False
    assert ps.get_comp("ML1a").is_open is False
    assert ps.get_comp("ML1b").is_open is False
    assert ps.get_comp("ML2a").is_open is False
    assert ps.get_comp("ML2b").is_open is False


def test_B5_trafo_fail():
    ps = initialize_network(
        include_ICT=False,
        microgrid_mode=MicrogridMode.LIMITED_SUPPORT,
    )

    # Create sections
    ps.create_sections()

    # Simulate failure at time 0
    # Time = 0
    curr_time = Time(0)
    dt = Time(1, TimeUnit.HOUR)

    ps.get_comp("B5").trafo_fail(dt)

    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    # Time = 1
    curr_time = Time(1)
    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    assert ps.get_comp("L1").connected is True
    assert ps.get_comp("L2").connected is True
    assert ps.get_comp("L3").connected is True
    assert ps.get_comp("L4").connected is True
    assert ps.get_comp("L5").connected is True
    assert ps.get_comp("L6").connected is False
    assert ps.get_comp("L7").connected is True
    assert ps.get_comp("ML1").connected is True
    assert ps.get_comp("ML2").connected is True
    assert ps.get_comp("E1").is_open is False
    assert ps.get_comp("L1a").is_open is False
    assert ps.get_comp("L1b").is_open is False
    assert ps.get_comp("L2a").is_open is False
    assert ps.get_comp("L2b").is_open is False
    assert ps.get_comp("L3a").is_open is False
    assert ps.get_comp("L3b").is_open is False
    assert ps.get_comp("L4a").is_open is False
    assert ps.get_comp("L4b").is_open is False
    assert ps.get_comp("L5a").is_open is False
    assert ps.get_comp("L5b").is_open is False
    assert ps.get_comp("L6a").is_open is True
    assert ps.get_comp("L6b").is_open is True
    assert ps.get_comp("E2").is_open is False
    assert ps.get_comp("L7a").is_open is False
    assert ps.get_comp("L7b").is_open is False
    assert ps.get_comp("ML1a").is_open is False
    assert ps.get_comp("ML1b").is_open is False
    assert ps.get_comp("ML2a").is_open is False
    assert ps.get_comp("ML2b").is_open is False


def test_B6_trafo_fail():
    ps = initialize_network(
        include_ICT=False,
        microgrid_mode=MicrogridMode.LIMITED_SUPPORT,
    )

    # Create sections
    ps.create_sections()

    # Simulate failure at time 0
    # Time = 0
    curr_time = Time(0)
    dt = Time(1, TimeUnit.HOUR)

    ps.get_comp("B6").trafo_fail(dt)

    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    # Time = 1
    curr_time = Time(1)
    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    assert ps.get_comp("L1").connected is True
    assert ps.get_comp("L2").connected is True
    assert ps.get_comp("L3").connected is True
    assert ps.get_comp("L4").connected is True
    assert ps.get_comp("L5").connected is True
    assert ps.get_comp("L6").connected is False
    assert ps.get_comp("L7").connected is True
    assert ps.get_comp("ML1").connected is True
    assert ps.get_comp("ML2").connected is True
    assert ps.get_comp("E1").is_open is False
    assert ps.get_comp("L1a").is_open is False
    assert ps.get_comp("L1b").is_open is False
    assert ps.get_comp("L2a").is_open is False
    assert ps.get_comp("L2b").is_open is False
    assert ps.get_comp("L3a").is_open is False
    assert ps.get_comp("L3b").is_open is False
    assert ps.get_comp("L4a").is_open is False
    assert ps.get_comp("L4b").is_open is False
    assert ps.get_comp("L5a").is_open is False
    assert ps.get_comp("L5b").is_open is False
    assert ps.get_comp("L6a").is_open is True
    assert ps.get_comp("L6b").is_open is True
    assert ps.get_comp("E2").is_open is False
    assert ps.get_comp("L7a").is_open is False
    assert ps.get_comp("L7b").is_open is False
    assert ps.get_comp("ML1a").is_open is False
    assert ps.get_comp("ML1b").is_open is False
    assert ps.get_comp("ML2a").is_open is False
    assert ps.get_comp("ML2b").is_open is False


def test_M1_trafo_fail():
    ps = initialize_network(
        include_ICT=False,
        microgrid_mode=MicrogridMode.LIMITED_SUPPORT,
    )

    # Create sections
    ps.create_sections()

    # Simulate failure at time 0
    # Time = 0
    curr_time = Time(0)
    dt = Time(1, TimeUnit.HOUR)

    ps.get_comp("M1").trafo_fail(dt)

    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    # Time = 1
    curr_time = Time(1)
    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    assert ps.get_comp("L1").connected is True
    assert ps.get_comp("L2").connected is True
    assert ps.get_comp("L3").connected is True
    assert ps.get_comp("L4").connected is True
    assert ps.get_comp("L5").connected is True
    assert ps.get_comp("L6").connected is False
    assert ps.get_comp("L7").connected is True
    assert ps.get_comp("ML1").connected is True
    assert ps.get_comp("ML2").connected is True
    assert ps.get_comp("E1").is_open is False
    assert ps.get_comp("L1a").is_open is False
    assert ps.get_comp("L1b").is_open is False
    assert ps.get_comp("L2a").is_open is False
    assert ps.get_comp("L2b").is_open is False
    assert ps.get_comp("L3a").is_open is False
    assert ps.get_comp("L3b").is_open is False
    assert ps.get_comp("L4a").is_open is False
    assert ps.get_comp("L4b").is_open is False
    assert ps.get_comp("L5a").is_open is False
    assert ps.get_comp("L5b").is_open is False
    assert ps.get_comp("L6a").is_open is True
    assert ps.get_comp("L6b").is_open is True
    assert ps.get_comp("E2").is_open is False
    assert ps.get_comp("L7a").is_open is False
    assert ps.get_comp("L7b").is_open is False
    assert ps.get_comp("ML1a").is_open is False
    assert ps.get_comp("ML1b").is_open is False
    assert ps.get_comp("ML2a").is_open is False
    assert ps.get_comp("ML2b").is_open is False


def test_M2_trafo_fail():
    ps = initialize_network(
        include_ICT=False,
        microgrid_mode=MicrogridMode.LIMITED_SUPPORT,
    )

    # Create sections
    ps.create_sections()

    # Simulate failure at time 0
    # Time = 0
    curr_time = Time(0)
    dt = Time(1, TimeUnit.HOUR)

    ps.get_comp("M2").trafo_fail(dt)

    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    # Time = 1
    curr_time = Time(1)
    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    assert ps.get_comp("L1").connected is True
    assert ps.get_comp("L2").connected is True
    assert ps.get_comp("L3").connected is True
    assert ps.get_comp("L4").connected is True
    assert ps.get_comp("L5").connected is True
    assert ps.get_comp("L6").connected is False
    assert ps.get_comp("L7").connected is True
    assert ps.get_comp("ML1").connected is True
    assert ps.get_comp("ML2").connected is True
    assert ps.get_comp("E1").is_open is False
    assert ps.get_comp("L1a").is_open is False
    assert ps.get_comp("L1b").is_open is False
    assert ps.get_comp("L2a").is_open is False
    assert ps.get_comp("L2b").is_open is False
    assert ps.get_comp("L3a").is_open is False
    assert ps.get_comp("L3b").is_open is False
    assert ps.get_comp("L4a").is_open is False
    assert ps.get_comp("L4b").is_open is False
    assert ps.get_comp("L5a").is_open is False
    assert ps.get_comp("L5b").is_open is False
    assert ps.get_comp("L6a").is_open is True
    assert ps.get_comp("L6b").is_open is True
    assert ps.get_comp("E2").is_open is False
    assert ps.get_comp("L7a").is_open is False
    assert ps.get_comp("L7b").is_open is False
    assert ps.get_comp("ML1a").is_open is False
    assert ps.get_comp("ML1b").is_open is False
    assert ps.get_comp("ML2a").is_open is False
    assert ps.get_comp("ML2b").is_open is False


def test_M3_trafo_fail():
    ps = initialize_network(
        include_ICT=False,
        microgrid_mode=MicrogridMode.LIMITED_SUPPORT,
    )

    # Create sections
    ps.create_sections()

    # Simulate failure at time 0
    # Time = 0
    curr_time = Time(0)
    dt = Time(1, TimeUnit.HOUR)

    ps.get_comp("M3").trafo_fail(dt)

    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    # Time = 1
    curr_time = Time(1)
    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    assert ps.get_comp("L1").connected is True
    assert ps.get_comp("L2").connected is True
    assert ps.get_comp("L3").connected is True
    assert ps.get_comp("L4").connected is True
    assert ps.get_comp("L5").connected is True
    assert ps.get_comp("L6").connected is False
    assert ps.get_comp("L7").connected is True
    assert ps.get_comp("ML1").connected is True
    assert ps.get_comp("ML2").connected is True
    assert ps.get_comp("E1").is_open is False
    assert ps.get_comp("L1a").is_open is False
    assert ps.get_comp("L1b").is_open is False
    assert ps.get_comp("L2a").is_open is False
    assert ps.get_comp("L2b").is_open is False
    assert ps.get_comp("L3a").is_open is False
    assert ps.get_comp("L3b").is_open is False
    assert ps.get_comp("L4a").is_open is False
    assert ps.get_comp("L4b").is_open is False
    assert ps.get_comp("L5a").is_open is False
    assert ps.get_comp("L5b").is_open is False
    assert ps.get_comp("L6a").is_open is True
    assert ps.get_comp("L6b").is_open is True
    assert ps.get_comp("E2").is_open is False
    assert ps.get_comp("L7a").is_open is False
    assert ps.get_comp("L7b").is_open is False
    assert ps.get_comp("ML1a").is_open is False
    assert ps.get_comp("ML1b").is_open is False
    assert ps.get_comp("ML2a").is_open is False
    assert ps.get_comp("ML2b").is_open is False


def test_L1_fail():
    ps = initialize_network(
        include_ICT=False,
        microgrid_mode=MicrogridMode.LIMITED_SUPPORT,
    )

    # Create sections
    ps.create_sections()

    # Simulate failure at time 0
    # Time = 0
    curr_time = Time(0)
    dt = Time(1, TimeUnit.HOUR)

    ps.get_comp("L1").fail(dt)

    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    # Time = 1
    curr_time = Time(1)
    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    assert ps.get_comp("L1").connected is False
    assert ps.get_comp("L2").connected is True
    assert ps.get_comp("L3").connected is True
    assert ps.get_comp("L4").connected is True
    assert ps.get_comp("L5").connected is True
    assert ps.get_comp("L6").connected is False
    assert ps.get_comp("L7").connected is True
    assert ps.get_comp("ML1").connected is True
    assert ps.get_comp("ML2").connected is True
    assert ps.get_comp("E1").is_open is True
    assert ps.get_comp("L1a").is_open is True
    assert ps.get_comp("L1b").is_open is True
    assert ps.get_comp("L2a").is_open is False
    assert ps.get_comp("L2b").is_open is False
    assert ps.get_comp("L3a").is_open is False
    assert ps.get_comp("L3b").is_open is False
    assert ps.get_comp("L4a").is_open is False
    assert ps.get_comp("L4b").is_open is False
    assert ps.get_comp("L5a").is_open is False
    assert ps.get_comp("L5b").is_open is False
    assert ps.get_comp("L6a").is_open is True
    assert ps.get_comp("L6b").is_open is True
    assert ps.get_comp("E2").is_open is False
    assert ps.get_comp("L7a").is_open is False
    assert ps.get_comp("L7b").is_open is False
    assert ps.get_comp("ML1a").is_open is False
    assert ps.get_comp("ML1b").is_open is False
    assert ps.get_comp("ML2a").is_open is False
    assert ps.get_comp("ML2b").is_open is False


def test_L2_fail():
    ps = initialize_network(
        include_ICT=False,
        microgrid_mode=MicrogridMode.LIMITED_SUPPORT,
    )

    # Create sections
    ps.create_sections()

    # Simulate failure at time 0
    # Time = 0
    curr_time = Time(0)
    dt = Time(1, TimeUnit.HOUR)

    ps.get_comp("L2").fail(dt)

    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    # Time = 1
    curr_time = Time(1)
    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    assert ps.get_comp("L1").connected is True
    assert ps.get_comp("L2").connected is False
    assert ps.get_comp("L3").connected is True
    assert ps.get_comp("L4").connected is True
    assert ps.get_comp("L5").connected is True
    assert ps.get_comp("L6").connected is True
    assert ps.get_comp("L7").connected is True
    assert ps.get_comp("ML1").connected is True
    assert ps.get_comp("ML2").connected is True
    assert ps.get_comp("E1").is_open is False
    assert ps.get_comp("L1a").is_open is False
    assert ps.get_comp("L1b").is_open is False
    assert ps.get_comp("L2a").is_open is True
    assert ps.get_comp("L2b").is_open is True
    assert ps.get_comp("L3a").is_open is False
    assert ps.get_comp("L3b").is_open is False
    assert ps.get_comp("L4a").is_open is False
    assert ps.get_comp("L4b").is_open is False
    assert ps.get_comp("L5a").is_open is False
    assert ps.get_comp("L5b").is_open is False
    assert ps.get_comp("L6a").is_open is False
    assert ps.get_comp("L6b").is_open is False
    assert ps.get_comp("E2").is_open is False
    assert ps.get_comp("L7a").is_open is False
    assert ps.get_comp("L7b").is_open is False
    assert ps.get_comp("ML1a").is_open is False
    assert ps.get_comp("ML1b").is_open is False
    assert ps.get_comp("ML2a").is_open is False
    assert ps.get_comp("ML2b").is_open is False


def test_L3_fail():
    ps = initialize_network(
        include_ICT=False,
        microgrid_mode=MicrogridMode.LIMITED_SUPPORT,
    )

    # Create sections
    ps.create_sections()

    # Simulate failure at time 0
    # Time = 0
    curr_time = Time(0)
    dt = Time(1, TimeUnit.HOUR)

    ps.get_comp("L3").fail(dt)

    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    # Time = 1
    curr_time = Time(1)
    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    assert ps.get_comp("L1").connected is True
    assert ps.get_comp("L2").connected is True
    assert ps.get_comp("L3").connected is False
    assert ps.get_comp("L4").connected is True
    assert ps.get_comp("L5").connected is True
    assert ps.get_comp("L6").connected is True
    assert ps.get_comp("L7").connected is True
    assert ps.get_comp("ML1").connected is True
    assert ps.get_comp("ML2").connected is True
    assert ps.get_comp("E1").is_open is False
    assert ps.get_comp("L1a").is_open is False
    assert ps.get_comp("L1b").is_open is False
    assert ps.get_comp("L2a").is_open is False
    assert ps.get_comp("L2b").is_open is False
    assert ps.get_comp("L3a").is_open is True
    assert ps.get_comp("L3b").is_open is True
    assert ps.get_comp("L4a").is_open is False
    assert ps.get_comp("L4b").is_open is False
    assert ps.get_comp("L5a").is_open is False
    assert ps.get_comp("L5b").is_open is False
    assert ps.get_comp("L6a").is_open is False
    assert ps.get_comp("L6b").is_open is False
    assert ps.get_comp("E2").is_open is False
    assert ps.get_comp("L7a").is_open is False
    assert ps.get_comp("L7b").is_open is False
    assert ps.get_comp("ML1a").is_open is False
    assert ps.get_comp("ML1b").is_open is False
    assert ps.get_comp("ML2a").is_open is False
    assert ps.get_comp("ML2b").is_open is False


def test_L4_fail():
    ps = initialize_network(
        include_ICT=False,
        microgrid_mode=MicrogridMode.LIMITED_SUPPORT,
    )

    # Create sections
    ps.create_sections()

    # Simulate failure at time 0
    # Time = 0
    curr_time = Time(0)
    dt = Time(1, TimeUnit.HOUR)

    ps.get_comp("L4").fail(dt)

    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    # Time = 1
    curr_time = Time(1)
    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    assert ps.get_comp("L1").connected is True
    assert ps.get_comp("L2").connected is True
    assert ps.get_comp("L3").connected is True
    assert ps.get_comp("L4").connected is False
    assert ps.get_comp("L5").connected is True
    assert ps.get_comp("L6").connected is False
    assert ps.get_comp("L7").connected is True
    assert ps.get_comp("ML1").connected is True
    assert ps.get_comp("ML2").connected is True
    assert ps.get_comp("E1").is_open is False
    assert ps.get_comp("L1a").is_open is False
    assert ps.get_comp("L1b").is_open is False
    assert ps.get_comp("L2a").is_open is False
    assert ps.get_comp("L2b").is_open is False
    assert ps.get_comp("L3a").is_open is False
    assert ps.get_comp("L3b").is_open is False
    assert ps.get_comp("L4a").is_open is True
    assert ps.get_comp("L4b").is_open is True
    assert ps.get_comp("L5a").is_open is False
    assert ps.get_comp("L5b").is_open is False
    assert ps.get_comp("L6a").is_open is True
    assert ps.get_comp("L6b").is_open is True
    assert ps.get_comp("E2").is_open is False
    assert ps.get_comp("L7a").is_open is False
    assert ps.get_comp("L7b").is_open is False
    assert ps.get_comp("ML1a").is_open is False
    assert ps.get_comp("ML1b").is_open is False
    assert ps.get_comp("ML2a").is_open is False
    assert ps.get_comp("ML2b").is_open is False


def test_L5_fail():
    ps = initialize_network(
        include_ICT=False,
        microgrid_mode=MicrogridMode.LIMITED_SUPPORT,
    )

    # Create sections
    ps.create_sections()

    # Simulate failure at time 0
    # Time = 0
    curr_time = Time(0)
    dt = Time(1, TimeUnit.HOUR)

    ps.get_comp("L5").fail(dt)

    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    # Time = 1
    curr_time = Time(1)
    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    assert ps.get_comp("L1").connected is True
    assert ps.get_comp("L2").connected is True
    assert ps.get_comp("L3").connected is True
    assert ps.get_comp("L4").connected is True
    assert ps.get_comp("L5").connected is False
    assert ps.get_comp("L6").connected is True
    assert ps.get_comp("L7").connected is True
    assert ps.get_comp("ML1").connected is True
    assert ps.get_comp("ML2").connected is True
    assert ps.get_comp("E1").is_open is False
    assert ps.get_comp("L1a").is_open is False
    assert ps.get_comp("L1b").is_open is False
    assert ps.get_comp("L2a").is_open is False
    assert ps.get_comp("L2b").is_open is False
    assert ps.get_comp("L3a").is_open is False
    assert ps.get_comp("L3b").is_open is False
    assert ps.get_comp("L4a").is_open is False
    assert ps.get_comp("L4b").is_open is False
    assert ps.get_comp("L5a").is_open is True
    assert ps.get_comp("L5b").is_open is True
    assert ps.get_comp("L6a").is_open is False
    assert ps.get_comp("L6b").is_open is False
    assert ps.get_comp("E2").is_open is False
    assert ps.get_comp("L7a").is_open is False
    assert ps.get_comp("L7b").is_open is False
    assert ps.get_comp("ML1a").is_open is False
    assert ps.get_comp("ML1b").is_open is False
    assert ps.get_comp("ML2a").is_open is False
    assert ps.get_comp("ML2b").is_open is False


def test_L6_fail():
    ps = initialize_network(
        include_ICT=False,
        microgrid_mode=MicrogridMode.LIMITED_SUPPORT,
    )

    # Create sections
    ps.create_sections()

    # Simulate failure at time 0
    # Time = 0
    curr_time = Time(0)
    dt = Time(1, TimeUnit.HOUR)

    ps.get_comp("L6").fail(dt)

    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    # Time = 1
    curr_time = Time(1)
    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    assert ps.get_comp("L1").connected is True
    assert ps.get_comp("L2").connected is True
    assert ps.get_comp("L3").connected is True
    assert ps.get_comp("L4").connected is True
    assert ps.get_comp("L5").connected is True
    assert ps.get_comp("L6").connected is False
    assert ps.get_comp("L7").connected is True
    assert ps.get_comp("ML1").connected is True
    assert ps.get_comp("ML2").connected is True
    assert ps.get_comp("E1").is_open is False
    assert ps.get_comp("L1a").is_open is False
    assert ps.get_comp("L1b").is_open is False
    assert ps.get_comp("L2a").is_open is False
    assert ps.get_comp("L2b").is_open is False
    assert ps.get_comp("L3a").is_open is False
    assert ps.get_comp("L3b").is_open is False
    assert ps.get_comp("L4a").is_open is False
    assert ps.get_comp("L4b").is_open is False
    assert ps.get_comp("L5a").is_open is False
    assert ps.get_comp("L5b").is_open is False
    assert ps.get_comp("L6a").is_open is True
    assert ps.get_comp("L6b").is_open is True
    assert ps.get_comp("E2").is_open is False
    assert ps.get_comp("L7a").is_open is False
    assert ps.get_comp("L7b").is_open is False
    assert ps.get_comp("ML1a").is_open is False
    assert ps.get_comp("ML1b").is_open is False
    assert ps.get_comp("ML2a").is_open is False
    assert ps.get_comp("ML2b").is_open is False


def test_L7_fail():
    ps = initialize_network(
        include_ICT=False,
        microgrid_mode=MicrogridMode.LIMITED_SUPPORT,
    )

    # Create sections
    ps.create_sections()

    # Simulate failure at time 0
    # Time = 0
    curr_time = Time(0)
    dt = Time(1, TimeUnit.HOUR)

    ps.get_comp("L7").fail(dt)

    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    # Time = 1
    curr_time = Time(1)
    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    assert ps.get_comp("L1").connected is True
    assert ps.get_comp("L2").connected is True
    assert ps.get_comp("L3").connected is True
    assert ps.get_comp("L4").connected is True
    assert ps.get_comp("L5").connected is True
    assert ps.get_comp("L6").connected is False
    assert ps.get_comp("L7").connected is False
    assert ps.get_comp("ML1").connected is True
    assert ps.get_comp("ML2").connected is True
    assert ps.get_comp("E1").is_open is False
    assert ps.get_comp("L1a").is_open is False
    assert ps.get_comp("L1b").is_open is False
    assert ps.get_comp("L2a").is_open is False
    assert ps.get_comp("L2b").is_open is False
    assert ps.get_comp("L3a").is_open is False
    assert ps.get_comp("L3b").is_open is False
    assert ps.get_comp("L4a").is_open is False
    assert ps.get_comp("L4b").is_open is False
    assert ps.get_comp("L5a").is_open is False
    assert ps.get_comp("L5b").is_open is False
    assert ps.get_comp("L6a").is_open is True
    assert ps.get_comp("L6b").is_open is True
    assert ps.get_comp("E2").is_open is True
    assert ps.get_comp("L7a").is_open is True
    assert ps.get_comp("L7b").is_open is True
    assert ps.get_comp("ML1a").is_open is False
    assert ps.get_comp("ML1b").is_open is False
    assert ps.get_comp("ML2a").is_open is False
    assert ps.get_comp("ML2b").is_open is False


def test_ML1_fail():
    ps = initialize_network(
        include_ICT=False,
        microgrid_mode=MicrogridMode.LIMITED_SUPPORT,
    )

    # Create sections
    ps.create_sections()

    # Simulate failure at time 0
    # Time = 0
    curr_time = Time(0)
    dt = Time(1, TimeUnit.HOUR)

    ps.get_comp("ML1").fail(dt)

    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    # Time = 1
    curr_time = Time(1)
    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    assert ps.get_comp("L1").connected is True
    assert ps.get_comp("L2").connected is True
    assert ps.get_comp("L3").connected is True
    assert ps.get_comp("L4").connected is True
    assert ps.get_comp("L5").connected is True
    assert ps.get_comp("L6").connected is False
    assert ps.get_comp("L7").connected is True
    assert ps.get_comp("ML1").connected is False
    assert ps.get_comp("ML2").connected is True
    assert ps.get_comp("E1").is_open is False
    assert ps.get_comp("L1a").is_open is False
    assert ps.get_comp("L1b").is_open is False
    assert ps.get_comp("L2a").is_open is False
    assert ps.get_comp("L2b").is_open is False
    assert ps.get_comp("L3a").is_open is False
    assert ps.get_comp("L3b").is_open is False
    assert ps.get_comp("L4a").is_open is False
    assert ps.get_comp("L4b").is_open is False
    assert ps.get_comp("L5a").is_open is False
    assert ps.get_comp("L5b").is_open is False
    assert ps.get_comp("L6a").is_open is True
    assert ps.get_comp("L6b").is_open is True
    assert ps.get_comp("E2").is_open is False
    assert ps.get_comp("L7a").is_open is False
    assert ps.get_comp("L7b").is_open is False
    assert ps.get_comp("ML1a").is_open is True
    assert ps.get_comp("ML1b").is_open is True
    assert ps.get_comp("ML2a").is_open is False
    assert ps.get_comp("ML2b").is_open is False


def test_ML2_fail():
    ps = initialize_network()

    ps = initialize_network(
        include_ICT=False,
        microgrid_mode=MicrogridMode.LIMITED_SUPPORT,
    )

    # Create sections
    ps.create_sections()

    # Simulate failure at time 0
    # Time = 0
    curr_time = Time(0)
    dt = Time(1, TimeUnit.HOUR)

    ps.get_comp("ML2").fail(dt)

    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    # Time = 1
    curr_time = Time(1)
    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    assert ps.get_comp("L1").connected is True
    assert ps.get_comp("L2").connected is True
    assert ps.get_comp("L3").connected is True
    assert ps.get_comp("L4").connected is True
    assert ps.get_comp("L5").connected is True
    assert ps.get_comp("L6").connected is False
    assert ps.get_comp("L7").connected is True
    assert ps.get_comp("ML1").connected is True
    assert ps.get_comp("ML2").connected is False
    assert ps.get_comp("E1").is_open is False
    assert ps.get_comp("L1a").is_open is False
    assert ps.get_comp("L1b").is_open is False
    assert ps.get_comp("L2a").is_open is False
    assert ps.get_comp("L2b").is_open is False
    assert ps.get_comp("L3a").is_open is False
    assert ps.get_comp("L3b").is_open is False
    assert ps.get_comp("L4a").is_open is False
    assert ps.get_comp("L4b").is_open is False
    assert ps.get_comp("L5a").is_open is False
    assert ps.get_comp("L5b").is_open is False
    assert ps.get_comp("L6a").is_open is True
    assert ps.get_comp("L6b").is_open is True
    assert ps.get_comp("E2").is_open is False
    assert ps.get_comp("L7a").is_open is False
    assert ps.get_comp("L7b").is_open is False
    assert ps.get_comp("ML1a").is_open is False
    assert ps.get_comp("ML1b").is_open is False
    assert ps.get_comp("ML2a").is_open is True
    assert ps.get_comp("ML2b").is_open is True


def test_L2_and_L3_fail():
    ps = initialize_network(
        include_ICT=False,
        microgrid_mode=MicrogridMode.LIMITED_SUPPORT,
    )

    # Create sections
    ps.create_sections()

    # Simulate failure at time 0
    # Time = 0
    curr_time = Time(0)
    dt = Time(1, TimeUnit.HOUR)

    ps.get_comp("L2").fail(dt)
    ps.get_comp("L3").fail(dt)

    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    # Time = 1
    curr_time = Time(1)
    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    assert ps.get_comp("L1").connected is True
    assert ps.get_comp("L2").connected is False
    assert ps.get_comp("L3").connected is False
    assert ps.get_comp("L4").connected is True
    assert ps.get_comp("L5").connected is True
    assert ps.get_comp("L6").connected is True
    assert ps.get_comp("L7").connected is True
    assert ps.get_comp("ML1").connected is True
    assert ps.get_comp("ML2").connected is True
    assert ps.get_comp("E1").is_open is False
    assert ps.get_comp("L1a").is_open is False
    assert ps.get_comp("L1b").is_open is False
    assert ps.get_comp("L2a").is_open is True
    assert ps.get_comp("L2b").is_open is True
    assert ps.get_comp("L3a").is_open is True
    assert ps.get_comp("L3b").is_open is True
    assert ps.get_comp("L4a").is_open is False
    assert ps.get_comp("L4b").is_open is False
    assert ps.get_comp("L5a").is_open is False
    assert ps.get_comp("L5b").is_open is False
    assert ps.get_comp("L6a").is_open is False
    assert ps.get_comp("L6b").is_open is False
    assert ps.get_comp("E2").is_open is False
    assert ps.get_comp("L7a").is_open is False
    assert ps.get_comp("L7b").is_open is False
    assert ps.get_comp("ML1a").is_open is False
    assert ps.get_comp("ML1b").is_open is False
    assert ps.get_comp("ML2a").is_open is False
    assert ps.get_comp("ML2b").is_open is False


def test_L3_and_L5_fail():
    ps = initialize_network()

    ps = initialize_network(
        include_ICT=False,
        microgrid_mode=MicrogridMode.LIMITED_SUPPORT,
    )

    # Create sections
    ps.create_sections()

    # Simulate failure at time 0
    # Time = 0
    curr_time = Time(0)
    dt = Time(1, TimeUnit.HOUR)

    ps.get_comp("L3").fail(dt)
    ps.get_comp("L5").fail(dt)

    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    # Time = 1
    curr_time = Time(1)
    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    assert ps.get_comp("L1").connected is True
    assert ps.get_comp("L2").connected is True
    assert ps.get_comp("L3").connected is False
    assert ps.get_comp("L4").connected is True
    assert ps.get_comp("L5").connected is False
    assert ps.get_comp("L6").connected is True
    assert ps.get_comp("L7").connected is True
    assert ps.get_comp("ML1").connected is True
    assert ps.get_comp("ML2").connected is True
    assert ps.get_comp("E1").is_open is False
    assert ps.get_comp("L1a").is_open is False
    assert ps.get_comp("L1b").is_open is False
    assert ps.get_comp("L2a").is_open is False
    assert ps.get_comp("L2b").is_open is False
    assert ps.get_comp("L3a").is_open is True
    assert ps.get_comp("L3b").is_open is True
    assert ps.get_comp("L4a").is_open is False
    assert ps.get_comp("L4b").is_open is False
    assert ps.get_comp("L5a").is_open is True
    assert ps.get_comp("L5b").is_open is True
    assert ps.get_comp("L6a").is_open is False
    assert ps.get_comp("L6b").is_open is False
    assert ps.get_comp("E2").is_open is False
    assert ps.get_comp("L7a").is_open is False
    assert ps.get_comp("L7b").is_open is False
    assert ps.get_comp("ML1a").is_open is False
    assert ps.get_comp("ML1b").is_open is False
    assert ps.get_comp("ML2a").is_open is False
    assert ps.get_comp("ML2b").is_open is False


def test_L2_L1_fail():
    ps = initialize_network(
        include_ICT=False,
        microgrid_mode=MicrogridMode.LIMITED_SUPPORT,
        fail_rate_line=0,
        line_repair_time_stat_dist=StatDist(
            stat_dist_type=StatDistType.UNIFORM_FLOAT,
            parameters=UniformParameters(
                min_val=2,
                max_val=2,
            ),
        ),
    )

    # Create sections
    ps.create_sections()

    # Simulate failure at time 0
    # Time = 0
    curr_time = Time(0)
    dt = Time(1, TimeUnit.HOUR)

    ps.update_fail_status(dt)

    ps.get_comp("L2").fail(dt)

    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    assert ps.get_comp("L1").connected is False
    assert ps.get_comp("L2").connected is True
    assert ps.get_comp("L3").connected is True
    assert ps.get_comp("L4").connected is True
    assert ps.get_comp("L5").connected is True
    assert ps.get_comp("L6").connected is False
    assert ps.get_comp("L7").connected is False
    assert ps.get_comp("ML1").connected is True
    assert ps.get_comp("ML2").connected is True
    assert ps.get_comp("E1").is_open is True
    assert ps.get_comp("L1a").is_open is True
    assert ps.get_comp("L1b").is_open is True
    assert ps.get_comp("L2a").is_open is False
    assert ps.get_comp("L2b").is_open is False
    assert ps.get_comp("L3a").is_open is False
    assert ps.get_comp("L3b").is_open is False
    assert ps.get_comp("L4a").is_open is False
    assert ps.get_comp("L4b").is_open is False
    assert ps.get_comp("L5a").is_open is False
    assert ps.get_comp("L5b").is_open is False
    assert ps.get_comp("L6a").is_open is True
    assert ps.get_comp("L6b").is_open is True
    assert ps.get_comp("E2").is_open is True
    assert ps.get_comp("L7a").is_open is True
    assert ps.get_comp("L7b").is_open is True
    assert ps.get_comp("ML1a").is_open is False
    assert ps.get_comp("ML1b").is_open is False
    assert ps.get_comp("ML2a").is_open is False
    assert ps.get_comp("ML2b").is_open is False

    # Time = 1
    ps.update_fail_status(dt)
    ps.get_comp("L1").fail(dt)

    curr_time = Time(1)
    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    assert ps.get_comp("L1").connected is False
    assert ps.get_comp("L2").connected is True
    assert ps.get_comp("L3").connected is True
    assert ps.get_comp("L4").connected is True
    assert ps.get_comp("L5").connected is True
    assert ps.get_comp("L6").connected is False
    assert ps.get_comp("L7").connected is False
    assert ps.get_comp("ML1").connected is True
    assert ps.get_comp("ML2").connected is True
    assert ps.get_comp("E1").is_open is True
    assert ps.get_comp("L1a").is_open is True
    assert ps.get_comp("L1b").is_open is True
    assert ps.get_comp("L2a").is_open is False
    assert ps.get_comp("L2b").is_open is False
    assert ps.get_comp("L3a").is_open is False
    assert ps.get_comp("L3b").is_open is False
    assert ps.get_comp("L4a").is_open is False
    assert ps.get_comp("L4b").is_open is False
    assert ps.get_comp("L5a").is_open is False
    assert ps.get_comp("L5b").is_open is False
    assert ps.get_comp("L6a").is_open is True
    assert ps.get_comp("L6b").is_open is True
    assert ps.get_comp("E2").is_open is True
    assert ps.get_comp("L7a").is_open is True
    assert ps.get_comp("L7b").is_open is True
    assert ps.get_comp("ML1a").is_open is False
    assert ps.get_comp("ML1b").is_open is False
    assert ps.get_comp("ML2a").is_open is False
    assert ps.get_comp("ML2b").is_open is False

    # Time = 2
    ps.update_fail_status(dt)

    curr_time = Time(2)
    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    assert ps.get_comp("L1").connected is False
    assert ps.get_comp("L2").connected is False
    assert ps.get_comp("L3").connected is True
    assert ps.get_comp("L4").connected is True
    assert ps.get_comp("L5").connected is True
    assert ps.get_comp("L6").connected is True
    assert ps.get_comp("L7").connected is True
    assert ps.get_comp("ML1").connected is True
    assert ps.get_comp("ML2").connected is True
    assert ps.get_comp("E1").is_open is True
    assert ps.get_comp("L1a").is_open is True
    assert ps.get_comp("L1b").is_open is True
    assert ps.get_comp("L2a").is_open is True
    assert ps.get_comp("L2b").is_open is True
    assert ps.get_comp("L3a").is_open is False
    assert ps.get_comp("L3b").is_open is False
    assert ps.get_comp("L4a").is_open is False
    assert ps.get_comp("L4b").is_open is False
    assert ps.get_comp("L5a").is_open is False
    assert ps.get_comp("L5b").is_open is False
    assert ps.get_comp("L6a").is_open is False
    assert ps.get_comp("L6b").is_open is False
    assert ps.get_comp("E2").is_open is False
    assert ps.get_comp("L7a").is_open is False
    assert ps.get_comp("L7b").is_open is False
    assert ps.get_comp("ML1a").is_open is False
    assert ps.get_comp("ML1b").is_open is False
    assert ps.get_comp("ML2a").is_open is False
    assert ps.get_comp("ML2b").is_open is False

    # Time = 3
    ps.update_fail_status(dt)

    curr_time = Time(3)
    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    assert ps.get_comp("L1").connected is False
    assert ps.get_comp("L2").connected is True
    assert ps.get_comp("L3").connected is True
    assert ps.get_comp("L4").connected is True
    assert ps.get_comp("L5").connected is True
    assert ps.get_comp("L6").connected is False
    assert ps.get_comp("L7").connected is True
    assert ps.get_comp("ML1").connected is True
    assert ps.get_comp("ML2").connected is True
    assert ps.get_comp("E1").is_open is True
    assert ps.get_comp("L1a").is_open is True
    assert ps.get_comp("L1b").is_open is True
    assert ps.get_comp("L2a").is_open is False
    assert ps.get_comp("L2b").is_open is False
    assert ps.get_comp("L3a").is_open is False
    assert ps.get_comp("L3b").is_open is False
    assert ps.get_comp("L4a").is_open is False
    assert ps.get_comp("L4b").is_open is False
    assert ps.get_comp("L5a").is_open is False
    assert ps.get_comp("L5b").is_open is False
    assert ps.get_comp("L6a").is_open is True
    assert ps.get_comp("L6b").is_open is True
    assert ps.get_comp("E2").is_open is False
    assert ps.get_comp("L7a").is_open is False
    assert ps.get_comp("L7b").is_open is False
    assert ps.get_comp("ML1a").is_open is False
    assert ps.get_comp("ML1b").is_open is False
    assert ps.get_comp("ML2a").is_open is False
    assert ps.get_comp("ML2b").is_open is False

    # Time = 4
    ps.update_fail_status(dt)

    curr_time = Time(4)
    ps.controller.run_control_loop(curr_time, dt)

    find_sub_systems(ps, curr_time)

    assert ps.get_comp("L1").connected is True
    assert ps.get_comp("L2").connected is True
    assert ps.get_comp("L3").connected is True
    assert ps.get_comp("L4").connected is True
    assert ps.get_comp("L5").connected is True
    assert ps.get_comp("L6").connected is False
    assert ps.get_comp("L7").connected is True
    assert ps.get_comp("ML1").connected is True
    assert ps.get_comp("ML2").connected is True
    assert ps.get_comp("E1").is_open is False
    assert ps.get_comp("L1a").is_open is False
    assert ps.get_comp("L1b").is_open is False
    assert ps.get_comp("L2a").is_open is False
    assert ps.get_comp("L2b").is_open is False
    assert ps.get_comp("L3a").is_open is False
    assert ps.get_comp("L3b").is_open is False
    assert ps.get_comp("L4a").is_open is False
    assert ps.get_comp("L4b").is_open is False
    assert ps.get_comp("L5a").is_open is False
    assert ps.get_comp("L5b").is_open is False
    assert ps.get_comp("L6a").is_open is True
    assert ps.get_comp("L6b").is_open is True
    assert ps.get_comp("E2").is_open is False
    assert ps.get_comp("L7a").is_open is False
    assert ps.get_comp("L7b").is_open is False
    assert ps.get_comp("ML1a").is_open is False
    assert ps.get_comp("ML1b").is_open is False
    assert ps.get_comp("ML2a").is_open is False
    assert ps.get_comp("ML2b").is_open is False
