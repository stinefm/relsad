from relsad.examples.tutorial.system_components import *

from relsad.network.systems import (
    PowerSystem,
    Transmission,
    Distribution,
)

from relsad.load.bus import CostFunction

from relsad.visualization.plotting import plot_topology

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


load_household = np.ones(365 * 24) * 0.05  # MW

household = CostFunction(
    A=8.8,
    B=14.7,
)

B2.add_load_data(
    pload_data=load_household,
    cost_function=household,
)

B3.add_load_data(
    pload_data=load_household,
    cost_function=household,
)


ps = PowerSystem(controller=C1)

tn = Transmission(
    parent_network=ps,
    trafo_bus=B1,
)

dn = Distribution(
    parent_network=tn,
    connected_line=L1,
)
dn.add_buses([B2, B3, B4, B5, B6])
dn.add_lines([L2, L3, L4, L5, L6])

fig = plot_topology(
    buses=ps.buses,
    lines=ps.lines,
    bus_text=True,
    line_text=True,
)

fig.savefig(
    "test_network.png",
    dpi=600,
)
os.remove("test_network.png")
