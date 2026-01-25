import pytest
from weathergrabber.domain.entities.today_details import TodayDetails
from weathergrabber.domain.entities.label_value import LabelValue
from weathergrabber.domain.entities.sunrise_sunset import SunriseSunset
from weathergrabber.domain.entities.temperature_hight_low import TemperatureHighLow
from weathergrabber.domain.entities.uv_index import UVIndex
from weathergrabber.domain.entities.moon_phase import MoonPhase
from weathergrabber.domain.entities.moon_phase_enum import MoonPhaseEnum
from weathergrabber.domain.adapter.mappers.today_details_mapper import today_details_to_dict, dict_to_today_details

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


def test_dict_to_today_details():
    data = {
        "feelslike": {"label": "Feels Like", "value": "25°C"},
        "sunrise_sunset": {
            "sunrise": {"icon": {"name": "sunrise"}, "value": "06:00"},
            "sunset": {"icon": {"name": "sunset"}, "value": "18:00"}
        },
        "high_low": {"high": "30°C", "low": "20°C", "label": "High/Low"},
        "wind": {"label": "Wind", "value": "10 km/h"},
        "humidity": {"label": "Humidity", "value": "60%"},
        "dew_point": {"label": "Dew Point", "value": "15°C"},
        "pressure": {"label": "Pressure", "value": "1013 hPa"},
        "uv_index": {"string_value": "5", "index": "5", "of": "10", "label": "UV Index"},
        "visibility": {"label": "Visibility", "value": "10 km"},
        "moon_phase": {"icon": "phase-14", "phase": "Full Moon", "label": "Full Moon"}
    }
    td = dict_to_today_details(data)
    assert isinstance(td, TodayDetails)
    assert td.feelslike.label == "Feels Like"
    assert td.high_low.high == "30°C"
    assert td.wind.value == "10 km/h"
    assert td.humidity.value == "60%"
    assert td.dew_point.label == "Dew Point"
    assert td.pressure.value == "1013 hPa"
    assert td.uv_index.index == "5"
    assert td.visibility.value == "10 km"
    assert td.moon_phase.phase == "Full Moon"


def test_dict_to_today_details_none_values():
    data = {
        "feelslike": None,
        "sunrise_sunset": None,
        "high_low": None,
        "wind": None,
        "humidity": None,
        "dew_point": None,
        "pressure": None,
        "uv_index": None,
        "visibility": None,
        "moon_phase": None
    }
    td = dict_to_today_details(data)
    assert td.feelslike is None
    assert td.sunrise_sunset is None
    assert td.high_low is None
    assert td.wind is None
    assert td.humidity is None
    assert td.dew_point is None
    assert td.pressure is None
    assert td.uv_index is None
    assert td.visibility is None
    assert td.moon_phase is None


def test_dict_to_today_details_partial_data():
    data = {
        "feelslike": {"label": "Feels Like", "value": "22°C"},
        "high_low": {"high": "28°C", "low": "18°C", "label": "Temp"}
    }
    td = dict_to_today_details(data)
    assert td.feelslike.value == "22°C"
    assert td.high_low.high == "28°C"
    assert td.wind is None
    assert td.humidity is None


def test_dict_to_today_details_roundtrip():
    original = TodayDetails(
        feelslike=LabelValue(label="Feels", value="24°C"),
        sunrise_sunset=SunriseSunset(sunrise="05:45", sunset="19:30"),
        high_low=TemperatureHighLow(high="29°C", low="19°C", label="Temp"),
        wind=LabelValue(label="Wind", value="8 km/h"),
        humidity=LabelValue(label="Humidity", value="55%"),
        dew_point=LabelValue(label="Dew", value="14°C"),
        pressure=LabelValue(label="Press", value="1012 hPa"),
        uv_index=UVIndex(string_value="4", index="4", of="10", label="Moderate"),
        visibility=LabelValue(label="Visibility", value="12 km"),
            moon_phase=MoonPhase(icon=MoonPhaseEnum.PHASE_8, phase="First Quarter", label="Quarter")
    )
    data = today_details_to_dict(original)
    reconstructed = dict_to_today_details(data)
    assert reconstructed.feelslike.label == original.feelslike.label
    assert reconstructed.high_low.high == original.high_low.high
    assert reconstructed.wind.value == original.wind.value
    assert reconstructed.humidity.value == original.humidity.value
