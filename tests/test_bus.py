from relsad.network.components import Bus, Battery, Production
from relsad.utils import eq
from relsad.load.bus import CostFunction
import numpy as np
from relsad.Time import (
    Time,
    TimeUnit,
)


def test_add_load():
    B1 = Bus("B1")
    B1.add_load(0.05, 0.005)

    assert B1.pload == 0.05
    assert B1.qload == 0.005

def test_perpare_load_data_equal_pq():
    B1 = Bus("B1")
    pload_data = np.array(
        [
            1,
            2,
            3,
            4,
            5,
            6,
        ]
    )

    qload_data = np.array(
        [
            1,
            2,
            3,
            4,
            5,
            6,
        ]
    )

    B1.add_load_data(
        pload_data=pload_data, qload_data=qload_data,
    )
    time_indices = np.linspace(0, 10, 100)
    B1.prepare_load_data(time_indices=time_indices)

    assert len(B1.pload_data[0]) == 100
    assert B1.pload_data[0][0] == 1
    assert B1.pload_data[0][-1] == 6
    assert len(B1.qload_data[0]) == 100
    assert B1.qload_data[0][0] == 1
    assert B1.qload_data[0][-1] == 6

def test_perpare_load_data_different_pq():
    B1 = Bus("B1")
    pload_data = np.array(
        [
            2,
            3,
            4,
            5,
            6,
        ]
    )

    qload_data = np.array(
        [
            1,
            2,
            8,
        ]
    )

    B1.add_load_data(
        pload_data=pload_data, qload_data=qload_data,
    )
    time_indices = np.linspace(0, 10, 100)
    B1.prepare_load_data(time_indices=time_indices)

    assert len(B1.pload_data[0]) == 100
    assert B1.pload_data[0][0] == 2
    assert B1.pload_data[0][-1] == 6
    assert len(B1.qload_data[0]) == 100
    assert B1.qload_data[0][0] == 1
    assert B1.qload_data[0][-1] == 8

def test_perpare_load_data_active_load():
    B1 = Bus("B1")
    pload_data = np.array(
        [
            2,
            3,
            4,
            5,
            6,
        ]
    )


    B1.add_load_data(
        pload_data=pload_data,
    )
    time_indices = np.linspace(0, 10, 100)
    B1.prepare_load_data(time_indices=time_indices)

    assert len(B1.pload_data[0]) == 100
    assert B1.pload_data[0][0] == 2
    assert B1.pload_data[0][-1] == 6
    assert len(B1.qload_data[0]) == 100
    assert B1.qload_data[0][0] == 0
    assert B1.qload_data[0][-1] == 0

def test_perpare_load_data_reactive_load():
    B1 = Bus("B1")
    pload_data = np.array(
        [
            0
        ]
    )

    qload_data = np.array(
        [
            1,
            2,
            3,
            4,
            5,
            6,
        ]
    )


    B1.add_load_data(
        pload_data=pload_data, qload_data=qload_data
    )
    time_indices = np.linspace(0, 10, 100)
    B1.prepare_load_data(time_indices=time_indices)

    assert len(B1.pload_data[0]) == 100
    assert B1.pload_data[0][0] == 0
    assert B1.pload_data[0][-1] == 0
    assert len(B1.qload_data[0]) == 100
    assert B1.qload_data[0][0] == 1
    assert B1.qload_data[0][-1] == 6

def test_set_load_and_cost():
    B1 = Bus("B1")
    pload_data = np.array([1, 2, 3, 4, 5, 6])
    qload_data = np.array([1, 2, 3, 4, 5, 6])

    cost_function = CostFunction(1, 0)
    increment = [0, 1, 2, 3, 4, 5]

    B1.add_load_data(pload_data=pload_data, qload_data=qload_data, cost_function=cost_function)
    for i in range(len(increment)):
        B1.set_load_and_cost(increment[i])
    
        assert B1.cost == 1
        assert B1.pload == B1.pload_data[0][increment[i]] 
        assert B1.qload == B1.qload_data[0][increment[i]] 
 
 

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




