import pytest
from weathergrabber.domain.entities.wind import Wind

def test_wind_properties():
    w = Wind(direction="N", speed="10 km/h")
    assert w.direction == "N"
    assert w.speed == "10 km/h"
    assert str(w) == "Wind Speed: N 10 km/h"
    r = repr(w)
    assert "Wind(direction:'N', speed: '10 km/h')" == r

def test_wind_from_string_valid():
    w = Wind.from_string("S 9\xa0mph")
    assert w.direction == "S"
    assert w.speed == "9\xa0mph"
    assert str(w) == "Wind Speed: S 9\xa0mph"

def test_wind_from_string_invalid():
    with pytest.raises(ValueError):
        Wind.from_string("invalidstring")
    with pytest.raises(ValueError):
        Wind.from_string("")
    with pytest.raises(ValueError):
        Wind.from_string("N")
    with pytest.raises(ValueError):
        Wind.from_string("N 10 km/h extra")
