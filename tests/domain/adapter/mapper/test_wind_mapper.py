class DummyWind:
    direction = "NW"
    speed = "10 km/h"

from weathergrabber.domain.adapter.mapper.wind_mapper import wind_to_dict

def test_wind_to_dict():
    wind = DummyWind()
    d = wind_to_dict(wind)
    assert d["direction"] == "NW"
    assert d["speed"] == "10 km/h"
    assert isinstance(d, dict)

def test_wind_to_dict_none():
    d = wind_to_dict(None)
    assert d is None
