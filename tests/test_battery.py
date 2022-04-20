from relsad.network.components import Bus, Battery
from relsad.utils import eq
from relsad.Time import (
    Time,
    TimeUnit,
)


def test_charge_from_min():
    bus = Bus("B1")
    b = Battery("b", bus, 1, 1, 5, 0.2, 1, 0.97)
    dt = Time(1, TimeUnit.HOUR)
    prem = b.charge(1, dt)

    assert prem == 0
    assert b.E_battery == 1.97


def test_discharge_from_min():
    bus = Bus("B1")
    b = Battery("b", bus, 1, 1, 5, 0.2, 1, 0.97)
    dt = Time(1, TimeUnit.HOUR)
    prem, qrem = b.discharge(0.97, 0, dt)

    assert prem == 0.97
    assert qrem == 0
    assert b.E_battery == 1


def test_charge_from_max():
    bus = Bus("B1")
    b = Battery("b", bus, 1, 1, 5, 0.2, 1, 0.97)
    dt = Time(1, TimeUnit.HOUR)
    rem = b.charge(1, dt)
    rem = b.charge(1, dt)
    rem = b.charge(1, dt)
    rem = b.charge(1, dt)
    rem = b.charge((1 / 0.97 - 1) * 4, dt)

    rem = b.charge(0.5, dt)

    assert eq(rem, 0.5)
    assert b.E_battery == 5


def test_discharge_from_max():
    bus = Bus("B1")
    b = Battery("b", bus, 1, 1, 5, 0.2, 1, 0.97)
    dt = Time(1, TimeUnit.HOUR)
    b.charge(1, dt)
    b.charge(1, dt)
    b.charge(1, dt)
    b.charge(1, dt)
    b.charge((1 / 0.97 - 1) * 4, dt)

    prem, qrem = b.discharge(0.5, 0, dt)

    assert prem == 0
    assert qrem == 0
    assert b.E_battery == (5 - 0.5 / 0.97)


def test_discharge_overload():
    bus = Bus("B1")
    b = Battery("b", bus, 1, 1, 5, 0.2, 1, 0.97)
    dt = Time(1, TimeUnit.HOUR)
    b.charge(1, dt)
    b.charge(1, dt)
    b.charge(1, dt)
    b.charge(1, dt)
    b.charge((1 / 0.97 - 1) * 4, dt)

    prem, qrem = b.discharge(1.5, 0, dt)

    assert prem == 0.5
    assert qrem == 0
    assert b.E_battery == (5 - 1 / 0.97)


def test_discharge_below_min():
    bus = Bus("B1")
    b = Battery("b", bus, 1, 1, 5, 0.2, 1, 0.97)
    dt = Time(1, TimeUnit.HOUR)
    prem = b.charge(0.5, dt)

    prem, qrem = b.discharge(1, 0, dt)

    assert eq(prem, (1 - 0.5 * 0.97 * 0.97))
    assert eq(qrem, 0)
    assert b.E_battery == 1


def test_charge_above_max():
    bus = Bus("B1")
    b = Battery("b", bus, 1, 1, 5, 0.2, 1, 0.97)
    dt = Time(1, TimeUnit.HOUR)
    prem = b.charge(1, dt)
    prem = b.charge(1, dt)
    prem = b.charge(1, dt)
    prem = b.charge(1, dt)

    prem = b.charge(1, dt)

    assert eq(prem, (1 - 0.12 / 0.97))
    assert b.E_battery == 5


def test_charge_overload():
    bus = Bus("B1")
    b = Battery("b", bus, 1, 1, 5, 0.2, 1, 0.97)
    dt = Time(1, TimeUnit.HOUR)
    prem = b.charge(1, dt)

    prem = b.charge(2, dt)

    assert prem == 1, 0
    assert b.E_battery == 1 + 2 * 0.97

def test_update_bus_load_prod():
    pass

def test_update_fail_status_failed():
    B1 = Bus("B1")
    dt = Time(1, TimeUnit.HOUR)
    B1.trafo_fail(dt)

    b = Battery("b", B1, 1, 1, 5, 0.2, 1, 0.97)

    b.update_fail_status(dt)

    assert b.lock == True

def test_update_fail_status_not_failed(): 
    B1 = Bus("B1")
    dt = Time(1, TimeUnit.HOUR)
    B1.trafo_not_fail()

    b = Battery("b", B1, 1, 1, 5, 0.2, 1, 0.97)

    b.update_fail_status(dt)

    assert b.lock == False


