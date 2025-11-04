import pytest
from weathergrabber.domain.entities.daily_predictions import DailyPredictions
from weathergrabber.domain.entities.temperature_hight_low import TemperatureHighLow
from weathergrabber.domain.entities.weather_icon_enum import WeatherIconEnum
from weathergrabber.domain.entities.precipitation import Precipitation
from weathergrabber.domain.entities.moon_phase import MoonPhase
from weathergrabber.domain.entities.moon_phase_enum import MoonPhaseEnum
from weathergrabber.domain.adapter.mappers.daily_predictions_mapper import daily_predictions_to_dict

def test_daily_predictions_to_dict():
    high_low = TemperatureHighLow(high="30°C", low="20°C", label="High/Low")
    icon = WeatherIconEnum.SUNNY
    precipitation = Precipitation(percentage="80%", amount="5mm")
    moon_phase = MoonPhase(icon=MoonPhaseEnum.PHASE_14, phase="Full Moon", label="Full Moon")
    dp = DailyPredictions(
        title="Today",
        high_low=high_low,
        icon=icon,
        summary="Sunny",
        precipitation=precipitation,
        moon_phase=moon_phase
    )
    result = daily_predictions_to_dict(dp)
    assert result["title"] == "Today"
    assert result["high_low"] == {"high": "30°C", "low": "20°C", "label": "High/Low"}
    assert result["icon"]["name"] == "sunny"
    assert result["summary"] == "Sunny"
    assert result["precipitation"] == {"percentage": "80%", "amount": "5mm"}
    assert result["moon_phase"] == {"icon": "phase-14", "phase": "Full Moon", "label": "Full Moon"}
    assert isinstance(result, dict)

def test_daily_predictions_to_dict_none():
    dp = DailyPredictions(
        title="Tomorrow",
        high_low=None,
        icon=None,
        summary="Cloudy",
        precipitation=None,
        moon_phase=None
    )
    result = daily_predictions_to_dict(dp)
    assert result["title"] == "Tomorrow"
    assert result["high_low"] is None
    assert result["icon"] is None
    assert result["summary"] == "Cloudy"
    assert result["precipitation"] is None
    assert result["moon_phase"] is None
    assert isinstance(result, dict)
