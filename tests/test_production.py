from relsad.network.components import Bus, Production
from relsad.utils import eq
import numpy as np
from relsad.Time import (
    Time,
    TimeUnit,
)


def test_prepare_prod_data():
    B1 = Bus("B1")
    P1 = Production("P1", B1)

    pprod_data = np.array(
        [
            1,
            2,
            3,
            4,
            5,
            6,
        ]
    )
    qprod_data = np.array(
        [
            1,
            2,
            3,
            4,
            5,
            6,
        ]
    )

    P1.add_prod_data(pprod_data=pprod_data, qprod_data=qprod_data)
    time_indices = np.linspace(0, 10, 100)
    P1.prepare_prod_data(time_indices=time_indices)

    assert len(P1.pprod_data) == 100
    assert len(P1.qprod_data) == 100


def test_set_prod():
    B1 = Bus("B1")
    P1 = Production("P1", B1)

    pprod_data = np.array(
        [
            1,
            2,
            3,
            4,
            5,
            6,
        ]
    )
    qprod_data = np.array(
        [
            1,
            2,
            3,
            4,
            5,
            6,
        ]
    )
    increment = [0, 1, 2, 3, 4, 5]

    P1.add_prod_data(pprod_data=pprod_data, qprod_data=qprod_data)

    for i in range(len(increment)):
        P1.set_prod(increment[i])
        




def test_update_bus_prod():

    B1 = Bus("B1")
    P1 = Production("P1", B1)

    P1.add_prod(5, 0)
    P1.update_bus_prod()

    assert B1.pprod == 5
    assert B1.qprod == 0