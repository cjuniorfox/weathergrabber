import pytest
from weathergrabber.domain.sunrise_sunset import SunriseSunset
from weathergrabber.domain.weather_icon_enum import WeatherIconEnum

def test_sunrise_sunset_properties():
    sunrise = "06:00"
    sunset = "18:00"
    ss = SunriseSunset(sunrise, sunset)
    assert ss.sunrise.value == "06:00"
    assert ss.sunset.value == "18:00"
    assert ss.sunrise.icon == WeatherIconEnum.SUNRISE
    assert ss.sunset.icon == WeatherIconEnum.SUNSET
    s = str(ss)
    assert "Sunrise:" in s
    assert "Sunset:" in s
    r = repr(ss)
    assert "SunriseSunset(" in r
    assert "sunrise=" in r
    assert "sunset=" in r

def test_icon_value_str_and_repr():
    icon_value = SunriseSunset.IconValue(WeatherIconEnum.SUNRISE, "05:30")
    s = str(icon_value)
    assert WeatherIconEnum.SUNRISE.emoji_icon in s
    assert "05:30" in s
    r = repr(icon_value)
    assert "IconValue(" in r
    assert "icon=" in r
    assert "value='05:30'" in r
