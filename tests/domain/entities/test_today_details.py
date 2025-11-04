import pytest
from weathergrabber.domain.entities.today_details import TodayDetails

class DummyLabelValue: pass
class DummySunriseSunset: pass
class DummyTemperatureHighLow: pass
class DummyUVIndex: pass
class DummyMoonPhase: pass

def test_today_details_properties():
    feelslike = DummyLabelValue()
    sunrise_sunset = DummySunriseSunset()
    high_low = DummyTemperatureHighLow()
    wind = DummyLabelValue()
    humidity = DummyLabelValue()
    dew_point = DummyLabelValue()
    pressure = DummyLabelValue()
    uv_index = DummyUVIndex()
    visibility = DummyLabelValue()
    moon_phase = DummyMoonPhase()
    td = TodayDetails(
        feelslike,
        sunrise_sunset,
        high_low,
        wind,
        humidity,
        dew_point,
        pressure,
        uv_index,
        visibility,
        moon_phase
    )
    assert td.feelslike is feelslike
    assert td.sunrise_sunset is sunrise_sunset
    assert td.high_low is high_low
    assert td.wind is wind
    assert td.humidity is humidity
    assert td.dew_point is dew_point
    assert td.pressure is pressure
    assert td.uv_index is uv_index
    assert td.visibility is visibility
    assert td.moon_phase is moon_phase
    r = repr(td)
    assert "TodayDetails(" in r
    assert "feelslike=" in r
    assert "sunrise_sunset=" in r
    assert "high_low=" in r
    assert "wind=" in r
    assert "humidity=" in r
    assert "dew_point=" in r
    assert "pressure=" in r
    assert "uv_index=" in r
    assert "visibility=" in r
    assert "moon_phase=" in r
