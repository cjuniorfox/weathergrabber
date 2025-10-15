import pytest
from weathergrabber.domain.sunrise_sunset import SunriseSunset
from weathergrabber.domain.weather_icon_enum import WeatherIconEnum
from weathergrabber.domain.adapter.mapper.sunrise_sunset_mapper import sunrise_sunset_to_dict

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
