from relsad.network.components import (
    Bus,
    Battery,
    BatteryState,
)
from relsad.utils import eq
from relsad.Time import (
    Time,
    TimeUnit,
)


def test_charge_from_min():
    bus = Bus("B1")
    b = Battery(
        name="b",
        bus=bus,
        inj_p_max=1,
        inj_q_max=1,
        E_max=5,
        SOC_min=0.2,
        SOC_max=1,
        n_battery=0.97,
    )
    dt = Time(1, TimeUnit.HOUR)
    prem = b.charge(1, dt)

    assert prem == 0
    assert b.E_battery == 1.97


def test_discharge_from_min():
    bus = Bus("B1")
    b = Battery(
        name="b",
        bus=bus,
        inj_p_max=1,
        inj_q_max=1,
        E_max=5,
        SOC_min=0.2,
        SOC_max=1,
        n_battery=0.97,
    )
    dt = Time(1, TimeUnit.HOUR)
    prem, qrem = b.discharge(0.97, 0, dt)

    assert prem == 0.97
    assert qrem == 0
    assert b.E_battery == 1


def test_charge_from_max():
    bus = Bus("B1")
    b = Battery(
        name="b",
        bus=bus,
        inj_p_max=1,
        inj_q_max=1,
        E_max=5,
        SOC_min=0.2,
        SOC_max=1,
        n_battery=0.97,
    )
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
    b = Battery(
        name="b",
        bus=bus,
        inj_p_max=1,
        inj_q_max=1,
        E_max=5,
        SOC_min=0.2,
        SOC_max=1,
        n_battery=0.97,
    )
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
    b = Battery(
        name="b",
        bus=bus,
        inj_p_max=1,
        inj_q_max=1,
        E_max=5,
        SOC_min=0.2,
        SOC_max=1,
        n_battery=0.97,
    )
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
    b = Battery(
        name="b",
        bus=bus,
        inj_p_max=1,
        inj_q_max=1,
        E_max=5,
        SOC_min=0.2,
        SOC_max=1,
        n_battery=0.97,
    )
    dt = Time(1, TimeUnit.HOUR)
    prem = b.charge(0.5, dt)

    prem, qrem = b.discharge(1, 0, dt)

    assert eq(prem, (1 - 0.5 * 0.97 * 0.97))
    assert eq(qrem, 0)
    assert b.E_battery == 1


def test_charge_above_max():
    bus = Bus("B1")
    b = Battery(
        name="b",
        bus=bus,
        inj_p_max=1,
        inj_q_max=1,
        E_max=5,
        SOC_min=0.2,
        SOC_max=1,
        n_battery=0.97,
    )
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
    b = Battery(
        name="b",
        bus=bus,
        inj_p_max=1,
        inj_q_max=1,
        E_max=5,
        SOC_min=0.2,
        SOC_max=1,
        n_battery=0.97,
    )
    dt = Time(1, TimeUnit.HOUR)
    prem = b.charge(1, dt)

    prem = b.charge(2, dt)

    assert prem == 1, 0
    assert b.E_battery == 1 + 2 * 0.97


def test_update_bus_load_and_prod_charge_normal():
    B1 = Bus("B1")
    dt = Time(1, TimeUnit.HOUR)

    SOC_min = 0.2
    E_max = 5
    n_battery = 0.97

    b = Battery(
        name="b",
        bus=B1,
        inj_p_max=1,
        inj_q_max=1,
        E_max=E_max,
        SOC_min=SOC_min,
        SOC_max=1,
        n_battery=n_battery,
    )

    p = 1

    p_rem, q_rem = b.update_bus_load_and_prod(
        system_load_balance_p=-p,
        system_load_balance_q=0,
        dt=dt,
    )

    assert eq(p_rem, 0, tol=1e-6)
    assert eq(q_rem, 0, tol=1e-6)
    assert eq(B1.pload, p, tol=1e-6)
    assert eq(B1.qload, 0, tol=1e-6)
    assert eq(B1.pprod, 0, tol=1e-6)
    assert eq(B1.qprod, 0, tol=1e-6)
    assert eq(b.SOC, SOC_min + n_battery * p / E_max, tol=1e-6)


