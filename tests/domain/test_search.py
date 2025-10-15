import pytest
from weathergrabber.domain.search import Search

def test_search_properties():
    s = Search("12345", "TestCity")
    assert s.id == "12345"
    assert s.search_name == "TestCity"
    r = repr(s)
    assert "Search(" in r
    assert "id='12345'" in r
    assert "search_name='TestCity'" in r

def test_search_no_name():
    s = Search("67890")
    assert s.id == "67890"
    assert s.search_name is None
    r = repr(s)
    assert "search_name=None" in r
