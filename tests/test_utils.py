import numpy as np
from relsad.utils import (
    eq,
    interpolate,
    convert_yearly_fail_rate,
)
from relsad.Time import (
    Time,
    TimeUnit,
)


def test_eq():
    assert eq(1.0e-6, 1.1e-6, tol=1e-6)


def test_interpolate():
    unit_load = np.ones(2)

    time_array = np.arange(
        stop=8760,
        step=1,
    )

    time_array_indices = np.arange(len(time_array))
    interpolated_data = interpolate(
        array=5e-3 * unit_load,
        time_indices=time_array_indices,
    )
    assert max(interpolated_data) == 5e-3
    assert min(interpolated_data) == 5e-3


def test_convert_yearly_fail_rate():
    assert eq(
        convert_yearly_fail_rate(
            fail_rate_per_year=0.07,
            dt=Time(1, TimeUnit.HOUR),
        ),
        0.07 / 8760,
    )
    assert eq(
        convert_yearly_fail_rate(
            fail_rate_per_year=0.07,
            dt=Time(1, TimeUnit.MINUTE),
        ),
        0.07 / 8760 / 60,
    )
    assert eq(
        convert_yearly_fail_rate(
            fail_rate_per_year=0.07,
            dt=Time(1, TimeUnit.SECOND),
        ),
        0.07 / 8760 / 60 / 60,
    )
