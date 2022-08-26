import os
import time

from relsad.examples.CINELDI.load_and_prod import set_network_load_and_prod
from relsad.examples.CINELDI.network import initialize_network
from relsad.load.bus import CostFunction
from relsad.simulation import Simulation
from relsad.StatDist import (
    GammaParameters,
    NormalParameters,
    StatDist,
    StatDistType,
)
from relsad.Time import Time, TimeStamp, TimeUnit


def run_simulation(
    include_microgrid=True,
    include_production=True,
    include_ev: bool = True,
    v2g_flag: bool = True,
    line_repair_time_stat_dist: StatDist = StatDist(
        stat_dist_type=StatDistType.TRUNCNORMAL,
        parameters=NormalParameters(
            loc=1,
            scale=1,
            min_val=0,
            max_val=2,
        ),
    ),
    fail_rate_line: float = 0.026,  # 0.013,  # fails per year
    fail_rate_trafo: float = 0.0,  # fails per year
    ev_percentage: float = 0.46,
    ev_E_max: float = 0.07,
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
        include_ev=include_ev,
        v2g_flag=v2g_flag,
        line_repair_time_stat_dist=line_repair_time_stat_dist,
        fail_rate_line=fail_rate_line,  # fails per year
        fail_rate_trafo=fail_rate_trafo,
        ev_percentage=ev_percentage,
        ev_E_max=ev_E_max,
        include_ICT=False,
    )

    ps = set_network_load_and_prod(
        power_system=ps,
        include_microgrid=include_microgrid,
        include_production=include_production,
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
