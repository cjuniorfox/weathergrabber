import pytest
from weathergrabber.domain.precipitation import Precipitation
from weathergrabber.domain.adapter.mapper.precipitation_mapper import precipitation_to_dict

def test_precipitation_to_dict():
    p = Precipitation(percentage="80%", amount="5mm")
    result = precipitation_to_dict(p)
    assert result == {"percentage": "80%", "amount": "5mm"}
    assert isinstance(result, dict)

def test_precipitation_to_dict_none_amount():
    p = Precipitation(percentage="20%", amount=None)
    result = precipitation_to_dict(p)
    assert result == {"percentage": "20%", "amount": None}
    assert isinstance(result, dict)
