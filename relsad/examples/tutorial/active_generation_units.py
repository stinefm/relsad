from relsad.examples.tutorial.system_components import *

from relsad.network.components import (
    Production,
    Battery,
    EVPark,
)
from relsad.Table import Table

import numpy as np

# A generation unit:

P1 = Production(
    name="P1",
    bus=B3,
)

# A battery:

Bat1 = Battery(
    name="B1",
    bus=B6,
)

# An EV park

num_ev_table = Table(
    x=np.arange(0, 24),  # Hour of the day
    y=np.ones(24) * 10,  # Number of EVs
)

EVPark(
    name="EV1",
    bus=B5,
    num_ev_dist=num_ev_table,
    v2g_flag=True,
)

generation_profile = np.ones(365 * 24) * 0.02  # MW
P1.add_prod_data(
    pprod_data=generation_profile,
)
