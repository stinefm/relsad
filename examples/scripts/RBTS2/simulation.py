import time
import os
from relsad.test_networks.RBTS2 import initialize_network
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
from load_and_prod import set_network_load_and_prod


def run_simulation(
    random_seed: int = 2837314,
    save_dir: str = "results",
):

    start = time.time()

    ps = initialize_network()

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
