from relsad.network.components import Bus, CircuitBreaker, Disconnector, Line
from relsad.Time import Time, TimeUnit
from relsad.utils import eq


def test_close():
    B1 = Bus("B1")
    B2 = Bus("B2")
    L1 = Line("L1", B1, B2, 0.5, 0.5)
    CB = CircuitBreaker("CB", L1)

    CB.close()

    assert CB.is_open is False
    assert L1.connected is True


def test_open():
    B1 = Bus("B1")
    B2 = Bus("B2")
    L1 = Line("L1", B1, B2, 0.5, 0.5)
    CB = CircuitBreaker("CB", L1)

    CB.open()

    assert CB.is_open is True
    assert L1.connected is False
