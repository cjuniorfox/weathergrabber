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

def test_repr():
    uv = UVIndex(string_value="5", index="5", of="10", label="UV Index")
    r = repr(uv)
    assert "UVIndex(" in r
    assert "string_value='5'" in r
    assert "index='5'" in r
    assert "of='10'" in r
    assert "label='UV Index'" in r

    uv = UVIndex(string_value="3", index="3", of=None, label=None)
    r = repr(uv)
    assert "string_value='3'" in r
    assert "label=None" in r

def test_str_string_value():
    uv = UVIndex(string_value="5", index="5", of="10", label="UV Index")
    s = str(uv)
    assert s == "UV Index 5"

def test_str_index_of_label():
    uv = UVIndex(string_value=None, index="7", of="10", label="UV Index")
    s = str(uv)
    assert s == "UV Index 7 10"

def test_str_index_of_no_label():
    uv = UVIndex(string_value=None, index="7", of="10", label=None)
    s = str(uv)
    assert s == "7 10"

def test_str_fallback_empty():
    uv = UVIndex(string_value=None, index=None, of=None, label=None)
    s = str(uv)
    # Should not raise, but will be 'None None None'
    assert isinstance(s, str)
    # Optionally, check for the exact fallback string
    assert s == "None None"

def test_from_string_fallback():
    # Two parts, not handled by other branches
    uvi = UVIndex.from_string("foo bar", "UV Index")
    assert uvi.string_value == "foo bar"
    assert uvi.index == ""
    assert uvi.of == ""
    assert uvi.label == "UV Index"