def test_update_bus_load_and_prod_charge_low():
    B1 = Bus("B1")
    dt = Time(1, TimeUnit.HOUR)

    SOC_min = 0.2
    E_max = 5
    n_battery = 0.97

    b = Battery(
        name="b",
        bus=B1,
        inj_p_max=1,
        inj_q_max=1,
        E_max=E_max,
        SOC_min=SOC_min,
        SOC_max=1,
        n_battery=n_battery,
    )

    p = 0.5

    p_rem, q_rem = b.update_bus_load_and_prod(
        system_load_balance_p=-p,
        system_load_balance_q=0,
        dt=dt,
    )

    assert eq(p_rem, 0, tol=1e-6)
    assert eq(q_rem, 0, tol=1e-6)
    assert eq(B1.pload, p, tol=1e-6)
    assert eq(B1.qload, 0, tol=1e-6)
    assert eq(B1.pprod, 0, tol=1e-6)
    assert eq(B1.qprod, 0, tol=1e-6)
    assert eq(b.SOC, SOC_min + n_battery * p / E_max, tol=1e-6)


def test_update_bus_load_and_prod_charge_SOC_max():
    B1 = Bus("B1")
    dt = Time(1, TimeUnit.HOUR)

    SOC_min = 0.2
    E_max = 5
    n_battery = 0.97
    SOC_state = 1

    b = Battery(
        name="b",
        bus=B1,
        inj_p_max=1,
        inj_q_max=1,
        E_max=E_max,
        SOC_min=SOC_min,
        SOC_max=1,
        n_battery=n_battery,
    )

    b.set_SOC_state(SOC_state)
    p = 0.5

    p_rem, q_rem = b.update_bus_load_and_prod(
        system_load_balance_p=-p,
        system_load_balance_q=0,
        dt=dt,
    )

    assert eq(p_rem, -p, tol=1e-6)
    assert eq(q_rem, 0, tol=1e-6)
    assert eq(B1.pload, 0, tol=1e-6)
    assert eq(B1.qload, 0, tol=1e-6)
    assert eq(B1.pprod, 0, tol=1e-6)
    assert eq(B1.qprod, 0, tol=1e-6)
    assert eq(b.SOC, SOC_state, tol=1e-6)


def test_update_bus_load_and_prod_discharge_SOC_min():
    B1 = Bus("B1")
    dt = Time(1, TimeUnit.HOUR)

    SOC_min = 0.2
    E_max = 5
    n_battery = 0.97

    b = Battery(
        name="b",
        bus=B1,
        inj_p_max=1,
        inj_q_max=1,
        E_max=E_max,
        SOC_min=SOC_min,
        SOC_max=1,
        n_battery=n_battery,
    )

    p = 1

    p_rem, q_rem = b.update_bus_load_and_prod(
        system_load_balance_p=p,
        system_load_balance_q=0,
        dt=dt,
    )

    assert eq(p_rem, 1, tol=1e-6)
    assert eq(q_rem, 0, tol=1e-6)
    assert eq(B1.pload, 0, tol=1e-6)
    assert eq(B1.qload, 0, tol=1e-6)
    assert eq(B1.pprod, 0, tol=1e-6)
    assert eq(B1.qprod, 0, tol=1e-6)
    assert eq(b.SOC, SOC_min, tol=1e-6)


def test_update_bus_load_and_prod_discharge_SOC_low():
    B1 = Bus("B1")
    dt = Time(1, TimeUnit.HOUR)

    SOC_min = 0.2
    E_max = 2
    n_battery = 0.97
    SOC_state = 0.3

    b = Battery(
        name="b",
        bus=B1,
        inj_p_max=1,
        inj_q_max=1,
        E_max=E_max,
        SOC_min=SOC_min,
        SOC_max=1,
        n_battery=n_battery,
    )
    b.set_SOC_state(SOC_state)
    p = 1

    p_rem, q_rem = b.update_bus_load_and_prod(
        system_load_balance_p=p,
        system_load_balance_q=0,
        dt=dt,
    )

    assert eq(
        p_rem, p - (SOC_state * E_max - SOC_min * E_max) * n_battery, tol=1e-6
    )
    assert eq(q_rem, 0, tol=1e-6)
    assert eq(B1.pload, 0, tol=1e-6)
    assert eq(B1.qload, 0, tol=1e-6)
    assert eq(
        B1.pprod, (SOC_state * E_max - SOC_min * E_max) * n_battery, tol=1e-6
    )
    assert eq(B1.qprod, 0, tol=1e-6)
    assert eq(b.SOC, SOC_min, tol=1e-6)


