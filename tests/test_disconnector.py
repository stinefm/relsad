from relsad.network.components import Bus, CircuitBreaker, Disconnector, Line
from relsad.Time import Time, TimeUnit
from relsad.utils import eq


def test_close():
    B1 = Bus("B1")
    B2 = Bus("B2")
    L1 = Line("L1", B1, B2, 0.5, 0.5)
    D1 = Disconnector("D1", L1, B1)

    D1.close()

    assert D1.is_open is False


def test_open():
    B1 = Bus("B1")
    B2 = Bus("B2")
    L1 = Line("L1", B1, B2, 0.5, 0.5)
    D1 = Disconnector("D1", L1, B1)

    D1.open()

    assert D1.is_open is True
