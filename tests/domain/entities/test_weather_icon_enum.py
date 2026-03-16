import pytest
from weathergrabber.domain.entities.weather_icon_enum import WeatherIconEnum

def test_enum_members():
    # Test a few representative members
    assert WeatherIconEnum.SUNNY.name == "sunny"
    assert WeatherIconEnum.SUNNY.fa_icon is not None
    assert WeatherIconEnum.SUNNY.emoji_icon == "☀️"
    assert WeatherIconEnum.CLOUDY.name == "cloudy"
    assert WeatherIconEnum.CLOUDY.emoji_icon == "☁️"
    assert WeatherIconEnum.RAIN.name == "rain"
    assert WeatherIconEnum.RAIN.emoji_icon == "🌧️"
    assert WeatherIconEnum.SNOW.name == "snow"
    assert WeatherIconEnum.SNOW.emoji_icon == "❄️"
    assert WeatherIconEnum.BLOWING_DRIFTING_SNOW.name == "blowing-drifting-snow"
    assert WeatherIconEnum.BLOWING_DRIFTING_SNOW.emoji_icon == "🌨️"
    assert WeatherIconEnum.SUNRISE.emoji_icon == "🌅"
    assert WeatherIconEnum.SUNSET.emoji_icon == "🌇"

def test_from_name_valid():
    assert WeatherIconEnum.from_name("sunny") == WeatherIconEnum.SUNNY
    assert WeatherIconEnum.from_name("cloudy") == WeatherIconEnum.CLOUDY
    assert WeatherIconEnum.from_name("rain") == WeatherIconEnum.RAIN
    assert WeatherIconEnum.from_name("blowing-drifting-snow") == WeatherIconEnum.BLOWING_DRIFTING_SNOW

def test_from_name_invalid():
    with pytest.raises(ValueError):
        WeatherIconEnum.from_name("not-a-real-icon")

def test_all_enum_members_have_properties():
    for icon in WeatherIconEnum:
        assert isinstance(icon.name, str)
        assert isinstance(icon.fa_icon, str)
        assert isinstance(icon.emoji_icon, str)
