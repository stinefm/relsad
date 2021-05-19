from stinetwork.network.components import Bus, Battery
from stinetwork.utils import eq


def test_charge_from_min():
    bus = Bus("B1")
    b = Battery("b", bus, 1, 1, 5, 0.2, 1, 0.97)
    prem = b.charge(1)

    assert prem == 0
    assert b.E_battery == 1.97


def test_discharge_from_min():
    bus = Bus("B1")
    b = Battery("b", bus, 1, 1, 5, 0.2, 1, 0.97)
    prem, qrem = b.discharge(0.97, 0)

    assert prem == 0.97
    assert qrem == 0
    assert b.E_battery == 1


def test_charge_from_max():
    bus = Bus("B1")
    b = Battery("b", bus, 1, 1, 5, 0.2, 1, 0.97)
    rem = b.charge(1)
    rem = b.charge(1)
    rem = b.charge(1)
    rem = b.charge(1)
    rem = b.charge((1 / 0.97 - 1) * 4)

    rem = b.charge(0.5)

    assert eq(rem, 0.5)
    assert b.E_battery == 5


def test_discharge_from_max():
    bus = Bus("B1")
    b = Battery("b", bus, 1, 1, 5, 0.2, 1, 0.97)
    b.charge(1)
    b.charge(1)
    b.charge(1)
    b.charge(1)
    b.charge((1 / 0.97 - 1) * 4)

    prem, qrem = b.discharge(0.5, 0)

    assert prem == 0
    assert qrem == 0
    assert b.E_battery == (5 - 0.5 / 0.97)


def test_discharge_overload():
    bus = Bus("B1")
    b = Battery("b", bus, 1, 1, 5, 0.2, 1, 0.97)
    b.charge(1)
    b.charge(1)
    b.charge(1)
    b.charge(1)
    b.charge((1 / 0.97 - 1) * 4)

    prem, qrem = b.discharge(1.5, 0)

    assert prem == 0.5
    assert qrem == 0
    assert b.E_battery == (5 - 1 / 0.97)


def test_discharge_below_min():
    bus = Bus("B1")
    b = Battery("b", bus, 1, 1, 5, 0.2, 1, 0.97)
    prem = b.charge(0.5)

    prem, qrem = b.discharge(1, 0)

    assert eq(prem, (1 - 0.5 * 0.97 * 0.97))
    assert eq(qrem, 0)
    assert b.E_battery == 1


def test_charge_above_max():
    bus = Bus("B1")
    b = Battery("b", bus, 1, 1, 5, 0.2, 1, 0.97)
    prem = b.charge(1)
    prem = b.charge(1)
    prem = b.charge(1)
    prem = b.charge(1)

    prem = b.charge(1)

    assert eq(prem, (1 - 0.12 / 0.97))
    assert b.E_battery == 5


def test_charge_overload():
    bus = Bus("B1")
    b = Battery("b", bus, 1, 1, 5, 0.2, 1, 0.97)
    prem = b.charge(1)

    prem = b.charge(2)

    assert prem == 1, 0
    assert b.E_battery == 1 + 2 * 0.97
