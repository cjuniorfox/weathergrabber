import pytest
from weathergrabber.domain.entities.search import Search
from weathergrabber.domain.adapter.mappers.search_mapper import search_to_dict

def test_search_to_dict():
    s = Search(id="dummy_id", search_name="dummy_name")
    result = search_to_dict(s)
    assert result == {"id": "dummy_id", "search_name": "dummy_name"}
    assert isinstance(result, dict)

def test_search_to_dict_none_name():
    s = Search(id="dummy_id", search_name=None)
    result = search_to_dict(s)
    assert result == {"id": "dummy_id", "search_name": None}
    assert isinstance(result, dict)
