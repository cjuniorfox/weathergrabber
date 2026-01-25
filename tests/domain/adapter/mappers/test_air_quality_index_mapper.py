from weathergrabber.domain.entities.air_quality_index import AirQualityIndex
from weathergrabber.domain.entities.color import Color
from weathergrabber.domain.adapter.mappers.air_quality_index_mapper import air_quality_index_to_dict, dict_to_air_quality_index

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


def test_dict_to_air_quality_index():
    data = {
        "title": "Air Quality Index",
        "value": 42,
        "category": "Good",
        "description": "Air quality is good.",
        "acronym": "AQI",
        "color": {"red": 255, "green": 0, "blue": 0, "hex": "FF0000"}
    }
    aqi = dict_to_air_quality_index(data)
    assert isinstance(aqi, AirQualityIndex)
    assert aqi.title == "Air Quality Index"
    assert aqi.value == 42
    assert aqi.category == "Good"
    assert aqi.description == "Air quality is good."
    assert aqi.acronym == "AQI"
    assert aqi.color is not None
    assert aqi.color.hex == "FF0000"


def test_dict_to_air_quality_index_none_color():
    data = {
        "title": "Air Quality Index",
        "value": 42,
        "category": "Good",
        "description": "Air quality is good.",
        "acronym": "AQI",
        "color": None
    }
    aqi = dict_to_air_quality_index(data)
    assert aqi.color is None


def test_dict_to_air_quality_index_missing_color():
    data = {
        "title": "Air Quality Index",
        "value": 42,
        "category": "Good",
        "description": "Air quality is good.",
        "acronym": "AQI"
    }
    aqi = dict_to_air_quality_index(data)
    assert aqi.color is None


def test_dict_to_air_quality_index_roundtrip():
    original_aqi = AirQualityIndex(
        title="Air Quality Index",
        value=50,
        category="Moderate",
        description="Air quality is moderate.",
        acronym="AQI",
        color=Color(255, 165, 0)
    )
    data = air_quality_index_to_dict(original_aqi)
    reconstructed_aqi = dict_to_air_quality_index(data)
    assert reconstructed_aqi.title == original_aqi.title
    assert reconstructed_aqi.value == original_aqi.value
    assert reconstructed_aqi.category == original_aqi.category
    assert reconstructed_aqi.description == original_aqi.description
    assert reconstructed_aqi.acronym == original_aqi.acronym
    assert reconstructed_aqi.color.hex == original_aqi.color.hex
