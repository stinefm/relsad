import time
import os
from relsad.examples.RBTS2.network import initialize_network
from relsad.simulation import Simulation
from relsad.load.bus import CostFunction
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
from relsad.examples.RBTS2.load_and_prod import set_network_load_and_prod


def run_simulation(
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
    save_flag: bool = True,
    save_dir: str = "results",
    n_procs: int = 1,
    debug: bool = True,
):

    start = time.time()

    ps = initialize_network()

    ps = set_network_load_and_prod(
        power_system=ps,
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
