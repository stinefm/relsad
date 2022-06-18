import os
import sys
from relsad.StatDist import (
    StatDist,
    StatDistType,
    NormalParameters,
)

from simulation import run_simulation

os.chdir(os.path.dirname(os.path.abspath(__file__)))

run_simulation(
    include_microgrid=True,
    include_production=True,
    include_backup=True,
    include_ICT=True,
    include_ev=True,
    v2g_flag=True,
    fail_rate_trafo=0.0,  # fails per year
    fail_rate_line=0.013,  # fails per year
    inverter=0.0036,
    ev_percentage=0.46,
    ev_E_max=0.07,
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
