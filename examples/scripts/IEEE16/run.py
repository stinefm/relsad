import os
import sys
from relsad.network.components import (
    MicrogridMode,
)
from relsad.StatDist import (
    StatDist,
    StatDistType,
    NormalParameters,
)

from simulation import run_simulation

os.chdir(os.path.dirname(os.path.abspath(__file__)))

run_simulation(
    fail_rate_trafo=0.007,
    fail_rate_line=0.7,
    microgrid_mode=MicrogridMode.SURVIVAL,
    line_stat_dist=StatDist(
        stat_dist_type=StatDistType.TRUNCNORMAL,
        parameters=NormalParameters(
            loc=1.25,
            scale=1,
            min_val=0.5,
            max_val=2,
        ),
    ),
    random_seed=2837314,
    save_dir="results",
)
