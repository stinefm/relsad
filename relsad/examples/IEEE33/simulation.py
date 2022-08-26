import os
import time

from relsad.examples.IEEE33.load_and_prod import set_network_load_and_prod
from relsad.examples.IEEE33.network import initialize_network
from relsad.network.components import MicrogridMode
from relsad.simulation import Simulation
from relsad.StatDist import (
    GammaParameters,
    NormalParameters,
    StatDist,
    StatDistType,
)
from relsad.Time import Time, TimeStamp, TimeUnit
from relsad.visualization.plotting import plot_topology


def run_simulation(
    include_microgrid: bool = True,
    include_production: bool = True,
    include_backup: bool = True,
    include_ICT: bool = True,
    include_ev: bool = True,
    v2g_flag: bool = True,
    fail_rate_trafo: float = 0.0,  # fails per year
    fail_rate_line: float = 0.013,  # fails per year
    inverter: float = 0.0036,
    ev_percentage: float = 0.46,
    ev_E_max: float = 0.07,
    line_repair_time_stat_dist: StatDist = StatDist(
        stat_dist_type=StatDistType.TRUNCNORMAL,
        parameters=NormalParameters(
            loc=1.25,
            scale=1,
            min_val=0.5,
            max_val=2,
        ),
    ),
    microgrid_mode: MicrogridMode = MicrogridMode.LIMITED_SUPPORT,
    battery_capacity: float = 1,  # MWh
    random_seed: int = 2837314,
    iterations: int = 2,
    start_time: TimeStamp = TimeStamp(
        year=2019,
        month=1,
        day=1,
        hour=0,
        minute=0,
        second=0,
    ),
    stop_time: TimeStamp = TimeStamp(
        year=2020,
        month=1,
        day=1,
        hour=0,
        minute=0,
        second=0,
    ),
    save_iterations: list = [1, 2],
    data_dir: str = os.path.join(
        os.pardir,
        "load",
        "data",
    ),
    save_flag: bool = True,
    save_dir: str = "results",
    n_procs: int = 1,
    debug: bool = True,
):

    start = time.time()

    ps = initialize_network(
        include_microgrid=include_microgrid,
        include_production=include_production,
        include_backup=include_backup,
        include_ICT=include_ICT,
        include_ev=include_ev,
        v2g_flag=v2g_flag,
        fail_rate_trafo=fail_rate_trafo,
        fail_rate_line=fail_rate_line,
        inverter=inverter,
        ev_percentage=ev_percentage,
        ev_E_max=ev_E_max,
        line_repair_time_stat_dist=line_repair_time_stat_dist,
        microgrid_mode=microgrid_mode,
        battery_capacity=battery_capacity,
    )

    ps = set_network_load_and_prod(
        power_system=ps,
        include_microgrid=include_microgrid,
        data_dir=data_dir,
    )

    sim = Simulation(ps, random_seed=random_seed)

    sim.run_monte_carlo(
        iterations=iterations,
        start_time=start_time,
        stop_time=stop_time,
        time_step=Time(5, TimeUnit.MINUTE),
        time_unit=TimeUnit.HOUR,
        save_iterations=save_iterations,
        save_dir=save_dir,
        save_flag=save_flag,
        n_procs=n_procs,
        debug=debug,
    )

    end = time.time()
    print("Time elapsed: {}".format(end - start))
