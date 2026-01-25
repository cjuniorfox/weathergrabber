import pytest
from weathergrabber.domain.entities.hourly_predictions import HourlyPredictions
from weathergrabber.domain.entities.weather_icon_enum import WeatherIconEnum
from weathergrabber.domain.entities.precipitation import Precipitation
from weathergrabber.domain.entities.wind import Wind
from weathergrabber.domain.entities.uv_index import UVIndex
from weathergrabber.domain.adapter.mappers.hourly_predictions_mapper import hourly_predictions_to_dict, dict_to_hourly_predictions

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


def test_dict_to_hourly_predictions():
    data = {
        "title": "10:00 AM",
        "temperature": "22°C",
        "icon": {"name": "sunny", "fa_icon": "fa-sun", "emoji_icon": "☀️"},
        "summary": "Sunny",
        "precipitation": {"percentage": "80%", "amount": "5mm"},
        "wind": {"direction": "N", "speed": "10 km/h"},
        "feels_like": "21°C",
        "humidity": "50%",
        "uv_index": {"string_value": "5", "index": "5", "of": "10", "label": "UV Index"},
        "cloud_cover": "10%"
    }
    hp = dict_to_hourly_predictions(data)
    assert isinstance(hp, HourlyPredictions)
    assert hp.title == "10:00 AM"
    assert hp.temperature == "22°C"
    assert hp.icon == WeatherIconEnum.SUNNY
    assert hp.summary == "Sunny"
    assert hp.precipitation.percentage == "80%"
    assert hp.wind.direction == "N"
    assert hp.feels_like == "21°C"
    assert hp.humidity == "50%"
    assert hp.uv_index.index == "5"
    assert hp.cloud_cover == "10%"


def test_dict_to_hourly_predictions_none_values():
    data = {
        "title": "2:00 PM",
        "temperature": "25°C",
        "icon": None,
        "summary": "Clear",
        "precipitation": None,
        "wind": None,
        "feels_like": None,
        "humidity": None,
        "uv_index": None,
        "cloud_cover": None
    }
    hp = dict_to_hourly_predictions(data)
    assert hp.icon is None
    assert hp.precipitation is None
    assert hp.wind is None
    assert hp.uv_index is None


def test_dict_to_hourly_predictions_roundtrip():
    original = HourlyPredictions(
        title="3:00 PM",
        temperature="26°C",
        icon=WeatherIconEnum.CLOUDY,
        summary="Partly cloudy",
        precipitation=Precipitation(percentage="20%", amount="2mm"),
        wind=Wind(direction="S", speed="5 km/h"),
        feels_like="25°C",
        humidity="55%",
        uv_index=UVIndex(string_value="6", index="6", of="10", label="High"),
        cloud_cover="30%"
    )
    data = hourly_predictions_to_dict(original)
    reconstructed = dict_to_hourly_predictions(data)
    assert reconstructed.title == original.title
    assert reconstructed.temperature == original.temperature
    assert reconstructed.icon == original.icon
    assert reconstructed.humidity == original.humidity
