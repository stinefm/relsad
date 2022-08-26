import os
import sys

from relsad.examples.TEST10.simulation import run_simulation
from relsad.network.components import MicrogridMode
from relsad.StatDist import NormalParameters, StatDist, StatDistType

# Set path to file path
os.chdir(os.path.dirname(os.path.abspath(__file__)))

run_simulation(
    fail_rate_trafo=0.007,
    fail_rate_line=0.7,
    fail_rate_intelligent_switch=1000,
    fail_rate_hardware=0.2,
    fail_rate_software=12,
    fail_rate_sensor=0.023,
    p_fail_repair_new_signal=1 - 0.95,
    p_fail_repair_reboot=1 - 0.9,
    include_microgrid=True,
    include_production=True,
    include_ICT=True,
    include_ev=True,
    v2g_flag=True,
    include_backup=True,
    line_repair_time_stat_dist=StatDist(
        stat_dist_type=StatDistType.TRUNCNORMAL,
        parameters=NormalParameters(
            loc=1.25,
            scale=1,
            min_val=0.5,
            max_val=2,
        ),
    ),
    random_seed=2837314,
    data_dir=os.path.join(
        os.pardir,
        os.pardir,
        "relsad",
        "examples",
        "load",
        "data",
    ),
    save_dir="results",
)
