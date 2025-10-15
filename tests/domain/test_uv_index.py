import pytest
from weathergrabber.domain.uv_index import UVIndex

def test_uv_index_properties():
    uvi = UVIndex("5 of 12", "5", "12", "UV Index")
    assert uvi.string_value == "5 of 12"
    assert uvi.index == "5"
    assert uvi.of == "12"
    assert uvi.label == "UV Index"
    assert str(uvi).startswith("UV Index 5 of 12")
    r = repr(uvi)
    assert "UVIndex(" in r
    assert "string_value='5 of 12'" in r
    assert "index='5'" in r
    assert "of='12'" in r
    assert "label='UV Index'" in r

def test_from_string_single():
    uvi = UVIndex.from_string("7", "UV Index")
    assert uvi.index == "7"
    assert uvi.of == ""
    assert uvi.label == "UV Index"
    assert str(uvi).startswith("UV Index 7")

def test_from_string_three_parts():
    uvi = UVIndex.from_string("8 of 15", "UV Index")
    assert uvi.index == "8"
    assert uvi.of == "15"
    assert uvi.label == "UV Index"
    assert str(uvi).startswith("UV Index 8 of 15")

def test_from_string_empty():
    with pytest.raises(ValueError):
        UVIndex.from_string("")
