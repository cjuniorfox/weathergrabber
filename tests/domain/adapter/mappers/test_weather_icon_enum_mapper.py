import pytest
from weathergrabber.domain.entities.weather_icon_enum import WeatherIconEnum
from weathergrabber.domain.adapter.mappers.weather_icon_enum_mapper import weather_icon_enum_to_dict

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
