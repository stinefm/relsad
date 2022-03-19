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

