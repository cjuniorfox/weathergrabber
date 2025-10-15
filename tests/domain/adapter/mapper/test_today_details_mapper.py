import pytest
from weathergrabber.domain.today_details import TodayDetails
from weathergrabber.domain.label_value import LabelValue
from weathergrabber.domain.sunrise_sunset import SunriseSunset
from weathergrabber.domain.temperature_hight_low import TemperatureHighLow
from weathergrabber.domain.uv_index import UVIndex
from weathergrabber.domain.moon_phase import MoonPhase
from weathergrabber.domain.moon_phase_enum import MoonPhaseEnum
from weathergrabber.domain.adapter.mapper.today_details_mapper import today_details_to_dict

def test_today_details_to_dict():
    feelslike = LabelValue(label="Feels Like", value="25°C")
    sunrise_sunset = SunriseSunset(sunrise="06:00", sunset="18:00")
    high_low = TemperatureHighLow(high="30°C", low="20°C", label="High/Low")
    wind = LabelValue(label="Wind", value="10 km/h")
    humidity = LabelValue(label="Humidity", value="60%")
    dew_point = LabelValue(label="Dew Point", value="15°C")
    pressure = LabelValue(label="Pressure", value="1013 hPa")
    uv_index = UVIndex(string_value="5", index="5", of="10", label="UV Index")
    visibility = LabelValue(label="Visibility", value="10 km")
    moon_phase = MoonPhase(icon=MoonPhaseEnum.PHASE_14, phase="Full Moon", label="Full Moon")

    td = TodayDetails(
        feelslike=feelslike,
        sunrise_sunset=sunrise_sunset,
        high_low=high_low,
        wind=wind,
        humidity=humidity,
        dew_point=dew_point,
        pressure=pressure,
        uv_index=uv_index,
        visibility=visibility,
        moon_phase=moon_phase
    )
    result = today_details_to_dict(td)
    assert result["feelslike"] == {"label": "Feels Like", "value": "25°C"}
    assert result["sunrise_sunset"]["sunrise"]["icon"] is not None
    assert result["high_low"] == {"high": "30°C", "low": "20°C", "label": "High/Low"}
    assert result["wind"] == {"label": "Wind", "value": "10 km/h"}
    assert result["humidity"] == {"label": "Humidity", "value": "60%"}
    assert result["dew_point"] == {"label": "Dew Point", "value": "15°C"}
    assert result["pressure"] == {"label": "Pressure", "value": "1013 hPa"}
    assert result["uv_index"] == {"string_value": "5", "index": "5", "of": "10", "label": "UV Index"}
    assert result["visibility"] == {"label": "Visibility", "value": "10 km"}
    assert result["moon_phase"] == {"icon": "phase-14", "phase": "Full Moon", "label": "Full Moon"}
    assert isinstance(result, dict)

def test_today_details_to_dict_none():
    td = TodayDetails(
        feelslike=None,
        sunrise_sunset=None,
        high_low=None,
        wind=None,
        humidity=None,
        dew_point=None,
        pressure=None,
        uv_index=None,
        visibility=None,
        moon_phase=None
    )
    result = today_details_to_dict(td)
    assert result["feelslike"] is None
    assert result["sunrise_sunset"] is None
    assert result["high_low"] is None
    assert result["wind"] is None
    assert result["humidity"] is None
    assert result["dew_point"] is None
    assert result["pressure"] is None
    assert result["uv_index"] is None
    assert result["visibility"] is None
    assert result["moon_phase"] is None
    assert isinstance(result, dict)
