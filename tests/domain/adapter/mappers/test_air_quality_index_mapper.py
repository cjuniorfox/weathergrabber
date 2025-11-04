from weathergrabber.domain.entities.air_quality_index import AirQualityIndex
from weathergrabber.domain.entities.color import Color
from weathergrabber.domain.adapter.mappers.air_quality_index_mapper import air_quality_index_to_dict

def test_air_quality_index_to_dict():
    aqi = AirQualityIndex(
        title="Air Quality Index",
        value=42,
        category="Good",
        description="Air quality is good.",
        acronym="AQI",
        color=Color(255, 0, 0)
    )
    d = air_quality_index_to_dict(aqi)
    assert d["title"] == "Air Quality Index"
    assert d["value"] == 42
    assert d["category"] == "Good"
    assert d["description"] == "Air quality is good."
    assert d["acronym"] == "AQI"
    assert isinstance(d["color"], dict)
    assert d["color"]["hex"] == "FF0000"

def test_air_quality_index_to_dict_none_color():
    aqi = AirQualityIndex(
        title="Air Quality Index",
        value=42,
        category="Good",
        description="Air quality is good.",
        acronym="AQI",
        color=None
    )
    d = air_quality_index_to_dict(aqi)
    assert d["color"] is None
