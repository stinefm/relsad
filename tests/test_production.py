import numpy as np

from relsad.network.components import Bus, Production
from relsad.Time import Time, TimeUnit
from relsad.utils import eq


def test_prepare_prod_data_equal_pq():
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

    P1.add_prod_data(
        pprod_data=pprod_data,
        qprod_data=qprod_data,
    )
    time_indices = np.linspace(0, 10, 100)
    P1.prepare_prod_data(time_indices=time_indices)

    assert len(P1.pprod_data) == 100
    assert P1.pprod_data[0] == 1
    assert P1.pprod_data[-1] == 6
    assert len(P1.qprod_data) == 100
    assert P1.qprod_data[0] == 1
    assert P1.qprod_data[-1] == 6


def test_prepare_prod_data_different_pq():
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
            2,
            2,
            8,
        ]
    )

    P1.add_prod_data(
        pprod_data=pprod_data,
        qprod_data=qprod_data,
    )
    time_indices = np.linspace(0, 10, 100)
    P1.prepare_prod_data(time_indices=time_indices)

    assert len(P1.pprod_data) == 100
    assert P1.pprod_data[0] == 1
    assert P1.pprod_data[-1] == 6
    assert len(P1.qprod_data) == 100
    assert P1.qprod_data[0] == 2
    assert P1.qprod_data[-1] == 8


def test_prepare_prod_data_active_prod():
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

    P1.add_prod_data(
        pprod_data=pprod_data,
    )
    time_indices = np.linspace(0, 10, 100)
    P1.prepare_prod_data(time_indices=time_indices)

    assert len(P1.pprod_data) == 100
    assert P1.pprod_data[0] == 1
    assert P1.pprod_data[-1] == 6
    assert len(P1.qprod_data) == 100
    assert P1.qprod_data[0] == 0
    assert P1.qprod_data[-1] == 0


def test_prepare_prod_data_reactive_prod():
    B1 = Bus("B1")
    P1 = Production("P1", B1)

    pprod_data = np.array(
        [
            0,
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

    P1.add_prod_data(
        pprod_data=pprod_data,
        qprod_data=qprod_data,
    )
    time_indices = np.linspace(0, 10, 100)
    P1.prepare_prod_data(time_indices=time_indices)

    assert len(P1.pprod_data) == 100
    assert P1.pprod_data[0] == 0
    assert P1.pprod_data[-1] == 0
    assert len(P1.qprod_data) == 100
    assert P1.qprod_data[0] == 1
    assert P1.qprod_data[-1] == 6


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

        assert P1.pprod == P1.pprod_data[increment[i]]
        assert P1.qprod == P1.qprod_data[increment[i]]


def test_update_bus_prod():

    B1 = Bus("B1")
    P1 = Production("P1", B1)

    P1.add_prod(5, 0)
    P1.update_bus_prod()

    assert B1.pprod == 5
    assert B1.qprod == 0
