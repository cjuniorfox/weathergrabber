from weathergrabber.domain.entities.day_night import DayNight
from weathergrabber.domain.adapter.mappers.day_night_mapper import day_night_to_dict, dict_to_day_night

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


def test_dict_to_day_night():
    data = {
        "day": {"label": "Day", "value": "30°"},
        "night": {"label": "Night", "value": "20°"}
    }
    dn = dict_to_day_night(data)
    assert isinstance(dn, DayNight)
    assert dn.day.label == "Day"
    assert dn.day.value == "30°"
    assert dn.night.label == "Night"
    assert dn.night.value == "20°"


def test_dict_to_day_night_none_values():
    data = {
        "day": None,
        "night": None
    }
    dn = dict_to_day_night(data)
    assert dn.day is None
    assert dn.night is None


def test_dict_to_day_night_partial_data():
    data = {
        "day": {"label": "Day", "value": "25°"},
        "night": None
    }
    dn = dict_to_day_night(data)
    assert dn.day.label == "Day"
    assert dn.night is None


def test_dict_to_day_night_dict_to_temp():
    """Tests the dict_to_temp nested function behavior"""
    data = {
        "day": {"label": "Daytime", "value": "28°C"},
        "night": {"label": "Nighttime", "value": "16°C"}
    }
    dn = dict_to_day_night(data)
    assert isinstance(dn.day, DayNight.Temperature)
    assert isinstance(dn.night, DayNight.Temperature)
    assert dn.day.label == "Daytime"
    assert dn.night.value == "16°C"


def test_dict_to_day_night_roundtrip():
    original = DayNight(
        day=DayNight.Temperature("High", "32°C"),
        night=DayNight.Temperature("Low", "12°C")
    )
    data = day_night_to_dict(original)
    reconstructed = dict_to_day_night(data)
    assert reconstructed.day.label == original.day.label
    assert reconstructed.day.value == original.day.value
    assert reconstructed.night.label == original.night.label
    assert reconstructed.night.value == original.night.value
