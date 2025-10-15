import pytest
from weathergrabber.domain.air_quality_index import AirQualityIndex
from weathergrabber.domain.color import Color

def test_from_string_valid():
    data = "Air Quality Index\n26\nGood\nAir quality is considered satisfactory, and air pollution poses little or no risk."
    aqi = AirQualityIndex.from_string(data)
    assert aqi.title == "Air Quality Index"
    assert aqi.value == 26
    assert aqi.category == "Good"
    assert aqi.description.startswith("Air quality is considered satisfactory")
    assert aqi.acronym == "AQI"
    assert aqi.color is None

def test_from_string_invalid():
    with pytest.raises(ValueError):
        AirQualityIndex.from_string("Invalid\nData")

def test_aqi_color_from_string_valid():
    aqi_data = "Air Quality Index\n50\nModerate\nSome pollution risk."
    color_data = "#FFFF00"
    aqi = AirQualityIndex.aqi_color_from_string(aqi_data, color_data)
    assert aqi.value == 50
    assert aqi.category == "Moderate"
    assert isinstance(aqi.color, Color)
    assert str(aqi.color) == "FFFF00"

def test_aqi_color_from_string_invalid_color():
    aqi_data = "Air Quality Index\n50\nModerate\nSome pollution risk."
    color_data = "not-a-color"
    with pytest.raises(ValueError):
        AirQualityIndex.aqi_color_from_string(aqi_data, color_data)

def test_air_quality_index_repr():
    aqi = AirQualityIndex("AQI", 42, "Good", "Air quality is good.", "AQI", None)
    r = repr(aqi)
    assert "AirQualityIndex(" in r
    assert "title='AQI'" in r
    assert "value=42" in r
    assert "category='Good'" in r
    assert "description='Air quality is good.'" in r
    assert "acronym='AQI'" in r
