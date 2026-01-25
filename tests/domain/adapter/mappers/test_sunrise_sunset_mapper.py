import pytest
from weathergrabber.domain.entities.sunrise_sunset import SunriseSunset
from weathergrabber.domain.entities.weather_icon_enum import WeatherIconEnum
from weathergrabber.domain.adapter.mappers.sunrise_sunset_mapper import sunrise_sunset_to_dict, dict_to_sunrise_sunset

def test_sunrise_sunset_to_dict():
    ss = SunriseSunset(sunrise="06:00", sunset="18:00")
    result = sunrise_sunset_to_dict(ss)
    assert result["sunrise"]["icon"]["name"] == "sunrise"
    assert result["sunrise"]["icon"]["emoji_icon"] == "🌅"
    assert result["sunrise"]["value"] == "06:00"
    assert result["sunset"]["icon"]["name"] == "sunset"
    assert result["sunset"]["icon"]["emoji_icon"] == "🌇"
    assert result["sunset"]["value"] == "18:00"
    assert isinstance(result, dict)

def test_sunrise_sunset_to_dict_none():
    class DummyIconValue:
        icon = None
        value = None
    class DummySunriseSunset:
        sunrise = None
        sunset = None
    ss = DummySunriseSunset()
    result = sunrise_sunset_to_dict(ss)
    assert result["sunrise"] is None
    assert result["sunset"] is None
    assert isinstance(result, dict)


def test_dict_to_sunrise_sunset():
    data = {
        "sunrise": {
            "icon": {"name": "sunrise", "fa_icon": "fa-sun", "emoji_icon": "🌅"},
            "value": "06:30"
        },
        "sunset": {
            "icon": {"name": "sunset", "fa_icon": "fa-sun", "emoji_icon": "🌇"},
            "value": "18:45"
        }
    }
    ss = dict_to_sunrise_sunset(data)
    assert isinstance(ss, SunriseSunset)
    assert ss.sunrise.value == "06:30"
    assert ss.sunset.value == "18:45"


def test_dict_to_sunrise_sunset_none_data():
    ss = dict_to_sunrise_sunset(None)
    assert ss is None


def test_dict_to_sunrise_sunset_none_values():
    data = {
        "sunrise": {"value": None},
        "sunset": {"value": None}
    }
    ss = dict_to_sunrise_sunset(data)
    assert ss.sunrise.value is None
    assert ss.sunset.value is None


def test_dict_to_sunrise_sunset_partial_data():
    data = {
        "sunrise": {
            "icon": {"name": "sunrise"},
            "value": "05:45"
        },
        "sunset": {"value": None}
    }
    ss = dict_to_sunrise_sunset(data)
    assert ss.sunrise.value == "05:45"
    assert ss.sunset.value is None


def test_dict_to_sunrise_sunset_roundtrip():
    original = SunriseSunset(sunrise="07:00", sunset="19:00")
    data = sunrise_sunset_to_dict(original)
    reconstructed = dict_to_sunrise_sunset(data)
    assert reconstructed.sunrise.value == original.sunrise.value
    assert reconstructed.sunset.value == original.sunset.value
