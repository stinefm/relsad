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
    random_seed=2837314,
    save_dir="results",
)
