import pytest
from weathergrabber.domain.current_conditions import CurrentConditions

class DummyLocation:
    pass
class DummyTimestamp:
    pass
class DummyIcon:
    pass
class DummyDayNight:
    pass

def test_current_conditions_properties():
    location = DummyLocation()
    timestamp = DummyTimestamp()
    temperature = "22°C"
    icon = DummyIcon()
    summary = "Sunny"
    day_night = DummyDayNight()
    cc = CurrentConditions(location, timestamp, temperature, icon, summary, day_night)
    assert cc.location is location
    assert cc.timestamp is timestamp
    assert cc.temperature == "22°C"
    assert cc.icon is icon
    assert cc.summary == "Sunny"
    assert cc.day_night is day_night
    # Check repr output
    r = repr(cc)
    assert "CurrentConditions(" in r
    assert "location=" in r
    assert "timestamp=" in r
    assert "temperature=" in r
    assert "icon=" in r
    assert "summary=" in r
    assert "day_night=" in r
