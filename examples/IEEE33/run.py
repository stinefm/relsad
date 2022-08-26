import os
import sys

from relsad.examples.IEEE33.simulation import run_simulation
from relsad.network.components import MicrogridMode
from relsad.StatDist import NormalParameters, StatDist, StatDistType

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
    line_repair_time_stat_dist=StatDist(
        stat_dist_type=StatDistType.TRUNCNORMAL,
        parameters=NormalParameters(
            loc=1.25,
            scale=1,
            min_val=0.5,
            max_val=2,
        ),
    ),
    microgrid_mode=MicrogridMode.LIMITED_SUPPORT,
    battery_capacity=1,  # MWh
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
