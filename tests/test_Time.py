from relsad.Time import (
    Time,
    TimeUnit,
    TimeStamp,
)


def test_get_seconds():
    hour = Time(1, TimeUnit.HOUR)
    seconds = hour.get_seconds()
    assert seconds == 60*60

def test_get_minutes():
    hour = Time(1, TimeUnit.HOUR)
    minutes = hour.get_minutes()
    assert minutes == 60

def test_get_hours():
    seconds = Time(120, TimeUnit.SECOND)
    hour = seconds.get_hour()
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
    hour = Time(672, TimeUnit.HOUR)
    month = hour.get_month()
    assert month == 1

def test_get_years():
    week = Time(52, TimeUnit.WEEK)
    year = week.get_years()
    assert year == 1


