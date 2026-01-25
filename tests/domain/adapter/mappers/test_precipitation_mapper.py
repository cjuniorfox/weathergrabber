import pytest
from weathergrabber.domain.entities.precipitation import Precipitation
from weathergrabber.domain.adapter.mappers.precipitation_mapper import precipitation_to_dict, dict_to_precipitation

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


def test_dict_to_precipitation():
    data = {"percentage": "80%", "amount": "5mm"}
    p = dict_to_precipitation(data)
    assert isinstance(p, Precipitation)
    assert p.percentage == "80%"
    assert p.amount == "5mm"


def test_dict_to_precipitation_none_amount():
    data = {"percentage": "0%", "amount": None}
    p = dict_to_precipitation(data)
    assert p.percentage == "0%"
    assert p.amount is None


def test_dict_to_precipitation_zero_percentage():
    data = {"percentage": "0%", "amount": "0mm"}
    p = dict_to_precipitation(data)
    assert p.percentage == "0%"
    assert p.amount == "0mm"


def test_dict_to_precipitation_high_values():
    data = {"percentage": "100%", "amount": "50mm"}
    p = dict_to_precipitation(data)
    assert p.percentage == "100%"
    assert p.amount == "50mm"


def test_dict_to_precipitation_roundtrip():
    original = Precipitation(percentage="45%", amount="10mm")
    data = precipitation_to_dict(original)
    reconstructed = dict_to_precipitation(data)
    assert reconstructed.percentage == original.percentage
    assert reconstructed.amount == original.amount
