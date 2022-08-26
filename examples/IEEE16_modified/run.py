import os
import sys

from relsad.examples.IEEE16_modified.simulation import run_simulation
from relsad.network.components import MicrogridMode
from relsad.StatDist import NormalParameters, StatDist, StatDistType

os.chdir(os.path.dirname(os.path.abspath(__file__)))

run_simulation(
    fail_rate_trafo=0.007,
    fail_rate_line=0.7,
    microgrid_mode=MicrogridMode.SURVIVAL,
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
