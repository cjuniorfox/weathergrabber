import pytest
from weathergrabber.domain.hourly_predictions import HourlyPredictions
from weathergrabber.domain.weather_icon_enum import WeatherIconEnum
from weathergrabber.domain.precipitation import Precipitation
from weathergrabber.domain.wind import Wind
from weathergrabber.domain.uv_index import UVIndex
from weathergrabber.domain.adapter.mapper.hourly_predictions_mapper import hourly_predictions_to_dict

def test_hourly_predictions_to_dict():
    precipitation = Precipitation(percentage="80%", amount="5mm")
    wind = Wind(direction="N", speed="10 km/h")
    uv_index = UVIndex(string_value="5", index="5", of="10", label="UV Index")
    hp = HourlyPredictions(
        title="10:00 AM",
        temperature="22°C",
        icon=WeatherIconEnum.SUNNY,
        summary="Sunny",
        precipitation=precipitation,
        wind=wind,
        feels_like="21°C",
        humidity="50%",
        uv_index=uv_index,
        cloud_cover="10%"
    )
    result = hourly_predictions_to_dict(hp)
    assert result["title"] == "10:00 AM"
    assert result["temperature"] == "22°C"
    assert result["icon"]["name"] == "sunny"
    assert result["summary"] == "Sunny"
    assert result["precipitation"] == {"percentage": "80%", "amount": "5mm"}
    assert result["wind"] == {"direction": "N", "speed": "10 km/h"}
    assert result["feels_like"] == "21°C"
    assert result["humidity"] == "50%"
    assert result["uv_index"] == {"string_value": "5", "index": "5", "of": "10", "label": "UV Index"}
    assert result["cloud_cover"] == "10%"
    assert isinstance(result, dict)

def test_hourly_predictions_to_dict_none():
    hp = HourlyPredictions(
        title="11:00 AM",
        temperature="20°C",
        icon=None,
        summary="Cloudy",
        precipitation=None,
        wind=None,
        feels_like=None,
        humidity=None,
        uv_index=None,
        cloud_cover=None
    )
    result = hourly_predictions_to_dict(hp)
    assert result["title"] == "11:00 AM"
    assert result["temperature"] == "20°C"
    assert result["icon"] is None
    assert result["summary"] == "Cloudy"
    assert result["precipitation"] is None
    assert result["wind"] is None
    assert result["feels_like"] is None
    assert result["humidity"] is None
    assert result["uv_index"] is None
    assert result["cloud_cover"] is None
    assert isinstance(result, dict)
