import os
import sys

from relsad.examples.RBTS2.simulation import run_simulation
from relsad.network.components import MicrogridMode
from relsad.StatDist import NormalParameters, StatDist, StatDistType

os.chdir(os.path.dirname(os.path.abspath(__file__)))

run_simulation(
    random_seed=2837314,
    save_dir="results",
)
