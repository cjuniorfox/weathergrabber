import pytest
from weathergrabber.domain.entities.hourly_predictions import HourlyPredictions

class DummyIcon: pass
class DummyPrecipitation: pass
class DummyWind: pass
class DummyUVIndex: pass

def test_hourly_predictions_properties():
    title = "10:00 AM"
    temperature = "22°C"
    icon = DummyIcon()
    summary = "Sunny"
    precipitation = DummyPrecipitation()
    wind = DummyWind()
    feels_like = "21°C"
    humidity = "50%"
    uv_index = DummyUVIndex()
    cloud_cover = "10%"
    hp = HourlyPredictions(title, temperature, icon, summary, precipitation, wind, feels_like, humidity, uv_index, cloud_cover)
    assert hp.title == "10:00 AM"
    assert hp.temperature == "22°C"
    assert hp.icon is icon
    assert hp.summary == "Sunny"
    assert hp.precipitation is precipitation
    assert hp.wind is wind
    assert hp.feels_like == "21°C"
    assert hp.humidity == "50%"
    assert hp.uv_index is uv_index
    assert hp.cloud_cover == "10%"
    r = repr(hp)
    assert "HourlyPredictions(" in r
    assert "title=" in r
    assert "temperature=" in r
    assert "icon=" in r
    assert "summary=" in r
    assert "precipitation=" in r
    assert "wind=" in r
    assert "feels_like=" in r
    assert "humidity=" in r
    assert "uv_index=" in r
    assert "cloud_cover=" in r
