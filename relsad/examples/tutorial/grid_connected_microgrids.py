from relsad.examples.tutorial.system_components import *

from relsad.network.systems import (
    PowerSystem,
    Transmission,
    Distribution,
)

from relsad.network.systems import Microgrid

from relsad.network.components import MicrogridMode

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

# Buses:

M1 = Bus(
    name="M1",
    n_customers=1,
    coordinate=[-1, -2],
)

M2 = Bus(
    name="M2",
    n_customers=1,
    coordinate=[-2, -3],
)

M3 = Bus(
    name="M3",
    n_customers=1,
    coordinate=[-1, -3],
)

# Lines:

ML1 = Line(
    name="ML1",
    fbus=B2,
    tbus=M1,
    r=0.5,
    x=0.5,
    fail_rate_density_per_year=fail_rate_line,
    repair_time_dist=line_stat_repair_time_dist,
)

ML2 = Line(
    name="ML2",
    fbus=M1,
    tbus=M2,
    r=0.5,
    x=0.5,
    fail_rate_density_per_year=fail_rate_line,
    repair_time_dist=line_stat_repair_time_dist,
)

ML3 = Line(
    name="ML3",
    fbus=M1,
    tbus=M3,
    r=0.5,
    x=0.5,
    fail_rate_density_per_year=fail_rate_line,
    repair_time_dist=line_stat_repair_time_dist,
)

# Circuit breaker:

E2 = CircuitBreaker(name="E2", line=ML1)

# Disconnectors:

DML1a = Disconnector(
    name="ML1a",
    line=ML1,
    bus=B2,
)
DML1b = Disconnector(
    name="ML1b",
    line=ML1,
    bus=M1,
)
DML2a = Disconnector(
    name="ML2a",
    line=ML2,
    bus=M1,
)
DML2b = Disconnector(
    name="ML2b",
    line=ML2,
    bus=M2,
)
DML3a = Disconnector(
    name="ML3a",
    line=ML3,
    bus=M1,
)
DML4b = Disconnector(
    name="ML4b",
    line=ML3,
    bus=M3,
)

m = Microgrid(
    distribution_network=dn,
    connected_line=ML1,
    mode=MicrogridMode.FULL_SUPPORT,
)
m.add_buses([M1, M2, M3])
m.add_lines([ML2, ML3])
