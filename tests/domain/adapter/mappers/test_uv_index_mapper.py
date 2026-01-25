import pytest
from weathergrabber.domain.entities.uv_index import UVIndex
from weathergrabber.domain.adapter.mappers.uv_index_mapper import uv_index_to_dict, dict_to_uv_index

def test_uv_index_to_dict():
    uv = UVIndex(string_value="5", index="5", of="10", label="UV Index")
    result = uv_index_to_dict(uv)
    assert result == {"string_value": "5", "index": "5", "of": "10", "label": "UV Index"}
    assert isinstance(result, dict)

def test_uv_index_to_dict_none_of_label():
    uv = UVIndex(string_value="3", index="3", of=None, label=None)
    result = uv_index_to_dict(uv)
    assert result == {"string_value": "3", "index": "3", "of": None, "label": None}
    assert isinstance(result, dict)


def test_dict_to_uv_index():
    data = {
        "string_value": "6",
        "index": "6",
        "of": "11",
        "label": "High"
    }
    uv = dict_to_uv_index(data)
    assert isinstance(uv, UVIndex)
    assert uv.string_value == "6"
    assert uv.index == "6"
    assert uv.of == "11"
    assert uv.label == "High"


def test_dict_to_uv_index_none_values():
    data = {
        "string_value": None,
        "index": None,
        "of": None,
        "label": None
    }
    uv = dict_to_uv_index(data)
    assert uv.string_value is None
    assert uv.index is None
    assert uv.of is None
    assert uv.label is None


def test_dict_to_uv_index_missing_keys():
    data = {}
    uv = dict_to_uv_index(data)
    assert uv.string_value is None
    assert uv.index is None
    assert uv.of is None
    assert uv.label is None


def test_dict_to_uv_index_various_levels():
    test_cases = [
        ({"string_value": "1", "index": "1", "of": "10", "label": "Low"}, "Low"),
        ({"string_value": "5", "index": "5", "of": "10", "label": "Moderate"}, "Moderate"),
        ({"string_value": "8", "index": "8", "of": "11", "label": "Very High"}, "Very High"),
    ]
    for data, expected_label in test_cases:
        uv = dict_to_uv_index(data)
        assert uv.label == expected_label


def test_dict_to_uv_index_roundtrip():
    original = UVIndex(string_value="7", index="7", of="11", label="Extreme")
    data = uv_index_to_dict(original)
    reconstructed = dict_to_uv_index(data)
    assert reconstructed.string_value == original.string_value
    assert reconstructed.index == original.index
    assert reconstructed.of == original.of
    assert reconstructed.label == original.label
