import os
import sys

from relsad.examples.CINELDI.simulation import run_simulation
from relsad.network.components import MicrogridMode
from relsad.StatDist import NormalParameters, StatDist, StatDistType

os.chdir(os.path.dirname(os.path.abspath(__file__)))

run_simulation(
    include_ev=True,
    v2g_flag=True,
    line_repair_time_stat_dist=StatDist(
        stat_dist_type=StatDistType.TRUNCNORMAL,
        parameters=NormalParameters(
            loc=1,
            scale=1,
            min_val=0,
            max_val=2,
        ),
    ),
    fail_rate_line=0.026,  # 0.013,  # fails per year
    fail_rate_trafo=0.0,
    ev_percentage=0.61,
    ev_E_max=0.07,
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
