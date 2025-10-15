import pytest
from weathergrabber.domain.precipitation import Precipitation

def test_precipitation_properties():
    p = Precipitation("10%", "0 mm")
    assert p.percentage == "10%"
    assert p.amount == "0 mm"
    r = repr(p)
    assert "Precipitation(" in r
    assert "percentage='10%'" in r
    assert "amount='0 mm'" in r

def test_precipitation_no_amount():
    p = Precipitation("20%")
    assert p.percentage == "20%"
    assert p.amount is None
    r = repr(p)
    assert "amount='None'" in r
