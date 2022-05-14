from relsad.Time import (
    Time,
    TimeUnit,
    TimeStamp,
)
from relsad.utils import eq


def test_get_seconds():
    hour = Time(1, TimeUnit.HOUR)
    seconds = hour.get_seconds()
    assert seconds == 60 * 60


def test_get_minutes():
    hour = Time(1, TimeUnit.HOUR)
    minutes = hour.get_minutes()
    assert minutes == 60


def test_get_hours():
    minutes = Time(120, TimeUnit.MINUTE)
    hour = minutes.get_hours()
    assert hour == 2


def test_get_days():
    hour = Time(72, TimeUnit.HOUR)
    day = hour.get_days()
    assert day == 3


def test_get_weeks():
    day = Time(7, TimeUnit.DAY)
    week = day.get_weeks()
    assert week == 1


def test_get_months():
    hour = Time(729.9936, TimeUnit.HOUR)
    month = hour.get_months()
    assert eq(month, 1, tol=1e-6)


def test_get_years():
    week = Time(52.1424, TimeUnit.WEEK)
    year = week.get_years()
    assert eq(year, 1, tol=1e-6)
