from relsad.network.components import Bus, Line
from relsad.utils import eq
import numpy as np
from relsad.Time import (
    Time,
    TimeUnit,
)


def test_disconnect():
    B1 = Bus("B1")
    B2 = Bus("B2")
    L1 = Line("L1", B1, B2, 0.5, 0.5)

    L1.disconnect()

    assert L1.connected is False
    assert B1.toline is None
    assert B1.fromline is None
    assert B2.toline is None
    assert B2.fromline is None


def test_connect():
    B1 = Bus("B1")
    B2 = Bus("B2")
    L1 = Line("L1", B1, B2, 0.5, 0.5)

    L1.connect()

    assert L1.connected is True
    assert B1.toline is None
    assert B1.fromline == L1
    assert B2.toline == L1
    assert B2.fromline is None


def test_change_direction():
    B1 = Bus("B1")
    B2 = Bus("B2")
    L1 = Line("L1", B1, B2, 0.5, 0.5)

    L1.change_direction()

    assert B1.toline == L1
    assert B1.fromline is None
    assert B2.toline is None
    assert B2.fromline == L1


def test_update_fail_status():
    B1 = Bus("B1")
    B2 = Bus("B2")
    Line("L1", B1, B2, 0.5, 0.5)
