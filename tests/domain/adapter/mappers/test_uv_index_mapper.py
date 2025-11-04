import pytest
from weathergrabber.domain.entities.uv_index import UVIndex
from weathergrabber.domain.adapter.mappers.uv_index_mapper import uv_index_to_dict

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
