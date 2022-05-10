from relsad.Time import (
    Time,
    TimeUnit,
    TimeStamp,
)
from relsad.utils import eq


def test_hour_of_day_1():
    start_time = TimeStamp(
        year=0,
        month=0,
        day=0,
        hour=0,
        minute=0,
        second=0,
    )
    time_passed = Time(1, TimeUnit.HOUR)
    assert start_time.get_hour_of_day(time_passed=time_passed) == 1

def test_hour_of_day_2():
    start_time = TimeStamp(
        year=0,
        month=0,
        day=0,
        hour=0,
        minute=0,
        second=0,
    )
    time_passed = Time(400, TimeUnit.MINUTE)
    assert start_time.get_hour_of_day(time_passed=time_passed) == 6

def test_hour_of_day_3():
    start_time = TimeStamp(
        year=0,
        month=0,
        day=0,
        hour=0,
        minute=30,
        second=0,
    )
    time_passed = Time(400, TimeUnit.MINUTE)
    assert start_time.get_hour_of_day(time_passed=time_passed) == 7