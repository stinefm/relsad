from relsad.network.components import (
    Bus,
    Line,
    Disconnector,
    CircuitBreaker,
    ManualMainController,
)
from relsad.Time import (
    Time,
    TimeUnit,
    TimeStamp,
)
from relsad.StatDist import (
    StatDist,
    StatDistType,
    NormalParameters,
)


# Failure rate and outage time of the transformer on the bus
# are not necessary to add, this can be added on each bus.
# Their default values are 0 and Time(0) respectively.

B1 = Bus(
    name="B1",
    n_customers=0,
    coordinate=[0, 0],
)
B2 = Bus(
    name="B2",
    n_customers=1,
    coordinate=[1, 0],
)

B3 = Bus(
    name="B3",
    n_customers=1,
    coordinate=[2, 1],
)

B4 = Bus(
    name="B4",
    n_customers=1,
    coordinate=[2, 0],
)

B5 = Bus(
    name="B5",
    n_customers=1,
    coordinate=[3, 0],
)

B6 = Bus(
    name="B6",
    n_customers=1,
    coordinate=[3, 1],
)

# Failure rate and outage time of the lines can be added to each line.
# The default value of the line failure rate is 0, while the default
# outage time is 0 (Uniform float distribution with max/min values of 0).

# For adding statistical distributions, in this case a
# truncated normal distribution:

line_stat_repair_time_dist = StatDist(
    stat_dist_type=StatDistType.TRUNCNORMAL,
    parameters=NormalParameters(
        loc=1.25,
        scale=1,
        min_val=0.5,
        max_val=2,
    ),
)

fail_rate_line = 0.07

L1 = Line(
    name="L1",
    fbus=B1,
    tbus=B2,
    r=0.5,
    x=0.5,
    fail_rate_density_per_year=fail_rate_line,
    repair_time_dist=line_stat_repair_time_dist,
)
L2 = Line(
    name="L2",
    fbus=B2,
    tbus=B3,
    r=0.5,
    x=0.5,
    fail_rate_density_per_year=fail_rate_line,
    repair_time_dist=line_stat_repair_time_dist,
)
L3 = Line(
    name="L3",
    fbus=B2,
    tbus=B4,
    r=0.5,
    x=0.5,
    fail_rate_density_per_year=fail_rate_line,
    repair_time_dist=line_stat_repair_time_dist,
)
L4 = Line(
    name="L4",
    fbus=B4,
    tbus=B5,
    r=0.5,
    x=0.5,
    fail_rate_density_per_year=fail_rate_line,
    repair_time_dist=line_stat_repair_time_dist,
)
L5 = Line(
    name="L5",
    fbus=B3,
    tbus=B6,
    r=0.5,
    x=0.5,
    fail_rate_density_per_year=fail_rate_line,
    repair_time_dist=line_stat_repair_time_dist,
)

# Backup line

L6 = Line(
    name="L6",
    fbus=B4,
    tbus=B6,
    r=0.5,
    x=0.5,
    fail_rate_density_per_year=fail_rate_line,
    repair_time_dist=line_stat_repair_time_dist,
)

# Set L6 as a backup line

L6.set_backup()

E1 = CircuitBreaker(
    name="E1",
    line=L1,
)

DL1a = Disconnector(
    name="L1a",
    line=L1,
    bus=B1,
)
DL1b = Disconnector(
    name="L1b",
    line=L1,
    bus=B2,
)
DL2a = Disconnector(
    name="L2a",
    line=L2,
    bus=B2,
)
DL2b = Disconnector(
    name="L2b",
    line=L2,
    bus=B3,
)
DL3a = Disconnector(
    name="L3a",
    line=L3,
    bus=B2,
)
DL3b = Disconnector(
    name="L3b",
    line=L3,
    bus=B4,
)
DL4a = Disconnector(
    name="L4a",
    line=L4,
    bus=B4,
)
DL4b = Disconnector(
    name="L4b",
    line=L4,
    bus=B5,
)
DL5a = Disconnector(
    name="L5a",
    line=L5,
    bus=B3,
)
DL5b = Disconnector(
    name="L5b",
    line=L5,
    bus=B6,
)

# For backup line
DL6a = Disconnector(
    name="L6a",
    line=L6,
    bus=B4,
)
DL6b = Disconnector(
    name="L6b",
    line=L6,
    bus=B6,
)

C1 = ManualMainController(name="C1", sectioning_time=Time(0))
