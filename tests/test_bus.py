from relsad.network.components import Bus, Battery, Production
from relsad.utils import eq
from relsad.Time import (
    Time,
    TimeUnit,
)


def test_add_load():
    B1 = Bus("B1")
    B1.add_load(0.05, 0.005)

    assert B1.pload == 0.05
    assert B1.qload == 0.005

def test_trafo_fail():
    B1 = Bus("B1")
    dt = Time(1, TimeUnit.HOUR)

    P = Production("P1", B1)

    P.add_prod_data(pprod_data=[0.5], qprod_data=[0])

    B1.trafo_fail(dt)

    assert B1.trafo_failed == True
    assert P.pprod == 0
    assert P.qprod == 0

def update_fail_status():
    pass 




