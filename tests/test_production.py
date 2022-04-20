from relsad.network.components import Bus, Production
from relsad.utils import eq
from relsad.Time import (
    Time,
    TimeUnit,
)

def test_update_bus_prod():

    B1 = Bus("B1")
    P1 = Production("P1", B1)

    P1.add_prod(5, 0)
    P1.update_bus_prod()

    assert B1.pprod == 5
    assert B1.qprod == 0