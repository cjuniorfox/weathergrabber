import pytest
from weathergrabber.domain.entities.weather_icon_enum import WeatherIconEnum
from weathergrabber.domain.adapter.mappers.weather_icon_enum_mapper import weather_icon_enum_to_dict, dict_to_weather_icon_enum

def test_weather_icon_enum_to_dict():
    icon = WeatherIconEnum.SUNNY
    result = weather_icon_enum_to_dict(icon)
    assert result["name"] == "sunny"
    assert isinstance(result["fa_icon"], str)
    assert result["emoji_icon"] == "☀️"
    assert isinstance(result, dict)

    icon = WeatherIconEnum.CLOUDY
    result = weather_icon_enum_to_dict(icon)
    assert result["name"] == "cloudy"
    assert isinstance(result["fa_icon"], str)
    assert result["emoji_icon"] == "☁️"
    assert isinstance(result, dict)


def test_dict_to_weather_icon_enum():
    data = {
        "name": "sunny",
        "fa_icon": "fa-sun",
        "emoji_icon": "☀️"
    }
    icon = dict_to_weather_icon_enum(data)
    assert isinstance(icon, WeatherIconEnum)
    assert icon == WeatherIconEnum.SUNNY
    assert icon.emoji_icon == "☀️"


def test_dict_to_weather_icon_enum_rain():
    data = {
        "name": "rain",
        "fa_icon": "fa-cloud-rain",
        "emoji_icon": "🌧️"
    }
    icon = dict_to_weather_icon_enum(data)
    assert icon == WeatherIconEnum.RAIN


def test_dict_to_weather_icon_enum_cloudy():
    data = {
        "name": "cloudy",
        "fa_icon": "fa-cloud",
        "emoji_icon": "☁️"
    }
    icon = dict_to_weather_icon_enum(data)
    assert icon == WeatherIconEnum.CLOUDY


def test_dict_to_weather_icon_enum_snow():
    data = {
        "name": "snow",
        "fa_icon": "fa-snow",
        "emoji_icon": "❄️"
    }
    icon = dict_to_weather_icon_enum(data)
    assert icon == WeatherIconEnum.SNOW


def test_dict_to_weather_icon_enum_roundtrip():
    original = WeatherIconEnum.SNOW
    data = weather_icon_enum_to_dict(original)
    reconstructed = dict_to_weather_icon_enum(data)
    assert reconstructed == original
    assert reconstructed.emoji_icon == original.emoji_icon
