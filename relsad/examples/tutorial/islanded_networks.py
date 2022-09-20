from relsad.examples.tutorial.system_components import *

from relsad.network.systems import Distribution, PowerSystem

ps = PowerSystem(controller=C1)

dn = Distribution(
    parent_network=ps,
    connected_line=None,
)
dn.add_buses([B1, B2, B3, B4, B5, B6])
dn.add_lines([L1, L2, L3, L4, L5, L6])
