import os
import time

from relsad.examples.TEST10.load_and_prod import set_network_load_and_prod
from relsad.examples.TEST10.network import initialize_network
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
    fail_rate_trafo: float = 0.007,
    fail_rate_line: float = 0.7,
    fail_rate_intelligent_switch: float = 1000,
    fail_rate_hardware: float = 0.2,
    fail_rate_software: float = 12,
    fail_rate_sensor: float = 0.023,
    p_fail_repair_new_signal: float = 1 - 0.95,
    p_fail_repair_reboot: float = 1 - 0.9,
    include_microgrid: bool = True,
    include_production: bool = True,
    include_ICT: bool = True,
    include_ev: bool = True,
    v2g_flag: bool = True,
    include_backup: bool = True,
    line_repair_time_stat_dist: StatDist = StatDist(
        stat_dist_type=StatDistType.TRUNCNORMAL,
        parameters=NormalParameters(
            loc=1.25,
            scale=1,
            min_val=0.5,
            max_val=2,
        ),
    ),
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
        fail_rate_trafo=fail_rate_trafo,
        fail_rate_line=fail_rate_line,
        fail_rate_intelligent_switch=fail_rate_intelligent_switch,
        fail_rate_hardware=fail_rate_hardware,
        fail_rate_software=fail_rate_software,
        fail_rate_sensor=fail_rate_sensor,
        p_fail_repair_new_signal=p_fail_repair_new_signal,
        p_fail_repair_reboot=p_fail_repair_reboot,
        include_microgrid=include_microgrid,
        include_production=include_production,
        include_ICT=include_ICT,
        include_ev=include_ev,
        v2g_flag=v2g_flag,
        include_backup=include_backup,
        line_repair_time_stat_dist=line_repair_time_stat_dist,
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
