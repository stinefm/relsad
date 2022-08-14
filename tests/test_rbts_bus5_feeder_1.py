import numpy as np
from relsad.utils import (
    eq,
)
from relsad.simulation import Simulation
from relsad.network.components import (
    Bus,
    Line,
    Disconnector,
    CircuitBreaker,
    ManualMainController,
)
from relsad.network.systems import (
    PowerSystem,
    Transmission,
    Distribution,
)
from relsad.Time import (
    Time,
    TimeUnit,
    TimeStamp,
)

from relsad.StatDist import (
    StatDist,
    StatDistType,
    UniformParameters,
)


def network(
    fail_rate_line: float = 0.065,  # fail rate per year
    r=0.266584,  # Length = 1 km
    x=0,
    line_repair_time_stat_dist: StatDist = StatDist(
        stat_dist_type=StatDistType.UNIFORM_FLOAT,
        parameters=UniformParameters(
            min_val=4,
            max_val=4,
        ),
    ),
):

    C1 = ManualMainController(
        name="C1",
        sectioning_time=Time(1, TimeUnit.HOUR),
    )

    ps = PowerSystem(C1)

    # Feeder
    F = Bus(
        name="F",
        n_customers=0,
        coordinate=[0, 0],
    )

    # Buses
    B1 = Bus(
        name="B1",
        n_customers=0,
        coordinate=[1, -3],
    )
    B2 = Bus(
        name="B2",
        n_customers=210,
        coordinate=[1, -4],
    )
    B3 = Bus(
        name="B3",
        n_customers=210,
        coordinate=[1.5, -4],
    )
    B4 = Bus(
        name="B4",
        n_customers=0,
        coordinate=[2, -3],
    )
    B5 = Bus(
        name="B5",
        n_customers=1,
        coordinate=[2, -4],
    )
    B6 = Bus(
        name="B6",
        n_customers=240,
        coordinate=[2.5, -4],
    )
    B7 = Bus(
        name="B7",
        n_customers=0,
        coordinate=[3, -3],
    )
    B8 = Bus(
        name="B8",
        n_customers=1,
        coordinate=[3, -4],
    )
    B9 = Bus(
        name="B9",
        n_customers=240,
        coordinate=[3.5, -4],
    )
    B10 = Bus(
        name="B10",
        n_customers=0,
        coordinate=[4, -3],
    )
    B11 = Bus(
        name="B11",
        n_customers=15,
        coordinate=[4, -4],
    )

    L1 = Line(
        name="L1",
        fbus=F,
        tbus=B1,
        r=r,
        x=x,
        fail_rate_density_per_year=0.5 * fail_rate_line,
        repair_time_dist=line_repair_time_stat_dist,
    )
    L2 = Line(
        name="L2",
        fbus=B1,
        tbus=B2,
        r=r,
        x=x,
        fail_rate_density_per_year=0.8 * fail_rate_line,
        repair_time_dist=line_repair_time_stat_dist,
    )
    L3 = Line(
        name="L3",
        fbus=B1,
        tbus=B3,
        r=r,
        x=x,
        fail_rate_density_per_year=0.8 * fail_rate_line,
        repair_time_dist=line_repair_time_stat_dist,
    )
    L4 = Line(
        name="L4",
        fbus=B1,
        tbus=B4,
        r=r,
        x=x,
        fail_rate_density_per_year=0.65 * fail_rate_line,
        repair_time_dist=line_repair_time_stat_dist,
    )
    L5 = Line(
        name="L5",
        fbus=B4,
        tbus=B5,
        r=r,
        x=x,
        fail_rate_density_per_year=0.8 * fail_rate_line,
        repair_time_dist=line_repair_time_stat_dist,
    )
    L6 = Line(
        name="L6",
        fbus=B4,
        tbus=B6,
        r=r,
        x=x,
        fail_rate_density_per_year=0.5 * fail_rate_line,
        repair_time_dist=line_repair_time_stat_dist,
    )
    L7 = Line(
        name="L7",
        fbus=B4,
        tbus=B7,
        r=r,
        x=x,
        fail_rate_density_per_year=0.65 * fail_rate_line,
        repair_time_dist=line_repair_time_stat_dist,
    )
    L8 = Line(
        name="L8",
        fbus=B7,
        tbus=B8,
        r=r,
        x=x,
        fail_rate_density_per_year=0.65 * fail_rate_line,
        repair_time_dist=line_repair_time_stat_dist,
    )
    L9 = Line(
        name="L9",
        fbus=B7,
        tbus=B9,
        r=r,
        x=x,
        fail_rate_density_per_year=0.5 * fail_rate_line,
        repair_time_dist=line_repair_time_stat_dist,
    )
    L10 = Line(
        name="L10",
        fbus=B7,
        tbus=B10,
        r=r,
        x=x,
        fail_rate_density_per_year=0.8 * fail_rate_line,
        repair_time_dist=line_repair_time_stat_dist,
    )
    L11 = Line(
        name="L11",
        fbus=B10,
        tbus=B11,
        r=r,
        x=x,
        fail_rate_density_per_year=0.8 * fail_rate_line,
        repair_time_dist=line_repair_time_stat_dist,
    )

    CircuitBreaker("E1", L1)
    Disconnector("DL4", L4, B1)
    Disconnector("DL7", L7, B4)
    Disconnector("DL10", L10, B7)

    tn = Transmission(parent_network=ps, trafo_bus=F)

    dn1 = Distribution(parent_network=tn, connected_line=L1)
    dn1.add_buses([B1, B2, B3, B4, B5, B6, B7, B8, B9, B10, B11])
    dn1.add_lines([L2, L3, L4, L5, L6, L7, L8, L9, L10, L11])

    unit_load = np.ones(2)

    B2.add_load_data(pload_data=unit_load * 0.4269 / B2.n_customers)
    B3.add_load_data(pload_data=unit_load * 0.4269 / B3.n_customers)
    B5.add_load_data(pload_data=unit_load * 0.6247 / B5.n_customers)
    B6.add_load_data(pload_data=unit_load * 0.4171 / B6.n_customers)
    B8.add_load_data(pload_data=unit_load * 0.6247 / B8.n_customers)
    B9.add_load_data(pload_data=unit_load * 0.4171 / B9.n_customers)
    B11.add_load_data(pload_data=unit_load * 0.4089 / B11.n_customers)

    return ps


def test_fail_L8():
    ps = network(fail_rate_line=0)

    ps.get_comp("L8").fail(dt=Time(1, TimeUnit.HOUR))

    sim = Simulation(ps)

    sim.run_sequential(
        start_time=TimeStamp(
            year=2019,
            month=1,
            day=1,
            hour=0,
            minute=0,
            second=0,
        ),
        stop_time=TimeStamp(
            year=2019,
            month=1,
            day=1,
            hour=6,
            minute=0,
            second=0,
        ),
        time_step=Time(1, TimeUnit.HOUR),
        time_unit=TimeUnit.HOUR,
        save_flag=False,
    )