def test_update_bus_load_and_prod_discharge_SOC_medium():
    B1 = Bus("B1")
    dt = Time(1, TimeUnit.HOUR)

    SOC_min = 0.2
    E_max = 5
    n_battery = 0.97
    SOC_state = 0.5

    b = Battery(
        name="b",
        bus=B1,
        inj_p_max=1,
        inj_q_max=1,
        E_max=E_max,
        SOC_min=SOC_min,
        SOC_max=1,
        n_battery=n_battery,
    )
    b.set_SOC_state(SOC_state)

    p = 1

    p_rem, q_rem = b.update_bus_load_and_prod(
        system_load_balance_p=p,
        system_load_balance_q=0,
        dt=dt,
    )

    assert eq(p_rem, 0, tol=1e-6)
    assert eq(q_rem, 0, tol=1e-6)
    assert eq(B1.pload, 0, tol=1e-6)
    assert eq(B1.qload, 0, tol=1e-6)
    assert eq(B1.pprod, p, tol=1e-6)
    assert eq(B1.qprod, 0, tol=1e-6)
    assert eq(b.SOC, SOC_state - p / n_battery / E_max, tol=1e-6)


def test_update_bus_load_and_prod_discharge_SOC_medium_reactive():
    B1 = Bus("B1")
    dt = Time(1, TimeUnit.HOUR)

    SOC_min = 0.2
    E_max = 5
    n_battery = 0.97
    SOC_state = 0.5

    b = Battery(
        name="b",
        bus=B1,
        inj_p_max=1,
        inj_q_max=1,
        E_max=E_max,
        SOC_min=SOC_min,
        SOC_max=1,
        n_battery=n_battery,
    )
    b.set_SOC_state(SOC_state)

    p = 0
    q = 1

    p_rem, q_rem = b.update_bus_load_and_prod(
        system_load_balance_p=p,
        system_load_balance_q=q,
        dt=dt,
    )

    assert eq(p_rem, 0, tol=1e-6)
    assert eq(q_rem, 0, tol=1e-6)
    assert eq(B1.pload, 0, tol=1e-6)
    assert eq(B1.qload, 0, tol=1e-6)
    assert eq(B1.pprod, p, tol=1e-6)
    assert eq(B1.qprod, q, tol=1e-6)
    assert eq(b.SOC, SOC_state - q / n_battery / E_max, tol=1e-6)


def test_update_bus_load_and_prod_discharge_SOC_medium_active_and_reactive():
    B1 = Bus("B1")
    dt = Time(1, TimeUnit.HOUR)

    SOC_min = 0.2
    E_max = 5
    n_battery = 0.97
    SOC_state = 0.5

    b = Battery(
        name="b",
        bus=B1,
        inj_p_max=1,
        inj_q_max=1,
        E_max=E_max,
        SOC_min=SOC_min,
        SOC_max=1,
        n_battery=n_battery,
    )
    b.set_SOC_state(SOC_state)

    p = 0.5
    q = 0.5

    p_rem, q_rem = b.update_bus_load_and_prod(
        system_load_balance_p=p,
        system_load_balance_q=q,
        dt=dt,
    )

    assert eq(p_rem, 0, tol=1e-6)
    assert eq(q_rem, 0, tol=1e-6)
    assert eq(B1.pload, 0, tol=1e-6)
    assert eq(B1.qload, 0, tol=1e-6)
    assert eq(B1.pprod, p, tol=1e-6)
    assert eq(B1.qprod, q, tol=1e-6)
    assert eq(b.SOC, SOC_state - (p + q) / n_battery / E_max, tol=1e-6)


def test_update_fail_status_failed():
    B1 = Bus("B1")
    dt = Time(1, TimeUnit.HOUR)
    B1.trafo_fail(dt)

    b = Battery(
        name="b",
        bus=B1,
        inj_p_max=1,
        inj_q_max=1,
        E_max=5,
        SOC_min=0.2,
        SOC_max=1,
        n_battery=0.97,
    )

    b.update_fail_status(dt)

    assert b.state == BatteryState.INACTIVE


def test_update_fail_status_not_failed():
    B1 = Bus("B1")
    dt = Time(1, TimeUnit.HOUR)
    B1.trafo_not_fail()

    b = Battery(
        name="b",
        bus=B1,
        inj_p_max=1,
        inj_q_max=1,
        E_max=5,
        SOC_min=0.2,
        SOC_max=1,
        n_battery=0.97,
    )

    b.update_fail_status(dt)

    assert b.state == BatteryState.ACTIVE
