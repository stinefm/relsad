import time
import os
from relsad.test_networks.IEEE16_modified import initialize_network
from relsad.simulation import Simulation
from relsad.load.bus import CostFunction
from relsad.network.components import MicrogridMode
from relsad.StatDist import (
    StatDist,
    StatDistType,
    NormalParameters,
    GammaParameters,
)
from relsad.Time import (
    Time,
    TimeUnit,
    TimeStamp,
)
from load_and_prod import set_network_load_and_prod


def run_simulation(
    fail_rate_trafo: float = 0.007,
    fail_rate_line: float = 0.7,
    microgrid_mode: MicrogridMode = MicrogridMode.SURVIVAL,
    line_stat_dist: StatDist = StatDist(
        stat_dist_type=StatDistType.TRUNCNORMAL,
        parameters=NormalParameters(
            loc=1.25,
            scale=1,
            min_val=0.5,
            max_val=2,
        ),
    ),
    random_seed: int = 2837314,
    save_dir: str = "results",
):

    start = time.time()

    ps = initialize_network(
        fail_rate_line=fail_rate_line,
        fail_rate_trafo=fail_rate_trafo,
        microgrid_mode=microgrid_mode,
        line_stat_dist=line_stat_dist,
    )

    ps = set_network_load_and_prod(
        power_system=ps,
    )

    sim = Simulation(ps, random_seed=random_seed)

    sim.run_monte_carlo(
        iterations=2,
        start_time=TimeStamp(
            year=2019,
            month=1,
            day=1,
            hour=0,
            minute=0,
            second=0,
        ),
        stop_time=TimeStamp(
            year=2020,
            month=1,
            day=1,
            hour=0,
            minute=0,
            second=0,
        ),
        time_step=Time(5, TimeUnit.MINUTE),
        time_unit=TimeUnit.HOUR,
        save_iterations=[],
        save_dir=save_dir,
        n_procs=10,
        debug=True,
    )

    end = time.time()
    print("Time elapsed: {}".format(end - start))
