from weathergrabber.domain.entities.day_night import DayNight
from weathergrabber.domain.adapter.mappers.day_night_mapper import day_night_to_dict

def test_day_night_to_dict():
    day = DayNight.Temperature("Day", "30°")
    night = DayNight.Temperature("Night", "20°")
    dn = DayNight(day, night)
    d = day_night_to_dict(dn)
    assert d["day"]["label"] == "Day"
    assert d["day"]["value"] == "30°"
    assert d["night"]["label"] == "Night"
    assert d["night"]["value"] == "20°"
    assert isinstance(d, dict)
