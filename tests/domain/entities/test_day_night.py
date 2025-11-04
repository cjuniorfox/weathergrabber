import pytest
from weathergrabber.domain.entities.day_night import DayNight

def test_temperature_properties():
    temp = DayNight.Temperature("Day", "30°")
    assert temp.label == "Day"
    assert temp.value == "30°"
    assert str(temp) == "Day: 30°"
    assert "label='Day'" in repr(temp)

def test_temperature_from_string():
    temp = DayNight.Temperature.from_string("Night\xa020°")
    assert temp.label == "Night"
    assert temp.value == "20°"
    assert str(temp) == "Night: 20°"

def test_day_night_properties():
    day = DayNight.Temperature("Day", "30°")
    night = DayNight.Temperature("Night", "20°")
    dn = DayNight(day, night)
    assert dn.day is day
    assert dn.night is night
    assert str(dn) == "Day: Day: 30°, Night: Night: 20°"
    assert "day=" in repr(dn)
    assert "night=" in repr(dn)

def test_day_night_from_string():
    dn = DayNight.from_string("Day\xa030° • Night\xa020°")
    assert dn.day.label == "Day"
    assert dn.day.value == "30°"
    assert dn.night.label == "Night"
    assert dn.night.value == "20°"
    assert str(dn) == "Day: Day: 30°, Night: Night: 20°"
