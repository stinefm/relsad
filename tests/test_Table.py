import numpy as np
from relsad.Table import Table


def num_ev_table_func():
    return Table(
        x=np.array(
            [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15,
                16,
                17,
                18,
                19,
                20,
                21,
                22,
                23,
            ],
        ),
        y=np.array(
            [
                0.52,
                0.52,
                0.52,
                0.52,
                0.52,
                0.52,
                0.52,
                0.08,
                0.08,
                0.18,
                0.18,
                0.18,
                0.18,
                0.18,
                0.18,
                0.18,
                0.28,
                0.28,
                0.28,
                0.28,
                0.42,
                0.42,
                0.42,
                0.42,
            ]
        ),
    )


def test_get_values():
    table = num_ev_table_func()
    assert table.get_value(7) == 0.08
    assert table.get_value(12) == 0.18
    assert table.get_value(19) == 0.28
    assert table.get_value(23) == 0.42
